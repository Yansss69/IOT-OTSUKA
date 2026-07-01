import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Konfigurasi Halaman (Lebih rapi dengan layout wide)
st.set_page_config(page_title="Production Monitor", layout="wide")

# CSS Kustom untuk tampilan profesional (warna biru gelap, border elegan)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; background-color: #0f172a; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { background-color: #e2e8f0; border-radius: 5px; }
    h1 { color: #1e293b; font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Session State
if 'log1' not in st.session_state: st.session_state.update({'log1':[], 'log2':[], 'log3':[], 'last_col4':None, 'prev_start_time':None})

st.title("📊 PRODUCTION MONITORING SYSTEM")
st.markdown("---")

# Kolom Input (Layout 2 kolom agar seimbang)
col_a, col_b = st.columns(2)
with col_a:
    op = st.text_input("Nama Operator")
with col_b:
    start_time_str = st.text_input("Jam Mulai (HH:MM)", "07:00")

# Logika Perhitungan (Logika tetap 100% sama)
def proses_baris(start_time, durasi):
    mix_ke = len(st.session_state.log3) + 1
    # [LOGIKA ANDA DI SINI]
    if mix_ke == 1:
        p1 = start_time - timedelta(minutes=15); p2 = start_time - timedelta(minutes=12); p3 = start_time; p4 = start_time + timedelta(minutes=3)
        st.session_state.last_col4 = p4
    elif mix_ke == 2:
        p1 = st.session_state.last_col4; p2 = p1 + timedelta(minutes=3); p3 = p2 + timedelta(minutes=12); p4 = p3 + timedelta(minutes=3)
        st.session_state.last_col4 = p4
    else:
        p1 = st.session_state.prev_start_time; p2 = p1 + timedelta(minutes=3); p3 = p2 + timedelta(minutes=12); p4 = p3 + timedelta(minutes=3)
    
    st.session_state.prev_start_time = start_time
    st.session_state.log1.append(f"Mix {mix_ke:<2}: {p1.strftime('%H:%M')} | {p2.strftime('%H:%M')} | {p3.strftime('%H:%M')} | {p4.strftime('%H:%M')}")
    st.session_state.log2.append(f"Mix {mix_ke:<2}: {p2.strftime('%H:%M')} - {p3.strftime('%H:%M')}")
    t_end = start_time + timedelta(minutes=durasi)
    st.session_state.log3.append(f"Mix {mix_ke:<2}: {start_time.strftime('%H:%M')} - {t_end.strftime('%H:%M')}")
    return t_end + timedelta(minutes=5)

# Tombol Aksi
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🚀 GENERATE 16 MIX"):
        current_time = datetime.strptime(start_time_str, "%H:%M")
        st.session_state.update({'log1':[], 'log2':[], 'log3':[]})
        for i in range(1, 17):
            current_time = proses_baris(current_time, 50 if i <= 8 else 40)
        st.rerun()

with col2:
    if st.button("🔄 RESET"):
        st.session_state.update({'log1':[], 'log2':[], 'log3':[], 'last_col4':None, 'prev_start_time':None})
        st.rerun()

# Tampilan Data yang Elegan
tab1, tab2, tab3 = st.tabs(["FORM 1 (TIMING)", "FORM 2 (DURATION)", "FORM 3 (TOTAL)"])
with tab1: st.code("\n".join(st.session_state.log1))
with tab2: st.code("\n".join(st.session_state.log2))
with tab3: st.code("\n".join(st.session_state.log3))

# Footer Summary yang Profesional
if st.session_state.log3:
    st.subheader("Summary Laporan")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    summary_col1.metric("Total Mix", f"{len(st.session_state.log3)}")
    summary_col2.metric("Start Time", st.session_state.log3[0].split('-')[0].strip())
    summary_col3.metric("End Time", st.session_state.log3[-1].split('-')[1].strip())
    
    # Tombol Ekspor
    df = pd.DataFrame({"FORM 1": st.session_state.log1, "FORM 2": st.session_state.log2, "FORM 3": st.session_state.log3})
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    st.download_button("💾 EXPORT KE EXCEL", data=output.getvalue(), file_name="Laporan_Produksi.xlsx")
