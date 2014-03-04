from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def put_message_on_shirt(msg, f):
    x = 10
    y = 10
    text_color = (0,0,0)
    font = ImageFont.truetype("libresansserifssk.ttf", 16)

    img = Image.open(f)
    draw = ImageDraw.Draw(img)
    draw.text((x, y), msg , text_color,font=font)
    img.save('sample-out.jpg')


if __name__ == '__main__':
    # simple test
    import requests
    from StringIO import StringIO
    from run import get_tshirt_image_url

    image_url = get_tshirt_image_url('Red')
    r = requests.get(image_url)
    f = StringIO(r.content)
    f.seek(0)
    put_message_on_shirt("Test", f)

