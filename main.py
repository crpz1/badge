from urllib.request import Request
from sanic import Sanic
from sanic.response import file, text
from sanic.request import Request
import asyncio

app = Sanic(name="badge");

@app.get("/")
async def index(req):
    return await file("./static/index.html")

@app.post("/upload_image")
async def upload_image(req: Request):
    await req.receive_body()
    if (len(req.files) == 0):
        raise NotImplementedError("no files")
    raise NotImplementedError("got files")
    ...

async def main():
    # inky init
    app.run(debug=True)
    ...

if __name__ == "__main__":
    asyncio.run(main())