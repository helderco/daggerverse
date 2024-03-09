"""Experimental Python codegen using the codegen module

The goal is to ultimately generate the Python SDK client code, but for now,
it's just a proof of concept, to explore the viability of the codegen module.

There's only two functions. Both return the list of object type names, but
one is concurrent and the other is not. The concurrent version is more
performant but much more verbose and not enough.
"""
import anyio
from dagger import dag, function, object_type


@object_type
class PythonCodegen:
    """Functions that use introspection from the codegen module"""

    @function
    async def objects(self) -> list[str]:
        """Get all object type names concurrently"""
        objs = await dag.codegen().introspect().objects()

        # preserve order
        n = [""] * len(objs)

        async def _name(i, obj):
            n[i] = await obj.name()

        # request concurrently
        async with anyio.create_task_group() as tg:
            for i, obj in enumerate(objs):
                tg.start_soon(_name, i, obj)

        return n

    @function
    async def objects_sync(self) -> list[str]:
        """Simpler but less performant version of the objects function"""
        objs = await dag.codegen().introspect().objects()
        return [await obj.name() for obj in objs]
