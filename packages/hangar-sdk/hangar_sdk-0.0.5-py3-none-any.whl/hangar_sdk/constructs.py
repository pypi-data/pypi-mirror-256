import os
import tarfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional

from aiohttp import ClientError
from pydantic import BaseModel

from .base import HangarScope
from .library import CompositeResource, Deployable


class SourceInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, source):
        pass


@dataclass
class S3(CompositeResource, Deployable):
    scope: HangarScope
    name: str

    @property
    def client(self):
        session = self.scope.get_boto3_session()
        return session.client("s3")

    def create_construct_definition(self) -> dict:
        return {
            "construct": "s3",
            "name": self.name,
        }


@dataclass
class GCS(CompositeResource, Deployable):
    location: str

    def create_construct_definition(self) -> dict:
        return {"construct": "gcs", "name": self.name, "location": self.location}


@dataclass
class Asset(CompositeResource, Deployable):
    source: SourceInterface
    bucket: S3

    def create_construct_definition(self) -> dict:
        return {
            "construct": "asset",
            "name": self.name,
            "source": {"!REF": True, "resourceId": self.source.name},
            "bucket": self.bucket._get_ref(),
        }

    def post_resolve(self):
        print("uploading asset")
        self.sync()

    def sync(self, token=None):
        if self.mode == "delete":
            return

        if isinstance(self.source, DirPath):
            fname = f"{self.source.name}.tar"

            with tarfile.open(fname, "w") as tar:
                tar.add(self.source.path, arcname=os.path.basename(self.source.path))

            try:
                self.bucket.client.upload_file(fname, self.bucket.name, f"{self.source.name}/{fname}")
            except ClientError as e:
                print(e)

        elif isinstance(self.source, FilePath):
            try:
                self.bucket.client.upload_file(
                    self.source.path,
                    self.bucket.name,
                    self.source.name
                    if self.source.name
                    else os.path.basename(self.source.path),
                )
            except ClientError as e:
                print(e)

        elif isinstance(self.source, GitHubRepo):
            self.scope.execute_action(
                self.name, "sync", {"token": token} if token is not None else {}
            )


@dataclass
class DirPath(CompositeResource, SourceInterface, Deployable):
    path: str
    name: str

    def create_construct_definition(self) -> dict:
        return {
            "construct": "dirpath",
            "name": self.name,
            "path": self.path,
        }


@dataclass
class FilePath(CompositeResource, SourceInterface, Deployable):
    path: str
    name: Optional[str]

    def create_construct_definition(self) -> dict:
        return {
            "construct": "filepath",
            "name": self.name,
            "path": self.path,
        }


@dataclass
class GitHubRepo(CompositeResource, SourceInterface, Deployable):
    repo: str
    branch: str

    def create_construct_definition(self) -> dict:
        return {
            "construct": "githubrepo",
            "name": self.name,
            "repository": self.repo,
            "branch": self.branch,
        }


class BuilderInterface(ABC):
    builderType: str

    @abstractmethod
    def __init__(self, builder):
        pass


@dataclass
class BuildkitBuilder(CompositeResource, BuilderInterface, Deployable):
    builder_type = "buildkit"

    def create_construct_definition(self) -> dict:
        return {"construct": "buildkit", "name": self.name}


class RegistryInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, builder):
        pass


@dataclass
class Registry(CompositeResource, RegistryInterface, Deployable):

    def create_construct_definition(self):
        return {"construct": "ecr"}


@dataclass
class ContainerBuilder(CompositeResource, Deployable):
    asset: Asset
    builder: BuilderInterface
    registry: RegistryInterface

    def create_construct_definition(self):
        return {
            "construct": "codebuild",
            "asset": self.asset._get_ref(),
            "builder": self.builder._get_ref(),
            "registry": self.registry._get_ref(),
        }

    def build(self, build_context=None):
        if self.mode == "delete":
            return

        return self.scope.execute_action(
            self.name,
            "build",
            {
                "build_context": build_context
                if build_context is not None
                else self.name
            },
        )


class PortMappings(BaseModel):
    containerPort: int
    hostPort: int


@dataclass
class Container(CompositeResource, Deployable):
    source: Registry
    tag: str
    startCommand: str = None
    portMappings: List[PortMappings] = None

    def create_construct_definition(self) -> dict:
        return {
            "construct": "container",
            "registry": self.source._get_ref(),
            "tag": self.tag,
            "startCommand": self.startCommand.split(" ")
            if self.startCommand is not None
            else None,
            "portMappings": [mapping.model_dump() for mapping in self.portMappings]
            if self.portMappings is not None
            else None,
        }


@dataclass
class Service(CompositeResource):
    name: str
    container: Container
    environmentVariables: Dict[str, str] | None = None


def env_vars_dict_to_str(env_vars: Dict[str, str]):
    return "\n".join([f"{k}={v}" for k, v in env_vars.items()])


@dataclass
class Cluster(CompositeResource, Deployable):
    name: str
    services: List[Service]

    def log(self, path=""):
        if self.mode == "delete":
            return
        return self.scope.get_logs(self.name, path)

    def create_construct_definition(self) -> dict:
        return {
            "construct": "cluster",
            "name": self.name,
            "services": [
                {
                    "name": s.name,
                    "container": s.container._get_ref(),
                    "environment_variables": env_vars_dict_to_str(
                        s.environmentVariables
                    )
                    if s.environmentVariables
                    else "",
                }
                for s in self.services
            ],
        }


class HostInterface(ABC):
    name: str

    @abstractmethod
    def __init__(self, builder):
        pass


class Ingress(BaseModel):
    fromPort: int
    toPort: int
    protocol: str
    cidrIp: List[str]


class Egress(BaseModel):
    fromPort: int
    toPort: int
    protocol: str
    cidrIp: List[str]


@dataclass
class SecurityGroup(CompositeResource, Deployable):
    name: str
    ingresses: List[Ingress] = None
    egresses: List[Egress] = None

    def create_construct_definition(self) -> dict:
        return {
            "construct": "securitygroup",
            "ingresses": [{
                "fromPort": str(ingress.fromPort),
                "toPort": str(ingress.toPort),
                "protocol": ingress.protocol,
                "cidrIp": ingress.cidrIp,
            } for ingress in self.ingresses],
            "egresses": [{
                "fromPort": str(egress.fromPort),
                "toPort": str(egress.toPort),
                "protocol": egress.protocol,
                "cidrIp": egress.cidrIp,
            } for egress in self.egresses],
        }


@dataclass
class Instance(CompositeResource, Deployable):
    name: str
    security_groups: List[SecurityGroup]
    instance_type: str
    path_to_key: str | None = None
    ssh: bool = True

    def pre_resolve(self):
        if self.ssh:
            works = False
            for sg in self.security_groups:
                if (
                    Ingress(
                        protocol="tcp",
                        fromPort=22,
                        toPort=22,
                        cidrIp=["0.0.0.0/0"],
                    )
                    in sg.ingresses
                ):
                    works = True
                    break
            if not works:
                self.security_groups[0].ingresses.append(
                    Ingress(
                        protocol="tcp",
                        fromPort=22,
                        toPort=22,
                        cidrIp=["0.0.0.0/0"],
                    )
                )

    def create_construct_definition(self) -> dict:
        return {
            "construct": "instance",
            "securityGroups": [sg._get_ref() for sg in self.security_groups],
            "instance_type": self.instance_type,
        }

    def run_command(self, command: str):
        if self.mode == "delete":
            return
        import os
        import sys

        import paramiko

        # Function to get default SSH key path based on the operating system
        def get_default_ssh_key_path():
            home = os.path.expanduser("~")
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                # Default path for Linux and macOS
                return os.path.join(home, ".ssh", "id_rsa")
            elif sys.platform.startswith("win32"):
                # Default path for Windows
                return os.path.join(home, ".ssh", "id_rsa")
            else:
                raise ValueError("Unsupported operating system")

        INSTANCE_USER = "ubuntu"  # e.g., 'ec2-user' or 'ubuntu'

        if not self.path_to_key:
            # Prompt user for SSH key path or use default
            self.path_to_key = get_default_ssh_key_path()

        # Read your public key
        public_key_path = self.path_to_key + ".pub"
        with open(public_key_path, "r") as key_file:
            public_key = key_file.read().strip()

        try:
            self.scope.execute_action(
                self.name, "send_public_key", {"public_key": public_key}
            )
            print("Public key sent successfully.")
        except Exception as e:
            print(f"Failed to send public key: {e}")

        # Connect to the instance using Paramiko
        key = paramiko.RSAKey.from_private_key_file(self.path_to_key)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=self.state[self.name]["values"]["public_ip"],
                username=INSTANCE_USER,
                pkey=key,
            )
            print("SSH connection established.")

            _stdin, _stdout, _stderr = ssh_client.exec_command(command)
            _stdin.close()

        except Exception as e:
            print(self.state[self.name]["values"])
            print(f"SSH connection failed: {e}")
        finally:
            ssh_client.close()
            print("SSH connection closed.")

        # return command_results

        return {
            "command": command,
            "stdout": _stdout.read().decode(),
            "stderr": _stderr.read().decode(),
        }

    def run_commands(self, commands: List[str]):
        if self.mode == "delete":
            return

        import os
        import sys

        import paramiko

        # Function to get default SSH key path based on the operating system
        def get_default_ssh_key_path():
            home = os.path.expanduser("~")
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                # Default path for Linux and macOS
                return os.path.join(home, ".ssh", "id_rsa")
            elif sys.platform.startswith("win32"):
                # Default path for Windows
                return os.path.join(home, ".ssh", "id_rsa")
            else:
                raise ValueError("Unsupported operating system")

        INSTANCE_USER = "ubuntu"  # e.g., 'ec2-user' or 'ubuntu'

        if not self.path_to_key:
            # Prompt user for SSH key path or use default
            self.path_to_key = get_default_ssh_key_path()

        # Read your public key
        public_key_path = self.path_to_key + ".pub"
        with open(public_key_path, "r") as key_file:
            public_key = key_file.read().strip()

        try:
            self.scope.execute_action(
                self.name, "send_public_key", {"public_key": public_key}
            )
            print("Public key sent successfully.")
        except Exception as e:
            print(f"Failed to send public key: {e}")

        # Connect to the instance using Paramiko
        key = paramiko.RSAKey.from_private_key_file(self.path_to_key)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=self.state[self.name]["values"]["public_ip"],
                username=INSTANCE_USER,
                pkey=key,
            )
            print("SSH connection established.")

            for command in commands:
                _stdin, _stdout, _stderr = ssh_client.exec_command(command)
                yield {
                    "command": command,
                    "stdout": _stdout.read().decode(),
                    "stderr": _stderr.read().decode(),
                }
                _stdin.close()

        except Exception as e:
            print(self.state[self.name]["values"])
            print(f"SSH connection failed: {e}")
        finally:
            ssh_client.close()
            print("SSH connection closed.")


class DockerEnvironment(CompositeResource):
    name: str
    host: Instance
    containers: List[Container]

    def post_resolve(self):
        self.host.run_commands(["sudo apt update", "sudo apt install -y docker.io"])
        self.ssh_host = self.host.state[self.host.name]["values"]["public_ip"]


@dataclass
class LambdaLayer(CompositeResource, Deployable):
    name: str
    asset: Asset
    runtimes: List[str] | None = None

    def create_construct_definition(self) -> dict:
        return {
            "construct": "lambda_layer",
            "name": self.name,
            "asset": self.asset._get_ref(),
            "runtimes": self.runtimes,
        }


@dataclass
class LambdaFunction(CompositeResource, Deployable):
    function_name: str
    asset: Asset
    runtime: str
    handler: str
    timeout: int
    role: str
    environment: Dict[str, str] | None = None
    layers: List[LambdaLayer] | None = None

    def create_construct_definition(self):
        return {
            "construct": "lambda",
            "name": self.function_name,
            "asset": self.asset._get_ref(),
            "role": self.role,
            "runtime": self.runtime,
            "handler": self.handler,
            "timeout": self.timeout,
            "environment": self.environment,
            "layers": [layer._get_ref() for layer in self.layers]
            if self.layers
            else None,
        }


class Queue(CompositeResource, Deployable):
    name: str
    scope: HangarScope
    type: Literal["fifo"] | Literal["standard"]

    def create_construct_definition(self) -> dict:
        return {
            "construct": "queue",
            "name": self.name,
            "config": {
                "type": self.type,
            },
        }

    def send_message(self, message: str):
        if self.mode == "delete":
            return
        self.scope.execute_action(self.name, "send_message", {"message": message})

    def receive_message(self):
        if self.mode == "delete":
            return
        return self.scope.execute_action(self.name, "receive_message", {})

    def delete_message(self, receipt_handle: str):
        if self.mode == "delete":
            return
        return self.scope.execute_action(
            self.name, "delete_message", {"receipt_handle": receipt_handle}
        )

    def purge_queue(self):
        if self.mode == "delete":
            return
        return self.scope.execute_action(self.name, "purge_queue", {})
