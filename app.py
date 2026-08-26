import streamlit as st
import base64
import os

# ============================================================
# SEN BURAYI DÜZENLE — kodun elle değiştireceğin TEK yeri burasıdır
# ============================================================

# Şarkı dosyasının adı. app.py ile AYNI klasöre bu isimle bir mp3 koy.
AUDIO_FILENAME = "sarki.mp3"

# Ekranda görünecek 1. söz parçası ve zamanı (BURAYI BOŞ BIRAKMA, mutlaka bir metin yaz):
LYRIC_1_TEXT = "Please god you must believe me"
LYRIC_1_START_SEC = 0   # 2:23
LYRIC_1_END_SEC = 2    # 2:25

# Ekranda görünecek 2. söz parçası ve zamanı (BURAYI BOŞ BIRAKMA, mutlaka bir metin yaz):
LYRIC_2_TEXT = "I have searched the universe and find myself in her eyes.."
LYRIC_2_START_SEC = 2   # 2:25
LYRIC_2_END_SEC = 9     # 2:32

# Kalbin içinde 2:32-3:50 arasında görünecek final mesajı (her satır ayrı görünür):
FINAL_MESSAGE = ("Aşk seninle güzel, kalbim seninle huzurlu, ruhum seninle bütün.\n"
                 "İyi ki doğdun kalbimin güneşi, seni çok tane çok seviyorum. ❤️")



# Zamanlama (şarkının 0:00'ından itibaren, saniye):
FINAL_START_SEC = 9   # 2:32
FINAL_END_SEC = 87     # 3:50

# ============================================================
# SAYFA YAPILANDIRMASI (buradan sonrasını değiştirmene gerek yok)
# ============================================================
st.set_page_config(
    page_title="İyi ki Doğdun Sevgilim❤️",
    page_icon="🎂",
    layout="wide"
)

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    .stApp {background: #000;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ŞARKIYI KLASÖRDEN OTOMATİK OKU
# ============================================================
audio_data_uri = ""
audio_path = os.path.join(os.path.dirname(__file__), AUDIO_FILENAME)
if os.path.exists(audio_path):
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_data_uri = f"data:audio/mp3;base64,{b64}"
else:
    st.warning(
        f"⚠️ '{AUDIO_FILENAME}' dosyası app.py ile aynı klasörde bulunamadı. "
        "Şarkı dosyanı bu isimle aynı klasöre koy."
    )

# JS'e güvenli şekilde aktarmak için kaçış (escape) işlemleri
def _escape(text):
    return text.replace("\\", "\\\\").replace("`", "\\`").replace("</", "<\\/")

safe_lyric_1 = _escape(LYRIC_1_TEXT)
safe_lyric_2 = _escape(LYRIC_2_TEXT)

final_message_lines = [line for line in FINAL_MESSAGE.split("\n") if line.strip()]
final_message_html = "".join(
    f"<div class='final-line' style='animation-delay:{0.1 + i * 0.5}s'>{line}</div>"
    for i, line in enumerate(final_message_lines)
)

START_DELAY_MS = 2000       # oynatma butonuna basıldıktan sonra şarkının başlamasına kadar geçecek süre

# ============================================================
# TAM EKRAN SÜRPRİZ: AY-GÜNEŞ SAHNESİ + SÖZLER ARKA PLAN ÜZERİNDE + OYNATMA/DURDURMA BUTONU
# (Sayfa açıldığında otomatik BAŞLAMAZ, sadece butona basınca çalışır)
# ============================================================
surprise_html = f"""
<style>
html, body {{ margin: 0; padding: 0; }}

#surprise-wrap {{
    position: relative;
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Segoe UI', sans-serif;
    overflow: hidden;
}}

.sky-scene {{
    position: absolute;
    inset: 0;
    z-index: 0;
    background: radial-gradient(circle at 50% 40%, #2c1f3d 0%, #1a1230 45%, #0d0a1c 100%);
    overflow: hidden;
}}

.emblem-wrap {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: min(78vmin, 620px);
    height: min(78vmin, 620px);
    z-index: 0;
    opacity: 0.9;
}}

.dim-overlay {{
    position: absolute;
    inset: 0;
    background: rgba(10, 6, 20, 0.25);
    z-index: 1;
}}

.control-wrap {{
    position: absolute;
    left: 50%;
    bottom: 5%;
    transform: translateX(-50%);
    z-index: 5;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}}

#play-btn {{
    position: relative;
    width: 74px;
    height: 74px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.35);
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    cursor: pointer;
    box-shadow:
        0 6px 20px rgba(0,0,0,0.35),
        inset 0 1px 1px rgba(255,255,255,0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease;
}}
#play-btn::before {{
    content: "";
    position: absolute;
    inset: -8px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.25);
    animation: ring-pulse 2.6s ease-out infinite;
}}
@keyframes ring-pulse {{
    0%   {{ transform: scale(0.94); opacity: 0.8; }}
    70%  {{ transform: scale(1.22); opacity: 0; }}
    100% {{ transform: scale(1.22); opacity: 0; }}
}}
#play-btn:hover {{
    transform: scale(1.05);
    background: rgba(255,255,255,0.18);
    box-shadow:
        0 8px 24px rgba(0,0,0,0.4),
        inset 0 1px 1px rgba(255,255,255,0.3);
}}
#play-btn:active {{ transform: scale(0.96); }}
#play-btn svg {{ width: 26px; height: 26px; display: block; }}
#play-btn .icon-play {{ fill: #ffffff; margin-left: 3px; }}
#play-btn .icon-stop {{ fill: #ffffff; display: none; }}
#play-btn.playing {{ background: rgba(214,69,69,0.28); border-color: rgba(214,69,69,0.5); }}
#play-btn.playing .icon-play {{ display: none; }}
#play-btn.playing .icon-stop {{ display: block; }}
#play-btn.playing::before {{ border-color: rgba(214,69,69,0.4); }}

#control-label {{
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.75);
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
    user-select: none;
}}

.lyric-text {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 80vw;
    text-align: center;
    font-weight: 600;
    font-size: 22px;
    color: #ffffff;
    opacity: 0;
    transition: opacity 1.2s ease;
    padding: 0 14px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.55);
    z-index: 4;
}}
.lyric-text.show {{ opacity: 1; }}

.final-message {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 80vw;
    text-align: center;
    opacity: 0;
    transition: opacity 1.5s ease;
    color: #ffffff;
    font-weight: 700;
    z-index: 4;
    text-shadow: 0 2px 10px rgba(0,0,0,0.55);
}}
.final-message.show {{ opacity: 1; }}
.final-line {{
    font-size: 20px;
    line-height: 1.7;
    animation: line-in 0.6s ease forwards;
    opacity: 0;
}}
@keyframes line-in {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
</style>

<div id="surprise-wrap">
    <div class="sky-scene"></div>
    <div class="emblem-wrap">
        <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="darkHalf" cx="35%" cy="35%" r="75%">
                    <stop offset="0%" stop-color="#241a38"/>
                    <stop offset="100%" stop-color="#120c1f"/>
                </radialGradient>
                <radialGradient id="lightHalf" cx="65%" cy="65%" r="75%">
                    <stop offset="0%" stop-color="#f3e6c8"/>
                    <stop offset="100%" stop-color="#d9bd85"/>
                </radialGradient>
            </defs>

            <circle cx="200" cy="200" r="178" fill="none" stroke="#c9a24d" stroke-width="2.5"/>
            <circle cx="200" cy="200" r="168" fill="none" stroke="#c9a24d" stroke-width="1"/>

            <clipPath id="circleClip">
                <circle cx="200" cy="200" r="165"/>
            </clipPath>

            <g clip-path="url(#circleClip)">
                <path d="M200,35 C260,90 140,150 200,200 C260,250 140,310 200,365 L365,365 L365,35 Z" fill="url(#lightHalf)"/>
                <path d="M200,35 C140,90 260,150 200,200 C140,250 260,310 200,365 L35,365 L35,35 Z" fill="url(#darkHalf)"/>

                <path d="M155,90 a48,48 0 1,0 6,92 a58,58 0 1,1 -6,-92 Z" fill="#f3e6c8" opacity="0.95"/>

                <g fill="#f3e6c8">
                    <circle cx="120" cy="150" r="2"/>
                    <circle cx="105" cy="180" r="1.4"/>
                    <circle cx="140" cy="200" r="1.6"/>
                    <circle cx="95" cy="120" r="1.4"/>
                    <circle cx="150" cy="130" r="1.2"/>
                    <circle cx="115" cy="230" r="1.6"/>
                    <path d="M128,105 l3,7 7,1.2 -5.2,5 1.2,7 -6.2,-3.4 -6.2,3.4 1.2,-7 -5.2,-5 7,-1.2 Z"/>
                </g>

                <g transform="translate(255,255)" fill="#120c1f">
                    <circle r="26"/>
                    <g stroke="#120c1f" stroke-width="3">
                        <line x1="0" y1="-42" x2="0" y2="-52"/>
                        <line x1="0" y1="42" x2="0" y2="52"/>
                        <line x1="-42" y1="0" x2="-52" y2="0"/>
                        <line x1="42" y1="0" x2="52" y2="0"/>
                        <line x1="-30" y1="-30" x2="-37" y2="-37"/>
                        <line x1="30" y1="-30" x2="37" y2="-37"/>
                        <line x1="-30" y1="30" x2="-37" y2="37"/>
                        <line x1="30" y1="30" x2="37" y2="37"/>
                    </g>
                </g>
            </g>

            <circle cx="200" cy="200" r="165" fill="none" stroke="#c9a24d" stroke-width="1.2"/>
        </svg>
    </div>
    <div class="dim-overlay"></div>
    <div class="control-wrap">
        <button id="play-btn" aria-label="">
            <svg class="icon-play" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M8 5v14l11-7z"/></svg>
            <svg class="icon-stop" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
        </button>
        <span id="control-label"></span>
    </div>
    <div class="lyric-text" id="lyric-text-1">{safe_lyric_1}</div>
    <div class="lyric-text" id="lyric-text-2">{safe_lyric_2}</div>
    <div class="final-message" id="final-message">{final_message_html}</div>
    <audio id="bg-audio" src="{audio_data_uri}"></audio>
</div>

<script>

const playBtn   = document.getElementById('play-btn');
const controlLabel = document.getElementById('control-label');
const lyricEl1  = document.getElementById('lyric-text-1');
const lyricEl2  = document.getElementById('lyric-text-2');
const finalEl   = document.getElementById('final-message');
const audioEl   = document.getElementById('bg-audio');

const LYRIC1_START = {LYRIC_1_START_SEC};
const LYRIC1_END   = {LYRIC_1_END_SEC};
const LYRIC2_START = {LYRIC_2_START_SEC};
const LYRIC2_END   = {LYRIC_2_END_SEC};
const FINAL_START  = {FINAL_START_SEC};
const FINAL_END    = {FINAL_END_SEC};
const START_DELAY  = {START_DELAY_MS};

let timers = [];
let isPlaying = false;
let lyric1Shown = false;
let lyric2Shown = false;
let finalShown = false;

function clearAllTimers() {{
    timers.forEach(t => clearTimeout(t));
    timers = [];
}}

function onTimeUpdate() {{
    const t = audioEl.currentTime;

    if (t >= LYRIC1_START && t < LYRIC1_END) {{
        if (!lyric1Shown) {{ lyricEl1.classList.add('show'); lyric1Shown = true; }}
    }} else if (lyric1Shown) {{
        lyricEl1.classList.remove('show');
        lyric1Shown = false;
    }}

    if (t >= LYRIC2_START && t < LYRIC2_END) {{
        if (!lyric2Shown) {{ lyricEl2.classList.add('show'); lyric2Shown = true; }}
    }} else if (lyric2Shown) {{
        lyricEl2.classList.remove('show');
        lyric2Shown = false;
    }}

    if (t >= FINAL_START && t < FINAL_END) {{
        if (!finalShown) {{ finalEl.classList.add('show'); finalShown = true; }}
    }} else if (t >= FINAL_END) {{
        stopPlayback();
    }}
}}

function resetVisuals() {{
    lyricEl1.classList.remove('show');
    lyricEl2.classList.remove('show');
    finalEl.classList.remove('show');
    lyric1Shown = false;
    lyric2Shown = false;
    finalShown = false;
}}

function stopPlayback() {{
    clearAllTimers();
    audioEl.removeEventListener('timeupdate', onTimeUpdate);
    audioEl.pause();
    audioEl.currentTime = 0;
    resetVisuals();
    isPlaying = false;
    playBtn.classList.remove('playing');
    controlLabel.textContent = 'Dinle';
}}

function startPlayback() {{
    isPlaying = true;
    playBtn.classList.add('playing');
    controlLabel.textContent = '';

    // Butona basıldıktan kısa bir süre sonra şarkı başlar
    timers.push(setTimeout(() => {{
        if (!isPlaying) return; // bu arada durdurulduysa başlatma
        if (audioEl.src) {{
            audioEl.currentTime = 0;
            audioEl.addEventListener('timeupdate', onTimeUpdate);
            audioEl.play().catch(() => {{}});
        }}

        // Güvenlik ağı: her ihtimale karşı FINAL_END'den birkaç saniye sonra
        // kesin bir durdurma zamanlayıcısı da kur.
        timers.push(setTimeout(() => {{
            if (isPlaying) stopPlayback();
        }}, (FINAL_END + 3) * 1000));

    }}, START_DELAY));
}}

playBtn.addEventListener('click', function() {{
    if (isPlaying) {{
        stopPlayback();
    }} else {{
        startPlayback();
    }}
}});
</script>
"""

st.components.v1.html(surprise_html, height=900, scrolling=False)
