from flask import Flask, request, send_file, make_response
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os

app = Flask(__name__)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def create_caution_image(text: str):
    img = Image.new('RGB', (512, 512), '#FFD700')
    draw = ImageDraw.Draw(img)
    draw.polygon([(256, 30), (482, 482), (30, 482)], fill='#FFD700', outline='black', width=8)

    font = ImageFont.truetype(FONT_PATH, 120)
    draw.text((256, 220), '!', font=font, fill='black', anchor='mm')

    size = 50 if len(text) <= 5 else 40 if len(text) <= 10 else 30 if len(text) <= 20 else 24
    text_font = ImageFont.truetype(FONT_PATH, size)
    wrapped = textwrap.fill(text, width=20 if size <= 30 else 15)

    y = 400
    for line in wrapped.split('\n'):
        bbox = draw.textbbox((0,0), line, font=text_font)
        w = bbox[2] - bbox[0]
        draw.text(((512 - w) // 2, y), line, font=text_font, fill='black')
        y += size + 5
    return img

@app.route('/v2/caution')
def caution():
    text = request.args.get('text', 'CAUTION')[:100]
    img = create_caution_image(text)
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)

    response = make_response(buf.getvalue())
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'inline', filename='caution.png')
    response.headers.set('Cache-Control', 'public, max-age=3600')
    return response

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
