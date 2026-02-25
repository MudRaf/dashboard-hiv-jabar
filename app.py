import streamlit as st
import pandas as pd
import plotly.express as px



# ================= CONFIG =================
st.set_page_config(
    page_title="Dashboard HIV Jawa Barat",
    layout="wide"
)

# ================= LOAD DATA =================
df = pd.read_excel(
    "dinkes-od_18510_jumlah_kasus_hiv_berdasarkan_kabupatenkota_v3_data.xlsx"
)

# Rename kolom biar enak
df = df.rename(columns={
    "nama_kabupaten_kota": "Kota",
    "tahun": "Tahun",
    "jumlah_kasus": "Jumlah Kasus"
})

df = df[["Kota", "Tahun", "Jumlah Kasus"]]

# ================= HEADER =================
st.title("Dashboard HIV Jawa Barat")
st.caption("Data kasus HIV/AIDS berdasarkan Kabupaten/Kota di Jawa Barat")

# ================= FILTER =================
with st.expander("🔎 Filter Data", expanded=True):
    c1, c2 = st.columns(2)

    kota = c1.selectbox(
        "Kota",
        ["Semua"] + sorted(df["Kota"].unique())
    )

    tahun = c2.selectbox(
        "Tahun",
        ["Semua"] + sorted(df["Tahun"].unique())
    )

filtered_df = df.copy()

if kota != "Semua":
    filtered_df = filtered_df[filtered_df["Kota"] == kota]

if tahun != "Semua":
    filtered_df = filtered_df[filtered_df["Tahun"] == tahun]

# ================= METRIC =================
total = int(filtered_df["Jumlah Kasus"].sum())
rata = int(filtered_df["Jumlah Kasus"].mean())

kota_max = (
    filtered_df.groupby("Kota")["Jumlah Kasus"].sum().idxmax()
)
kota_max_jml = (
    filtered_df.groupby("Kota")["Jumlah Kasus"].sum().max()
)

m1, m2, m3 = st.columns(3)
m1.metric("Total Kasus", f"{total:,}")
m2.metric("Rata-rata", rata)
m3.metric("Kota Tertinggi", kota_max, f"{int(kota_max_jml):,} kasus")

# ================= CHART =================
c3, c4 = st.columns(2)

kasus_kota = (
    filtered_df.groupby("Kota")["Jumlah Kasus"]
    .sum()
    .reset_index()
)

with c3:
    st.subheader("Jumlah Kasus per Kota")
    fig_bar = px.bar(
        kasus_kota,
        x="Kota",
        y="Jumlah Kasus",
        color="Kota"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c4:
    st.subheader("Tren Kasus per Tahun")
    fig_line = px.line(
        filtered_df.groupby("Tahun")["Jumlah Kasus"]
        .sum()
        .reset_index(),
        x="Tahun",
        y="Jumlah Kasus",
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ================= PIE + TABLE =================
c5, c6 = st.columns(2)

with c5:
    st.subheader("Distribusi per Kota")
    fig_pie = px.pie(
        kasus_kota,
        names="Kota",
        values="Jumlah Kasus"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with c6:
    st.subheader("Data Detail")
    st.dataframe(filtered_df, use_container_width=True)

# ================= FOOTER =================
st.info(
    "Sumber data: Dinas Kesehatan Provinsi Jawa Barat (Open Data Jabar)"
)
