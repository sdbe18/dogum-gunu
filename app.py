import streamlit as st
import base64

# ============================================================
# SAYFA YAPILANDIRMASI
# ============================================================
st.set_page_config(
    page_title="İyi ki Doğdun Sevgilim! ❤️",
    page_icon="🎂",
    layout="centered"
)

# ============================================================
# AYARLAR (kenar çubuğundan kendi dosyana göre düzenle)
# ============================================================
with st.sidebar:
    st.header("⚙️ Sürpriz Ayarları")
    st.caption(
        "Telif hakkı nedeniyle şarkının ses dosyasını ve sözlerini ben "
        "koyamam. Kendi sahip olduğun mp3'ü ve istediğin sözü buradan "
        "kendin ekle — animasyon bunlarla senkronize çalışacak."
    )
    audio_file = st.file_uploader("🎵 Şarkı dosyasını yükle (mp3)", type=["mp3"])
    lyric_text = st.text_input(
        "💬 Kalbin içinde görünecek söz",
        value="",
        placeholder="Buraya istediğin şarkı sözünü/mesajı yaz..."
    )
    st.divider()
    st.caption("Zamanlamayı kendi şarkı dosyana göre ayarla (saniye):")
    lyric_duration = st.number_input("Sözün ekranda kalma süresi (sn)", min_value=1, value=10)
    final_msg_start = st.number_input(
        "Final mesajının başlayacağı an (gitar solosu bitince, sn)",
        min_value=1, value=45
    )
    final_msg_duration = st.number_input("Final mesajının ekranda kalma süresi (sn)", min_value=1, value=10)

# Ses dosyasını base64'e çevir (yüklendiyse)
audio_data_uri = ""
if audio_file is not None:
    audio_bytes = audio_file.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_data_uri = f"data:audio/mp3;base64,{b64}"

# JS'e güvenli şekilde aktarmak için kaçış (escape) işlemleri
safe_lyric = lyric_text.replace("\\", "\\\\").replace("`", "\\`").replace("</", "<\\/")
final_message_lines = [
    "Aşk seninle güzel kalbim,",
    "Seninle huzurlu ruhum,",
    "Seninle mutlu...",
    "İyi ki doğdun hayatım,",
    "Seni çok ama çok seviyorum. ❤️"
]
final_message_html = "".join(f"<div class='final-line'>{line}</div>" for line in final_message_lines)

HEART_GROW_MS = 2500        # kalp "açılış" animasyonunun süresi
EXTRA_DELAY_MS = 2000       # kalp animasyonu bitince şarkının başlamasına kadar geçecek ek süre
lyric_duration_ms = int(lyric_duration * 1000)
final_msg_start_ms = int(final_msg_start * 1000)
final_msg_duration_ms = int(final_msg_duration * 1000)

# ============================================================
# AÇILIŞ SÜRPRİZİ: MAVİ KALP + OYNATMA BUTONU
# (Sayfa açıldığında otomatik BAŞLAMAZ, sadece butona basınca çalışır)
# ============================================================
surprise_html = f"""
<style>
#surprise-wrap {{
    position: relative;
    width: 100%;
    min-height: 380px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Segoe UI', sans-serif;
    background: radial-gradient(circle at center, #eaf6ff 0%, #ffffff 70%);
    border-radius: 24px;
    overflow: hidden;
}}

.heart {{
    position: relative;
    width: 140px;
    height: 126px;
    margin: 60px auto;
    transition: transform 0.4s ease;
}}
.heart::before,
.heart::after {{
    content: "";
    position: absolute;
    top: 0;
    width: 72px;
    height: 116px;
    background: #7ec8f2;
    border-radius: 72px 72px 0 0;
    box-shadow: 0 0 25px 6px rgba(126,200,242,0.55);
    animation: idle-pulse 2.4s ease-in-out infinite;
}}
.heart::before {{ left: 70px; transform: rotate(-45deg); transform-origin: 0 100%; }}
.heart::after  {{ left: 0;    transform: rotate(45deg);  transform-origin: 100% 100%; }}

@keyframes idle-pulse {{
    0%, 100% {{ filter: brightness(1);   transform: scale(1) rotate(var(--rot, 0deg)); }}
    50%      {{ filter: brightness(1.15); transform: scale(1.04) rotate(var(--rot, 0deg)); }}
}}

.heart.active::before, .heart.active::after {{
    animation: grow-pulse {HEART_GROW_MS}ms ease-in-out forwards, glow-pulse 1.6s ease-in-out infinite 2.5s;
}}
@keyframes grow-pulse {{
    0%   {{ transform: scale(0.85) rotate(var(--rot, 0deg)); filter: brightness(1); }}
    50%  {{ transform: scale(1.25) rotate(var(--rot, 0deg)); filter: brightness(1.3); }}
    100% {{ transform: scale(1.1)  rotate(var(--rot, 0deg)); filter: brightness(1.2); }}
}}
.heart.active::before {{ --rot: -45deg; }}
.heart.active::after  {{ --rot: 45deg; }}
@keyframes glow-pulse {{
    0%, 100% {{ box-shadow: 0 0 25px 6px rgba(126,200,242,0.55); }}
    50%      {{ box-shadow: 0 0 45px 14px rgba(126,200,242,0.85); }}
}}

#play-btn {{
    position: absolute;
    z-index: 5;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: none;
    background: #ffffff;
    color: #4aa8e8;
    font-size: 30px;
    cursor: pointer;
    box-shadow: 0 4px 18px rgba(0,0,0,0.15);
    transition: all 0.25s ease;
}}
#play-btn:hover {{ transform: scale(1.08); box-shadow: 0 6px 22px rgba(0,0,0,0.22); }}
#play-btn.hidden {{ opacity: 0; pointer-events: none; transform: scale(0.6); }}

.lyric-text {{
    position: absolute;
    max-width: 240px;
    text-align: center;
    font-weight: 600;
    font-size: 16px;
    color: #ffffff;
    opacity: 0;
    transition: opacity 1.2s ease;
    padding: 0 12px;
    text-shadow: 0 1px 4px rgba(0,0,0,0.25);
}}
.lyric-text.show {{ opacity: 1; }}

.final-message {{
    position: absolute;
    text-align: center;
    opacity: 0;
    transition: opacity 1.5s ease;
    color: #2b6fa0;
    font-weight: 700;
}}
.final-message.show {{ opacity: 1; }}
.final-line {{
    font-size: 19px;
    line-height: 1.7;
    animation: line-in 0.6s ease forwards;
    opacity: 0;
}}
.final-line:nth-child(1) {{ animation-delay: 0.1s; }}
.final-line:nth-child(2) {{ animation-delay: 0.6s; }}
.final-line:nth-child(3) {{ animation-delay: 1.1s; }}
.final-line:nth-child(4) {{ animation-delay: 1.6s; }}
.final-line:nth-child(5) {{ animation-delay: 2.1s; }}
@keyframes line-in {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

#surprise-wrap.finished .heart {{ transform: scale(1); }}
</style>

<div id="surprise-wrap">
    <button id="play-btn">▶️</button>
    <div class="heart" id="heart"></div>
    <div class="lyric-text" id="lyric-text">{safe_lyric}</div>
    <div class="final-message" id="final-message">{final_message_html}</div>
    <audio id="bg-audio" src="{audio_data_uri}"></audio>
</div>

<script>
const playBtn   = document.getElementById('play-btn');
const heart     = document.getElementById('heart');
const lyricEl   = document.getElementById('lyric-text');
const finalEl   = document.getElementById('final-message');
const audioEl   = document.getElementById('bg-audio');
const wrap      = document.getElementById('surprise-wrap');

let timers = [];
function clearAllTimers() {{
    timers.forEach(t => clearTimeout(t));
    timers = [];
}}

function resetToInitial() {{
    clearAllTimers();
    audioEl.pause();
    audioEl.currentTime = 0;
    heart.classList.remove('active');
    lyricEl.classList.remove('show');
    finalEl.classList.remove('show');
    wrap.classList.remove('finished');
    playBtn.classList.remove('hidden');
}}

playBtn.addEventListener('click', function() {{
    playBtn.classList.add('hidden');
    heart.classList.add('active');

    // Kalp animasyonu bitince + 2 sn sonra şarkı başlar
    const startDelay = {HEART_GROW_MS} + {EXTRA_DELAY_MS};

    timers.push(setTimeout(() => {{
        if (audioEl.src) {{
            audioEl.currentTime = 0;
            audioEl.play().catch(() => {{}});
        }}
        lyricEl.classList.add('show');

        // Söz bir süre sonra kaybolur, gitar solosu (enstrümantal) devam eder
        timers.push(setTimeout(() => {{
            lyricEl.classList.remove('show');
        }}, {lyric_duration_ms}));

        // Solo bitince final mesajı belirir
        timers.push(setTimeout(() => {{
            finalEl.classList.add('show');
            wrap.classList.add('finished');

            // Final mesajı bir süre görünür kalır, sonra sayfa ilk haline döner
            timers.push(setTimeout(() => {{
                resetToInitial();
            }}, {final_msg_duration_ms}));
        }}, {final_msg_start_ms}));

    }}, startDelay));
}});

// Ses dosyası kullanıcı tarafından erkenden biterse de akışı bozmadan devam etsin
audioEl.addEventListener('ended', function() {{
    // ses bitse bile final mesaj zamanlaması yukarıdaki setTimeout ile yönetiliyor
}});
</script>
"""

st.components.v1.html(surprise_html, height=420, scrolling=False)

if audio_file is None:
    st.info("ℹ️ Soldaki menüden kendi mp3 dosyanı yüklersen, oynat butonuna basınca şarkı da çalar.")

st.divider()

# ============================================================
# BAŞLIK VE KARŞILAMA
# ============================================================
st.title("🎉 İyi ki Doğdun Hayatım! ❤️")
st.subheader("Senin için hazırladığım küçük bir sürpriz... ✨")
st.divider()

# ============================================================
# SÜRPRİZ BUTONU VE KONFETİ EFEKTİ
# ============================================================
if st.button("🎁 Sürprizi Gör / Konfeti Patlat!"):
    st.balloons()
    st.snow()
    st.success("Seni çok seviyorum! Günün en az senin kadar güzel geçsin. 💕")

st.divider()

# ============================================================
# İNTERAKTİF TEST (BİZİM HİKÂYEMİZ)
# ============================================================
st.header("🧩 Küçük Bir Test")
st.write("Bakalım hatırında mı?")

answer = st.radio(
    "İlk randevumuzda nerede buluşmuştuk?",
    ("Sahil Kenarı 🌊", "En Sevdiğimiz Kafe ☕", "Sinema 🍿")
)

if st.button("Cevabı Kontrol Et"):
    if answer == "En Sevdiğimiz Kafe ☕":  # Doğru cevabı buraya yaz
        st.success("Harika! Doğru bildin 🥰❤️")
    else:
        st.warning("Tekrar düşün bakalım... 😜")

st.divider()

# ============================================================
# ÖZEL MEKTUP / MESAJ BÖLÜMÜ
# ============================================================
st.header("💌 Sana Özel Bir Not")
with st.expander("Mektubumu Okumak İçin Tıkla ❤️"):
    st.write("""
    Canım sevgilim,
    
    Hayatıma girdiğin günden beri her günüm seninle daha anlamlı ve güzel. 
    Gülüşünle hayatımı aydınlattığın, her anımda yanımda olduğun için teşekkür ederim.
    
    Yeni yaşında tüm dileklerinin gerçekleşmesini, birlikte daha nice mutlu, 
    sağlıklı ve kahkaha dolu yıllar geçirmeyi diliyorum. İyi ki doğdun, iyi ki varsın! 💕
    """)

# Müzik/Ses Dosyası Ekleme (İsteğe Bağlı, ayrı bir bölüm için)
# st.audio("en_sevdigimiz_sarki.mp3")
