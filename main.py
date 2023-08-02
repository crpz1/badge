from sanic import Sanic, json
from sanic.response import file, text, empty, JSONResponse
from sanic.request import Request, File
import asyncio
import aiofiles
from aiofiles.os import scandir, remove
from os import DirEntry
from inky.mock import InkyMockImpression as Inky
from PIL import Image

app = Sanic(name="badge");

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
@app.delete("/uploads/<file>")
async def delete_image(req: Request, file: str):
    try:
        await remove("./uploads/" + file)
    except FileNotFoundError as e:
        raise e
    return text("done", headers={"Access-Control-Allow-Origin": "*"})

@app.get("/uploads/<filename>")
async def get_image(req: Request, filename: str):
    return await file("./uploads/" + filename)
@app.options("/uploads/<filename>")
async def fuck_cors(req: Request, filename: str):
    return empty(headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", "Origin": "http://localhost:8000"})

app.static("/", "./vue/dist", index="index.html")

async def main():
    # inky init
    app.run(debug=True, host="0.0.0.0")
    ...

if __name__ == "__main__":
    asyncio.run(main())