import streamlit as st
import google.generativeai as genai
import random
import os

# --- API ANAHTARI ---
API_KEY = "AIzaSyAOruEBUqlrSuE03BTiEP5I-yQaoVX7zYU"
# --------------------

st.set_page_config(page_title="Pro-Atlet AI Coach", layout="centered")

# Tasarım - Profesyonel Koyu Tema
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background-color: #e63946; 
        color: white; 
        border-radius: 10px; 
        height: 3.8em; 
        font-weight: bold; 
        font-size: 1.1em;
        border: none; 
        transition: 0.3s ease;
    }
    .stButton>button:hover { background-color: #f1faee; color: #1d3557; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# Üst Bölüm: İkonlar ve Ana Görsel
col_left, col_mid, col_right = st.columns([1, 4, 1])

with col_left:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🦅</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa; font-size: 0.8em;'>GÜÇ</p>", unsafe_allow_html=True)

with col_mid:
    if os.path.exists('hero_athlete.png'):
        st.image('hero_athlete.png', use_container_width=True)
    else:
        st.warning("⚠️ 'hero_athlete.png' bulunamadı.")

with col_right:
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>🦉</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa; font-size: 0.8em;'>BİLGELİK</p>", unsafe_allow_html=True)

# Stoacı Motivasyon
motivasyon_arsivi = [
    "“Kendini fethetmeyen insan, hiçbir şeyi fethedemez.”",
    "“Bedeninin nelere muktedir olduğunu görmeden yaşlanmak bir trajedidir.” — Socrates",
    "“Şampiyonlar, kimsenin bakmadığı o karanlık saatlerde doğar.”",
    "“Antrenman yapmadığın her saniye, rakibin çalışıyor.”",
    "“Zorluklar zihni güçlendirir, tıpkı çalışmanın bedeni güçlendirmesi gibi.” — Seneca",
    "“Disiplin, ne istediğinle şu an ne istediğin arasındaki köprüdür.”",
    "“Ringde seni ayakta tutan şey, karanlık odada yaptıklarındır.”",
    "“Konfor alanı, karakterin öldüğü yerdir.”"
]
st.info(f"⚡ **Günün Mentalitesi:** {random.choice(motivasyon_arsivi)}")

st.title("🏆 PRO-ATLET AI COACH")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    branslar = st.multiselect("🏊‍♂️ Branşların", ["Boks", "Yüzme", "Güreş", "Fitness", "Basketbol", "Voleybol"])
    hedef = st.selectbox("💪 Odak Bölgesi", ["Biceps", "Triceps", "Geniş Omuz", "Güçlü Sırt", "Parçalı Karın", "Atletik Bacak"])

with col2:
    sakatlik = st.selectbox("🚑 Sakatlık Durumu", ["Yok", "Ayak Bileği", "Omuz", "Bel", "Diz", "El Bileği"])
    ek_not = st.text_input("📝 AI'ya özel notun (opsiyonel)")

# Analiz Butonu
if st.button("🔥 SİSTEMİ ÇALIŞTIR VE ANALİZ ET"):
    if not branslar:
        st.error("Lütfen en az bir branş seç.")
    else:
        with st.spinner('🎯 AI Analiz Ediyor...'):
            try:
                genai.configure(api_key=API_KEY)
                # Model seçimi
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                selected_model = model_list[0] if model_list else 'gemini-1.5-flash'
                model = genai.GenerativeModel(selected_model)
                
                prompt = f"Sporcu: {branslar}. Hedef: {hedef}. Sakatlık: {sakatlik}. Not: {ek_not}. Profesyonel antrenman programı yaz."
                response = model.generate_content(prompt)
                
                st.success("✅ ANALİZ TAMAMLANDI")
                st.markdown("### 📋 Önerilen Reçete")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

st.markdown("---")