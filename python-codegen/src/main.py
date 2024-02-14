import anyio

from dagger import dag, function, object_type

@object_type
class PythonCodegen:
    @function
    async def objects(self) -> list[str]:
        """Get the name of all object types"""
        objs = await dag.codegen().introspect().objects()

        n = [""] * len(objs)
        async def _name(i, obj):
            n[i] = await obj.name()

        async with anyio.create_task_group() as tg:
            for i, obj in enumerate(objs):
                tg.start_soon(_name, i, obj)

        return n

    @function
    async def object_names(self) -> list[str]:
        """Simpler but less performant version of objects"""
        objs = await dag.codegen().introspect().objects()
        return [await obj.name() for obj in objs]
