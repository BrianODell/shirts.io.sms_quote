import textwrap

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

def put_message_on_shirt(msg, f):
    x_offset = 125
    y_rows = [125, 160, 195, 230, 265]  # y coordinate for each line
    width = 350
    max_line_length = 11 # number of characters on a line
    text_color = (0,0,0)

    #font = ImageFont.truetype("libresansserifssk.ttf", 40)
    font = ImageFont.truetype("SourceCodePro-Bold.otf", 36)
    img = Image.open(f)
    draw = ImageDraw.Draw(img)

    lines = textwrap.wrap(msg, max_line_length)
    for row, line in enumerate(lines):
        if row < len(y_rows):
            y = y_rows[row]
            w, h = draw.textsize(line, font)
            _x = x_offset + (width-w)/2
            draw.text((_x, y), line, text_color, font=font)
        else:
            print "Message too long, not printing: '%s'" % (line)

    img.save('sample-out.jpg')


if __name__ == '__main__':
    # simple test
    import requests
    from StringIO import StringIO
    from run import get_tshirt_image_url
    from sys import argv

    image_url = get_tshirt_image_url('Red')
    r = requests.get(image_url)
    f = StringIO(r.content)
    f.seek(0)
    put_message_on_shirt(argv[1], f)

