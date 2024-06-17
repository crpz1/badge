#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
import os
import socket
import ngrok
import qrcode
import dotenv

class PlaceholderListener:
    text = ""
    def set(self, a):
        self.text = a
    def url(self):
        return self.text

def wrap(str):
    count = 0
    out_str = ""
    for char in str:
        count += 1
        if count % 64 == 0:
            out_str += "\n"
        out_str += char
    return out_str

try:
    import smbus2 as _
    from inky.auto import auto as Inky
except:
    from inky.mock import InkyMockImpression as Inky

dotenv.load_dotenv()

network_up = False
qr_img = Image.new("RGBA", [1, 1])
listener = PlaceholderListener()

try:
    listener = ngrok.forward(8000, authtoken_from_env=True, domain=os.environ.get("NGROK_DOMAIN"))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    qr.add_data(listener.url())
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
except Exception as e: 
    listener.set(wrap(str(e)))

if os.name != "nt":
    with open("/sys/class/net/wlan0/operstate", "r") as f:
        if f.read() != "down":
            network_up = True
else: 
    network_up = True

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = s.getsockname()[0]
s.close()

display = Inky()

img = Image.new("RGB", display.resolution)
battery = Image.open("./res/battery.png")
wifi_status = Image.open("./res/wifi_connected.png") if network_up else Image.open("./wifi_notconnected.png")
font = ImageFont.truetype("./res/CascadiaCode-Regular.ttf", 16)
draw = ImageDraw.Draw(img)

draw.rectangle((0, 0, display.WIDTH, 40), fill="#222")
draw.text((16, 12), "Status / About", font=font)
img.paste(battery, (display.WIDTH - 32, 10), battery)
img.paste(wifi_status, (display.WIDTH - 64, 10), wifi_status)
img.paste(qr_img, (display.WIDTH - 172, display.HEIGHT - 174), qr_img)
draw.text((16, 52), ip_addr, font=font)
draw.text((16, 74), listener.url(), font=font)

display.set_image(img)
display.show()
display.wait_for_window_close()