"""
Pixel Lock — Image Encryption via Pixel Manipulation
A single-file Flask app: Python backend uses Pillow to XOR every pixel
channel with a numeric key (a reversible operation — XOR twice with the
same key returns the original image), frontend lets you upload an image,
set a key, and download the encrypted/decrypted result.

Run:
    pip install flask pillow --break-system-packages
    python pixel_lock_app.py
Then open http://127.0.0.1:5000
"""

import base64
import io
from flask import Flask, request, jsonify, render_template_string
from PIL import Image

app = Flask(__name__)

MAX_KEY = 255


def xor_image(image: Image.Image, key: int) -> Image.Image:
    """XOR every pixel channel with `key`. Applying it twice with the same
    key restores the original image, which is what makes this reversible."""
    image = image.convert("RGB")
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            pixels[x, y] = (r ^ key, g ^ key, b ^ key)
    return image


@app.route("/api/process", methods=["POST"])
def api_process():
    if "image" not in request.files:
        return jsonify({"error": "no image uploaded"}), 400

    file = request.files["image"]
    key_raw = request.form.get("key", "42")
    try:
        key = int(key_raw)
    except ValueError:
        return jsonify({"error": "key must be an integer"}), 400
    if not (0 <= key <= MAX_KEY):
        return jsonify({"error": f"key must be between 0 and {MAX_KEY}"}), 400

    try:
        image = Image.open(file.stream)
    except Exception:
        return jsonify({"error": "could not read image file"}), 400

    result = xor_image(image, key)

    buf = io.BytesIO()
    result.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")

    return jsonify({"image": f"data:image/png;base64,{encoded}", "key": key})


@app.route("/")
def index():
    return render_template_string(PAGE_TEMPLATE)


PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Pixel Lock — Image Encryption</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{
    --ink:#15131c; --ink-2:#1d1a26; --coral:#d97757; --teal:#6fb6a8;
    --bone:#f1ece1; --bone-dim:#a39d97; --line:rgba(241,236,225,0.1);
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html,body{ background:var(--ink); color:var(--bone); font-family:'JetBrains Mono', monospace; min-height:100vh; }
  body{ display:flex; flex-direction:column; align-items:center; padding:5vh 6vw 8vh;
        background-image: radial-gradient(circle at 10% 90%, rgba(111,182,168,0.1), transparent 45%); }
  .wrap{ width:100%; max-width:760px; }
  .eyebrow{ font-size:11px; letter-spacing:0.22em; text-transform:uppercase; color:var(--coral);
            display:flex; align-items:center; gap:10px; margin-bottom:16px; }
  .eyebrow::before{ content:""; width:18px; height:1px; background:var(--coral); display:inline-block; }
  h1{ font-family:'Fraunces', serif; font-weight:700; font-size:clamp(1.9rem, 5vw, 2.8rem); line-height:1.08; margin-bottom:14px; }
  h1 em{ font-style:italic; font-weight:400; color:var(--coral); }
  .sub{ color:var(--bone-dim); font-size:14px; line-height:1.6; max-width:58ch; margin-bottom:40px; }

  .dropzone{
    border:1px dashed var(--line); border-radius:6px; padding:36px 20px; text-align:center;
    cursor:pointer; transition:border-color .2s ease, background .2s ease; margin-bottom:24px;
    background:var(--ink-2);
  }
  .dropzone:hover, .dropzone.dragover{ border-color:var(--coral); background:rgba(217,119,87,0.05); }
  .dropzone p{ color:var(--bone-dim); font-size:13px; }
  .dropzone span{ color:var(--coral); }
  input[type="file"]{ display:none; }

  .key-row{ display:flex; align-items:center; gap:18px; margin-bottom:28px; flex-wrap:wrap; }
  .field-label{ font-size:10px; letter-spacing:0.1em; text-transform:uppercase; color:var(--bone-dim); margin-bottom:8px; display:block; }
  input[type="number"]{
    width:100px; background:var(--ink-2); border:1px solid var(--line); border-radius:4px;
    color:var(--bone); font-family:'JetBrains Mono', monospace; font-size:15px; padding:10px 12px; outline:none;
  }
  input[type="number"]:focus{ border-color:var(--coral); }
  .key-note{ font-size:11px; color:var(--bone-dim); max-width:36ch; }

  .actions{ display:flex; gap:10px; margin-bottom:36px; }
  button{
    background:none; border:1px solid var(--line); color:var(--bone-dim);
    font-family:'JetBrains Mono', monospace; font-size:11px; letter-spacing:0.06em; text-transform:uppercase;
    padding:11px 18px; border-radius:3px; cursor:pointer; transition:all .2s ease;
  }
  button#processBtn:hover{ border-color:var(--coral); color:var(--coral); }
  button#downloadBtn{ display:none; }
  button#downloadBtn:hover{ border-color:var(--teal); color:var(--teal); }
  button:disabled{ opacity:0.4; cursor:not-allowed; }

  .compare{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }
  .compare-panel{ border:1px solid var(--line); border-radius:6px; background:var(--ink-2); padding:14px; }
  .compare-panel h3{ font-size:10px; letter-spacing:0.1em; text-transform:uppercase; color:var(--bone-dim); margin-bottom:10px; font-weight:500; }
  .compare-panel img{ width:100%; border-radius:4px; display:block; }
  .placeholder{ aspect-ratio:1; display:flex; align-items:center; justify-content:center; color:var(--bone-dim); font-size:11px; }

  footer{ margin-top:56px; font-size:10px; letter-spacing:0.1em; text-transform:uppercase; color:var(--bone-dim); opacity:0.5; }

  @media (max-width:560px){ .compare{ grid-template-columns:1fr; } }
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">Task 02 — Pixel Manipulation</div>
  <h1>Lock an image, <em>pixel by pixel.</em></h1>
  <p class="sub">Every pixel's red, green, and blue values get XORed with a key you choose. Run it once to encrypt, run the result through the same key again to decrypt — XOR undoes itself.</p>

  <div class="dropzone" id="dropzone">
    <p>Drop an image here, or <span>click to browse</span></p>
    <input type="file" id="fileInput" accept="image/*" />
  </div>

  <div class="key-row">
    <div>
      <label class="field-label" for="keyInput">Key (0–255)</label>
      <input type="number" id="keyInput" value="42" min="0" max="255" />
    </div>
    <div class="key-note">Use the same key to decrypt as you used to encrypt — that's what makes it reversible.</div>
  </div>

  <div class="actions">
    <button id="processBtn" disabled>Apply key</button>
    <button id="downloadBtn">Download result</button>
  </div>

  <div class="compare">
    <div class="compare-panel">
      <h3>Original</h3>
      <div class="placeholder" id="originalPlaceholder">No image yet</div>
      <img id="originalImg" style="display:none" />
    </div>
    <div class="compare-panel">
      <h3>Result</h3>
      <div class="placeholder" id="resultPlaceholder">Apply a key to see it here</div>
      <img id="resultImg" style="display:none" />
    </div>
  </div>

  <footer>Pixel Lock — a Pixel Manipulation image encryption tool</footer>
</div>

<script>
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const keyInput = document.getElementById('keyInput');
  const processBtn = document.getElementById('processBtn');
  const downloadBtn = document.getElementById('downloadBtn');
  const originalImg = document.getElementById('originalImg');
  const originalPlaceholder = document.getElementById('originalPlaceholder');
  const resultImg = document.getElementById('resultImg');
  const resultPlaceholder = document.getElementById('resultPlaceholder');

  let currentFile = null;

  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if(e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener('change', e => {
    if(e.target.files.length) handleFile(e.target.files[0]);
  });

  function handleFile(file){
    currentFile = file;
    const url = URL.createObjectURL(file);
    originalImg.src = url;
    originalImg.style.display = 'block';
    originalPlaceholder.style.display = 'none';
    processBtn.disabled = false;
    resultImg.style.display = 'none';
    resultPlaceholder.style.display = 'flex';
    resultPlaceholder.textContent = 'Apply a key to see it here';
    downloadBtn.style.display = 'none';
  }

  processBtn.addEventListener('click', async () => {
    if(!currentFile) return;
    processBtn.disabled = true;
    processBtn.textContent = 'Processing…';
    resultPlaceholder.textContent = 'Processing…';

    const formData = new FormData();
    formData.append('image', currentFile);
    formData.append('key', keyInput.value);

    try{
      const res = await fetch('/api/process', { method:'POST', body: formData });
      const data = await res.json();
      if(data.error){
        resultPlaceholder.textContent = data.error;
        resultPlaceholder.style.display = 'flex';
        resultImg.style.display = 'none';
      }else{
        resultImg.src = data.image;
        resultImg.style.display = 'block';
        resultPlaceholder.style.display = 'none';
        downloadBtn.style.display = 'inline-block';
        downloadBtn.dataset.href = data.image;
      }
    }catch(err){
      resultPlaceholder.textContent = 'Server offline — start the Flask app.';
      resultPlaceholder.style.display = 'flex';
    }finally{
      processBtn.disabled = false;
      processBtn.textContent = 'Apply key';
    }
  });

  downloadBtn.addEventListener('click', () => {
    const href = downloadBtn.dataset.href;
    if(!href) return;
    const a = document.createElement('a');
    a.href = href;
    a.download = 'pixel-lock-result.png';
    a.click();
  });
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)