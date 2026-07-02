from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os

app = Flask(__name__)

FONT_PATH = None
fonts = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
for f in fonts:
    try:
        ImageFont.truetype(f, 60)
        FONT_PATH = f
        break
    except:
        pass


def create_caution_image(text: str):
    img = Image.new('RGB', (512, 512), '#FFD700')
    draw = ImageDraw.Draw(img)
    
    # Yellow triangle with black border
    draw.polygon([(256, 30), (482, 482), (30, 482)], fill='#FFD700', outline='black', width=8)
    
    # Exclamation mark
    font = ImageFont.truetype(FONT_PATH, 120) if FONT_PATH else ImageFont.load_default()
    draw.text((256, 220), '!', font=font, fill='black', anchor='mm')
    
    # Text below triangle
    size = 50 if len(text) <= 5 else 40 if len(text) <= 10 else 30 if len(text) <= 20 else 24
    text_font = ImageFont.truetype(FONT_PATH, size) if FONT_PATH else ImageFont.load_default()
    wrapped = textwrap.fill(text, width=20 if size <= 30 else 15)
    
    y = 400
    for line in wrapped.split('\n'):
        draw.text(((512 - len(line) * size * 0.5) // 2, y), line, font=text_font, fill='black')
        y += size + 5
    
    return img


@app.route('/v2/caution')
def caution():
    text = request.args.get('text', 'CAUTION')[:100]
    img = create_caution_image(text)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Caution API running'}


@app.route('/')
def index():
    return '<h1>Caution API</h1><p>Use: <code>/v2/caution?text=YourText</code></p>'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
