import asyncio, time


async def fun1():
    await asyncio.sleep(1)
    print("done 1")


async def fun2():
    await asyncio.sleep(1)
    print("done 2")


async def main():
    start = time.time()
    await asyncio.gather(fun1(), fun2())
    print(time.time() - start)


asyncio.run(main())
