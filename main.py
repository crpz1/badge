import os
from sanic import Sanic, json
from sanic.response import file, text, empty, JSONResponse
from sanic.request import Request, File
import asyncio
import aiofiles
from aiofiles.os import scandir
from os import DirEntry, remove
from PIL import Image

import buttons

try:
    from inky.auto import auto as Inky
except:
    from inky.mock import InkyMockImpression as Inky

app = Sanic(name="badge")
mode = "image"
current_image: str = None

def button_press(button):
    if button == 3:
        import imagedraw

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
    mode = "image"
    current_image = req.json["image"]
    display = Inky()
    image = Image.open("." + req.json["image"])
    resizedimage = image.resize(display.resolution)
    display.set_image(resizedimage, saturation=1)
    display.show()
    try: 
        display.wait_for_window_close()
    except:
        pass
    return text("done")

@app.get("/status")
async def status(req: Request):
    res: JSONResponse = json({"currentDisplay": mode}, headers={"Access-Control-Allow-Origin": "*"})
    if mode == "image": 
        res.append({"displayData": {"image": current_image}})
    return res

app.static("/uploads", "./uploads", name="uploads")

@app.delete("/uploads/<filename>")
async def delete_image(req: Request, filename: str):
    try:
        remove("./uploads/" + filename)
        return text("done", headers={"Access-Control-Allow-Origin": "*"})
    except FileNotFoundError as e:
        return empty(status=404)

@app.get("/uploads/<filename>")
async def get_image(req: Request, filename: str):
    try:
        return await file("./uploads/" + filename)
    except FileNotFoundError as e:
        return empty(status=404)

@app.options("/uploads/<filename>")
async def fuck_cors(req: Request, filename: str):
    return empty(headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", "Origin": "http://localhost:8000"})

app.static("/", "./dist", index="index.html")

async def main():
    # inky init
    if os.name != "nt":
        buttons.init(button_press)
    app.run(debug=True, host="0.0.0.0")
    ...

if __name__ == "__main__":
    asyncio.run(main())