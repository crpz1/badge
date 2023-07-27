from urllib.request import Request
from sanic import Sanic
from sanic.response import file, text
from sanic.request import Request, File
import asyncio
import aiofiles

app = Sanic(name="badge");

@app.get("/")
async def index(req):
    return await file("./static/index.html")

@app.post("/upload_image")
async def upload_image(req: Request):
    await req.receive_body()
    if (len(req.files) == 0):
        raise NotImplementedError("no files")
    file: File = req.files["file"][0];
    async with aiofiles.open("./uploads/" + file.name, "wb") as f:
        await f.write(file.body)
    return text("done")

async def main():
    # inky init
    app.run(debug=True, host="0.0.0.0")
    ...

if __name__ == "__main__":
    asyncio.run(main())