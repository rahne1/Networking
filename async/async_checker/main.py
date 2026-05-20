import asyncio, httpx


async def check_username(session, username: str, semaphore):
    async with semaphore:
        res = await session.get(f"https://api.github.com/users/{username}")
        if res.status_code == 200:
            return (username, True)
        if res.status_code == 404:
            return (username, False)
        else:
            return (username, res.status_code)


async def main():
    async with httpx.AsyncClient() as client:
        sem = asyncio.Semaphore(10)
        usernames = [
            "dragon",
            "killer",
            "pen",
            "nerd",
            "geekatron901010",
            "trolfacedaf",
        ]
        results = await asyncio.gather(
            *[check_username(client, u, sem) for u in usernames]
        )
        for r in results:
            print(r)


if __name__ == "__main__":
    asyncio.run(main())
