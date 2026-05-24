import asyncio, httpx, sqlite3


def setup_db():
    conn = sqlite3.connect("usernames.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS results(username TEXT, available BOOLEAN)"
    )
    conn.commit()
    return conn


def get_cached(conn, username: str):
    cursor = conn.cursor()
    cursor.execute("SELECT available FROM results WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result is not None else None


def save_result(conn, username: str, available: bool):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO results (username, available) VALUES (?, ?)", (username, available)
    )
    conn.commit()


async def check_username(conn, session, username: str, semaphore):
    async with semaphore:
        cached = get_cached(conn, username)
        if cached is not None:
            return (username, bool(cached))
        res = await session.get(f"https://api.github.com/users/{username}")
        if res.status_code == 200:
            save_result(conn, username, True)
            return (username, True)
        if res.status_code == 404:
            save_result(conn, username, False)
            return (username, False)
        else:
            return (username, res.status_code)


async def main():
    async with httpx.AsyncClient() as client:
        db = setup_db()
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
            *[check_username(db, client, u, sem) for u in usernames]
        )
        for r in results:
            print(r)
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
