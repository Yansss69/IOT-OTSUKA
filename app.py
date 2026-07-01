import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Konfigurasi Halaman
st.set_page_config(page_title="SACHET MONITOR", layout="wide")

# Inisialisasi Session State (agar data tidak hilang saat refresh)
if 'log1' not in st.session_state: st.session_state.log1 = []
if 'log2' not in st.session_state: st.session_state.log2 = []
if 'log3' not in st.session_state: st.session_state.log3 = []
if 'last_col4' not in st.session_state: st.session_state.last_col4 = None
if 'prev_start_time' not in st.session_state: st.session_state.prev_start_time = None

st.title("PRODUCTION MONITOR - GIANT SCALE")

# Input User
op = st.text_input("Nama Operator")
start_time_str = st.text_input("Jam Mulai (HH:MM)", "07:00")

# Fungsi Logika (Sama persis dengan logika Anda)
def proses_baris(start_time, durasi):
    mix_ke = len(st.session_state.log3) + 1
    if mix_ke == 1:
        p1 = start_time - timedelta(minutes=15)
        p2 = start_time - timedelta(minutes=12)
        p3 = start_time
        p4 = start_time + timedelta(minutes=3)
        st.session_state.last_col4 = p4
    elif mix_ke == 2:
        p1 = st.session_state.last_col4
        p2 = p1 + timedelta(minutes=3)
        p3 = p2 + timedelta(minutes=12)
        p4 = p3 + timedelta(minutes=3)
        st.session_state.last_col4 = p4
    else:
        p1 = st.session_state.prev_start_time
        p2 = p1 + timedelta(minutes=3)
        p3 = p2 + timedelta(minutes=12)
        p4 = p3 + timedelta(minutes=3)
    
    st.session_state.prev_start_time = start_time
    data_f1 = f"Mix {mix_ke:<2}: {p1.strftime('%H:%M')} | {p2.strftime('%H:%M')} | {p3.strftime('%H:%M')} | {p4.strftime('%H:%M')}"
    data_f2 = f"Mix {mix_ke:<2}: {p2.strftime('%H:%M')} - {p3.strftime('%H:%M')}"
    t_end = start_time + timedelta(minutes=durasi)
    data_f3 = f"Mix {mix_ke:<2}: {start_time.strftime('%H:%M')} - {t_end.strftime('%H:%M')}"
    
    st.session_state.log1.append(data_f1)
    st.session_state.log2.append(data_f2)
    st.session_state.log3.append(data_f3)
    return t_end + timedelta(minutes=5)

# Tombol Generate
if st.button("🚀 GENERATE 16 MIX (OTOMATIS)"):
    try:
        current_time = datetime.strptime(start_time_str, "%H:%M")
        st.session_state.log1, st.session_state.log2, st.session_state.log3 = [], [], []
        for i in range(1, 17):
            durasi = 50 if i <= 8 else 40
            current_time = proses_baris(current_time, durasi)
        st.rerun()
    except: st.error("Format jam salah! Gunakan HH:MM")

# Tampilan Tab
tab1, tab2, tab3 = st.tabs(["FORM 1 (TIMING)", "FORM 2 (DURATION)", "FORM 3 (TOTAL)"])
with tab1: st.text("\n".join(st.session_state.log1))
with tab2: st.text("\n".join(st.session_state.log2))
with tab3: st.text("\n".join(st.session_state.log3))

# Tombol Reset
if st.button("🔄 RESET"):
    st.session_state.log1, st.session_state.log2, st.session_state.log3 = [], [], []
    st.session_state.last_col4, st.session_state.prev_start_time = None, None
    st.rerun()

# Tombol Export Excel
if st.session_state.log3:
    df = pd.DataFrame({
        "OPERATOR": [op] * len(st.session_state.log3),
        "FORM 1": st.session_state.log1,
        "FORM 2": st.session_state.log2,
        "FORM 3": st.session_state.log3
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    st.download_button("💾 DOWNLOAD EXCEL", data=output.getvalue(), file_name="Laporan_Produksi.xlsx")
