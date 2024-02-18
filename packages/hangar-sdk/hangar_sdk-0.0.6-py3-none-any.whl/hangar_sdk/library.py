import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

from rich import print
from rich.live import Live
from rich.tree import Tree

from .base import HangarScope
from .utils import print_status


class Config:
    mode = "create"


class HangarManager:
    objects = []

    @staticmethod
    def add(obj):
        HangarManager.objects.append(obj)

    @staticmethod
    def delete_objects():
        while HangarManager.objects:
            obj = HangarManager.objects.pop()
            del obj
            print("Object deleted.")


@dataclass(kw_only=True)
class Resource(ABC):
    name: str
    _resolved: bool = False

    def __post_init__(self):
        HangarManager.add(self)
        self.mode = Config.mode

    async def deploy(self):
        await self._resolve()

    def _resolve(self, parent=None):
        pass


class Deployable:
    @abstractmethod
    def create_construct_definition(self) -> dict:
        pass


@dataclass(kw_only=True)
class CompositeResource(Resource, ABC):
    scope: HangarScope
    name: str
    mode: str = None
    _changed: bool = False
    _job_id: Optional[str] = None
    _resources: List[Resource] = field(default_factory=list)
    _dependencies: List[Resource] = field(default_factory=list)
    _parents: List[Resource] = field(default_factory=list)

    def __post_init__(self):
        HangarManager.add(self)
        self.mode = Config.mode
        self.scope.resources[self.name] = self
        
        for f in self.__dict__.values():
            if isinstance(f, CompositeResource):
                self._depends_on(f)

            elif isinstance(f, list):
                for item in f:
                    if isinstance(item, CompositeResource):
                        self._depends_on(item)

    def _depended_on_by(self, resource: Resource):
        resource._dependencies.append(self)
        self._parents.append(resource)

    def _depends_on(self, resource: Resource):
        self._dependencies.append(resource)
        resource._parents.append(self)

    def _get_ref(self):
        return {"!REF": True, "resourceId": self.name}

    def pre_resolve(self):
        pass

    def post_resolve(self):
        pass

    async def _resolveDependencies(self):
        for dependency in self._dependencies:
            await dependency._resolve(self)

    async def _resolveDependedOnBy(self):
        for dependency in self._parents:
            await dependency._resolve(self)

    def _create_full_construct_definition(self):
        return {
            "config": {**self.create_construct_definition(), "name": self.name},
            "resourceId": self.name,
            "parents": [parent.name for parent in self._parents]
        }

    async def _resolve(self, parent: Optional[Resource] = None):
        if self._resolved:
            return

        if self.mode == "delete":
            await self._resolveDependedOnBy()
            self.scope.delete_resource(self.name)
            self._resolved = True
            return
        print("Resolving", self.name)
        await self._resolveDependencies()
        
        to_change = False
        for dependency in self._dependencies:
            if dependency._changed:
                to_change = True

        self.pre_resolve()

        if not self._resolved:
            if isinstance(self, Deployable):
                job_id = self.scope.add_construct(
                    self._create_full_construct_definition(),
                    force_change=to_change,
                )

                self._job_id = job_id

                await self.poll_status()

            self._resolved = True

        self.post_resolve()

    def delete(self):
        self.scope.delete_resource(self.name)

    async def poll_status(self):
        if self._job_id is None:
            raise Exception("No job id")

        response = None

        with Live(print_status(self.name, None)[0], refresh_per_second=4) as live:
            while True:
                if self._job_id == "no-change":
                    tree = Tree(self.name)
                    tree.add("No change")
                    live.update(tree)
                    self._changed = False
                    break
                self._changed = True

                response = self.scope.get_status(self._job_id)
                # print(response)
                await asyncio.sleep(1)

                if response.status_code != 200:
                    raise Exception(response.text)

                status = response.json()
                render, _, errors = print_status(self.name, status)
                live.update(render)

                if errors and len(errors) > 0:
                    raise Exception(f"Errors occurred: {errors}")

                if response.json() and response.json()["completed"] is True:
                    break

        return response.json() if response else None

    @property
    def state(self):
        return self.scope.get_state(self.name)
