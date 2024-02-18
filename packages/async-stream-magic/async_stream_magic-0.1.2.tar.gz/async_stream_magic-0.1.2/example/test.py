import asyncio
from async_stream_magic import Info, State, Source, StreamMagicError, StreamMagic

async def main():
    async with StreamMagic("192.168.178.123") as sm:
        info: Info
        state: State
        sourcelist: list(Source)

        try:
            state = await sm.get_state()
            info = await sm.get_info()
            sourcelist = await sm.get_sources()
        except StreamMagicError as err:
            print(err)

        print(info)
        print(state)
        #print(sourcelist)

asyncio.run(main())