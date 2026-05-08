import webbrowser
import os
import tempfile

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>AI Voice Speaker</title>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Space+Mono&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0a0a0f;
      --surface: #13131a;
      --accent: #7fffb2;
      --accent2: #ff6ef7;
      --text: #e8e8f0;
      --muted: #555566;
      --border: #2a2a3a;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Syne', sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      overflow: hidden;
    }

    /* Animated background blobs */
    body::before, body::after {
      content: '';
      position: fixed;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.18;
      pointer-events: none;
      animation: drift 8s ease-in-out infinite alternate;
    }
    body::before {
      width: 420px; height: 420px;
      background: var(--accent);
      top: -100px; left: -100px;
    }
    body::after {
      width: 340px; height: 340px;
      background: var(--accent2);
      bottom: -80px; right: -80px;
      animation-delay: -4s;
    }
    @keyframes drift {
      from { transform: translate(0,0) scale(1); }
      to   { transform: translate(40px, 30px) scale(1.1); }
    }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 48px 40px 40px;
      width: 100%;
      max-width: 520px;
      position: relative;
      z-index: 1;
      box-shadow: 0 0 60px #7fffb220, 0 2px 40px #0008;
    }

    .badge {
      display: inline-block;
      font-family: 'Space Mono', monospace;
      font-size: 10px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: var(--accent);
      background: #7fffb215;
      border: 1px solid #7fffb240;
      border-radius: 100px;
      padding: 4px 14px;
      margin-bottom: 20px;
    }

    h1 {
      font-size: 2.4rem;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 8px;
      background: linear-gradient(135deg, var(--text) 40%, var(--accent));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .subtitle {
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 32px;
      font-family: 'Space Mono', monospace;
    }

    textarea {
      width: 100%;
      background: #0a0a0f;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px;
      color: var(--text);
      font-family: 'Space Mono', monospace;
      font-size: 0.9rem;
      resize: vertical;
      min-height: 120px;
      outline: none;
      transition: border-color 0.2s;
      line-height: 1.6;
    }
    textarea:focus { border-color: var(--accent); }
    textarea::placeholder { color: var(--muted); }

    .controls {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin: 18px 0;
    }

    .control-group label {
      display: block;
      font-size: 10px;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--muted);
      font-family: 'Space Mono', monospace;
      margin-bottom: 8px;
    }

    input[type=range] {
      width: 100%;
      accent-color: var(--accent);
      cursor: pointer;
    }

    select {
      width: 100%;
      background: #0a0a0f;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 14px;
      color: var(--text);
      font-family: 'Space Mono', monospace;
      font-size: 0.8rem;
      outline: none;
      cursor: pointer;
      appearance: none;
      transition: border-color 0.2s;
    }
    select:focus { border-color: var(--accent); }

    .btn-row { display: flex; gap: 12px; margin-top: 24px; }

    button {
      flex: 1;
      padding: 16px;
      border-radius: 14px;
      border: none;
      font-family: 'Syne', sans-serif;
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.18s;
      letter-spacing: 0.5px;
    }

    .btn-speak {
      background: var(--accent);
      color: #0a0a0f;
    }
    .btn-speak:hover { transform: translateY(-2px); box-shadow: 0 8px 30px #7fffb240; }
    .btn-speak:active { transform: translateY(0); }
    .btn-speak:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }

    .btn-stop {
      background: transparent;
      color: var(--accent2);
      border: 1px solid var(--accent2);
    }
    .btn-stop:hover { background: #ff6ef715; }

    /* Waveform visualizer */
    .visualizer {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      height: 48px;
      margin: 20px 0 0;
    }
    .bar {
      width: 4px;
      border-radius: 4px;
      background: var(--accent);
      opacity: 0.3;
      transition: height 0.1s ease, opacity 0.1s;
      height: 6px;
    }
    .speaking .bar {
      opacity: 1;
      animation: wave 0.8s ease-in-out infinite alternate;
    }
    .bar:nth-child(1)  { animation-delay: 0.0s; }
    .bar:nth-child(2)  { animation-delay: 0.05s; }
    .bar:nth-child(3)  { animation-delay: 0.1s; }
    .bar:nth-child(4)  { animation-delay: 0.15s; }
    .bar:nth-child(5)  { animation-delay: 0.2s; }
    .bar:nth-child(6)  { animation-delay: 0.25s; }
    .bar:nth-child(7)  { animation-delay: 0.3s; }
    .bar:nth-child(8)  { animation-delay: 0.35s; }
    .bar:nth-child(9)  { animation-delay: 0.4s; }
    .bar:nth-child(10) { animation-delay: 0.45s; }
    .bar:nth-child(11) { animation-delay: 0.4s; }
    .bar:nth-child(12) { animation-delay: 0.35s; }
    .bar:nth-child(13) { animation-delay: 0.3s; }
    .bar:nth-child(14) { animation-delay: 0.25s; }
    .bar:nth-child(15) { animation-delay: 0.2s; }

    @keyframes wave {
      from { height: 6px; }
      to   { height: 36px; }
    }

    .status {
      text-align: center;
      font-family: 'Space Mono', monospace;
      font-size: 0.75rem;
      color: var(--muted);
      margin-top: 8px;
      min-height: 18px;
      transition: color 0.2s;
    }
    .status.active { color: var(--accent); }
  </style>
</head>
<body>
<div class="card">
  <div class="badge">⚡ No Install Required</div>
  <h1>AI Voice<br>Speaker</h1>
  <p class="subtitle">// browser-powered text-to-speech</p>

  <textarea id="textInput" placeholder="Type anything here and I'll say it out loud...">Hello! I am your AI voice. Type anything and I will speak it for you!</textarea>

  <div class="controls">
    <div class="control-group">
      <label>Speed — <span id="rateVal">1.0</span>x</label>
      <input type="range" id="rate" min="0.5" max="2" step="0.1" value="1.0"
             oninput="document.getElementById('rateVal').textContent=this.value">
    </div>
    <div class="control-group">
      <label>Pitch — <span id="pitchVal">1.0</span></label>
      <input type="range" id="pitch" min="0.5" max="2" step="0.1" value="1.0"
             oninput="document.getElementById('pitchVal').textContent=this.value">
    </div>
    <div class="control-group" style="grid-column:1/-1">
      <label>Voice</label>
      <select id="voiceSelect"></select>
    </div>
  </div>

  <div class="btn-row">
    <button class="btn-speak" id="speakBtn" onclick="speakText()">▶ Speak</button>
    <button class="btn-stop" onclick="stopSpeech()">■ Stop</button>
  </div>

  <div class="visualizer" id="viz">
    <div class="bar"></div><div class="bar"></div><div class="bar"></div>
    <div class="bar"></div><div class="bar"></div><div class="bar"></div>
    <div class="bar"></div><div class="bar"></div><div class="bar"></div>
    <div class="bar"></div><div class="bar"></div><div class="bar"></div>
    <div class="bar"></div><div class="bar"></div><div class="bar"></div>
  </div>
  <div class="status" id="status">Ready to speak</div>
</div>

<script>
  const synth = window.speechSynthesis;
  let voices = [];

  function loadVoices() {
    voices = synth.getVoices();
    const sel = document.getElementById('voiceSelect');
    sel.innerHTML = '';
    if (voices.length === 0) {
      sel.innerHTML = '<option>Loading voices...</option>';
      return;
    }
    voices.forEach((v, i) => {
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = v.name + ' (' + v.lang + ')';
      sel.appendChild(opt);
    });
  }

  loadVoices();
  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = loadVoices;
  }

  function speakText() {
    const text = document.getElementById('textInput').value.trim();
    if (!text) return;
    synth.cancel();

    const utt = new SpeechSynthesisUtterance(text);
    utt.rate  = parseFloat(document.getElementById('rate').value);
    utt.pitch = parseFloat(document.getElementById('pitch').value);

    const vi = document.getElementById('voiceSelect').value;
    if (voices[vi]) utt.voice = voices[vi];

    utt.onstart = () => {
      document.getElementById('viz').classList.add('speaking');
      document.getElementById('status').textContent = 'Speaking...';
      document.getElementById('status').classList.add('active');
      document.getElementById('speakBtn').disabled = true;
    };
    utt.onend = utt.onerror = () => {
      document.getElementById('viz').classList.remove('speaking');
      document.getElementById('status').textContent = 'Done!';
      document.getElementById('status').classList.remove('active');
      document.getElementById('speakBtn').disabled = false;
    };

    synth.speak(utt);
  }

  function stopSpeech() {
    synth.cancel();
    document.getElementById('viz').classList.remove('speaking');
    document.getElementById('status').textContent = 'Stopped.';
    document.getElementById('status').classList.remove('active');
    document.getElementById('speakBtn').disabled = false;
  }
</script>
</body>
</html>
"""

# Save HTML to a temp file and open in browser
tmp = tempfile.NamedTemporaryFile(
    mode='w',
    suffix='.html',
    delete=False,
    encoding='utf-8'
)
tmp.write(html_content)
tmp.close()


print(f"📁 File saved at: {tmp.name}")
webbrowser.open('file://' + tmp.name)
