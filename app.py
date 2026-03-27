import streamlit as st
import google.generativeai as genai
import random
import os

# --- 1. SİSTEM AYARLARI (İLK SIRADA OLMALI) ---
st.set_page_config(
    page_title="Pro-Atlet AI Coach",
    page_icon="🏆",
    layout="centered"
)

# --- 2. API VE GÜVENLİK ---
# API anahtarını st.secrets üzerinden güvenli bir şekilde alıyoruz
API_KEY = st.secrets["GEMINI_API_KEY"]

# --- 3. TASARIM VE STİL ---
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background-color: #e63946; 
        color: white; 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold; 
        border: none; 
        transition: 0.3s ease;
    }
    .stButton>button:hover { background-color: #f1faee; color: #1d3557; }
</style>
""", unsafe_allow_html=True)

# --- 4. ÜST BÖLÜM: VİTRİN ---
col_l, col_m, col_r = st.columns([1, 4, 1])
with col_l:
    st.markdown("<h2 style='text-align:center;'>🦅</h2><p style='text-align:center;color:#aaa;font-size:0.7em;'>GÜÇ</p>", unsafe_allow_html=True)

with col_m:
    # Görsel kontrolü
    if os.path.exists('hero_athlete.png'):
        st.image('hero_athlete.png', use_container_width=True)
    else:
        st.info("🎯 Pro-Atlet AI Coaching System")

with col_r:
    st.markdown("<h2 style='text-align:center;'>🦉</h2><p style='text-align:center;color:#aaa;font-size:0.7em;'>BİLGELİK</p>", unsafe_allow_html=True)

# --- 5. MENTALİTE ---
motivasyon = [
    "“Kendini fethetmeyen insan, hiçbir şeyi fethedemez.”",
    "“Bedeninin nelere muktedir olduğunu görmeden yaşlanmak bir trajedidir.” — Socrates",
    "“Disiplin, ne istediğinle şu an ne istediğin arasındaki köprüdür.”",
    "“Konfor alanı, karakterin öldüğü yerdir.”"
]
st.info(f"⚡ **Günün Mentalitesi:** {random.choice(motivasyon)}")

# --- 6. GİRİŞ ALANLARI ---
st.title("🏆 PRO-ATLET AI COACH")
st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    branslar = st.multiselect("🏊‍♂️ Branşların", ["Boks", "Yüzme", "Güreş", "Fitness", "Basketbol", "Voleybol"])
    hedef = st.selectbox("💪 Odak Bölgesi", ["Biceps", "Triceps", "Geniş Omuz", "Güçlü Sırt", "Parçalı Karın", "Atletik Bacak"])

with c2:
    sakatlik = st.selectbox("🚑 Sakatlık Durumu", ["Yok", "Ayak Bileği", "Omuz", "Bel", "Diz", "El Bileği"])
    ek_not = st.text_input("📝 AI'ya özel notun (opsiyonel)")

# --- 7. ANALİZ MANTIK (LOGIC) ---
if st.button("🔥 SİSTEMİ ÇALIŞTIR VE ANALİZ ET"):
    if not branslar:
        st.error("Lütfen en az bir branş seçin.")
    else:
        with st.spinner('🎯 AI Analiz Ediyor...'):
            try:
                # Google AI Yapılandırması
                genai.configure(api_key=API_KEY)
                
                # --- DINAMIK MODEL SEÇİCİ ---
                # Hata almamak için sistemdeki aktif modelleri listeliyoruz
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Eğer gemini-1.5-flash listede varsa onu seç, yoksa listedeki ilk uygun modeli al
                model_name = "gemini-1.5-flash" if any("gemini-1.5-flash" in m for m in available_models) else available_models[0]
                
                model = genai.GenerativeModel(model_name)
                # ----------------------------
                
                prompt = f"""Profesyonel bir spor koçu gibi davran. 
                Branşlar: {branslar}. Hedef Bölge: {hedef}. Sakatlık: {sakatlik}. Notlar: {ek_not}. 
                Buna uygun bilimsel temelli bir antrenman programı yaz."""
                
                response = model.generate_content(prompt)
                
                st.success("✅ ANALİZ TAMAMLANDI")
                st.markdown("### 📋 Önerilen Reçete")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")