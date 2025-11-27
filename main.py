# main.py
import hmac
import hashlib
import asyncio
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime

app = FastAPI()
SECRET = b"lib-secret-key"

async def log_commits(payload):
    repo = payload["repository"]["full_name"]
    commits = payload["commits"]

    for c in commits:
        sha = c["id"]
        msg = c["message"]
        author = c["author"]["name"]
        ts = c["timestamp"]
        url = c["url"]

        print("======== COMMIT ========")
        print("Repo     :", repo)
        print("SHA      :", sha)
        print("Message  :", msg)
        print("Author   :", author)
        print("Time     :", ts)
        print("URL      :", url)
        print("========================")

        # OPTIONAL: log file
        with open("commit_log.txt", "a") as f:
            f.write(f"{datetime.now()} | {repo} | {sha} | {author} | {msg}\n")


@app.post("/github-webhook")
async def github_webhook(req: Request):
    raw = await req.body()
    sig = req.headers.get("X-Hub-Signature-256")

    if not sig:
        raise HTTPException(400, "Missing signature")

    expected = "sha256=" + hmac.new(SECRET, raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        raise HTTPException(400, "Invalid signature")

    payload = await req.json()

    # commit handling async
    asyncio.create_task(log_commits(payload))

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #test