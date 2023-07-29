from sanic import Sanic, json
from sanic.response import file, text, JSONResponse
from sanic.request import Request, File
import asyncio
import aiofiles
from aiofiles.os import scandir
from os import DirEntry
from inky.mock import InkyMockImpression as Inky
from PIL import Image

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

@app.get("/enumerate_images")
async def enumerate_images(req: Request):
    res: JSONResponse = json([], headers={"Access-Control-Allow-Origin": "*"})
    files = await scandir("./uploads")
    file: DirEntry
    for file in files:
        res.append({"path": "/uploads/" + file.name})
    return res

@app.post("/pick_image")
async def pick_image(req: Request):
    display = Inky()
    image = Image.open("." + req.json["image"])
    resizedimage = image.resize(display.resolution)
    display.set_image(resizedimage, saturation=1)
    display.show()
    display.wait_for_window_close()
    return text("done")

app.static("/uploads", "./uploads", name="uploads")
async def main():
    # inky init
    app.run(debug=True, host="0.0.0.0")
    ...

if __name__ == "__main__":
    asyncio.run(main())