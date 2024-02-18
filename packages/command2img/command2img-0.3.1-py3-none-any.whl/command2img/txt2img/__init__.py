from os.path import join, realpath, dirname
from PIL import Image, ImageDraw, ImageFont
PATH_FONTS = join(dirname(__file__), "fonts")
FONT_FACE_MESLO = join(PATH_FONTS, "meslo.ttf")

def Txt2img(
    text: str,
    margin=10,
    font_face=FONT_FACE_MESLO,
    font_size=28,
    font_encoding="unic",
    backgroud_color=(255, 255, 255),
    backgroud_transparency=255,
    text_fill=(0, 0, 0),
) -> Image:
    font = ImageFont.truetype(font=font_face, size=font_size, encoding=font_encoding)
    w, h = font.getsize_multiline(text)
    img = Image.new("RGBA", (w+2*margin, h+2*margin), backgroud_color)
    img.putalpha(backgroud_transparency)
    ImageDraw.Draw(img).text((margin, margin), text, fill=text_fill, font=font)
    return img
