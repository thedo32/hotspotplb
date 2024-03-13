from datetime import datetime
import folium
import streamlit as st
import geopandas as gpd
import pydeck as pdk
from streamlit_float import *
import altair as alt
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium

st.set_page_config(
    page_title = "Hotspot Kebakaran Lahan Hutan dan Polusi Udara",
    page_icon="fishtail.png",
    layout="wide",
    menu_items={"About":"""##### Pengaruh Hotspot Di Puncak Musim El Nino Terhadap Generasi Masa Depan. 
            Author: Jeffri Argon
Email: jeffriargon@gmail.com
            """}
)
float_init()


url = "https://ditppu.menlhk.go.id/portal/read/indeks-standar-pencemar-udara-ispu-sebagai-informasi-mutu-udara-ambien-di-indonesia"
urllhk = "https://www.menlhk.go.id/"
urlsipongi = "https://sipongi.menlhk.go.id/"
urlfirms = "https://firms.modaps.eosdis.nasa.gov/api/country/"
urlopenwea = "https://openweathermap.org/api/air-pollution"
urlbmkg = "https://dataonline.bmkg.go.id/akses_data"
urlboston = "https://www.bc.edu/bc-web/centers/schiller-institute/sites/masscleanair/articles/children.html"
urlhalodoc = "https://www.halodoc.com/artikel/perlu-tahu-ini-7-gangguan-kesehatan-yang-dipicu-partikel-polusi-pm2-5"
urlnafas = "https://nafas.co.id/article/Apakah-PM2-5-berbahaya-untuk-anak-anak"
urlotc = "https://otcdigest.id/kesehatan-anak/polusi-udara-tingkatkan-risiko-adhd-pada-anak-anak"
urlkompastv = "https://www.kompas.tv/regional/448420/akibat-karhutla-kabut-asap-di-palembang-makin-pekat"
urlsctv = "https://www.liputan6.com/photo/read/5415505/diselimuti-kabut-asap-palembang-berlakukan-sekolah-daring?page=1"
urlbnpb = "https://bnpb.go.id/berita/99-penyebab-kebakaran-hutan-dan-lahan-adalah-ulah-manusia"
urlbubble = "https://github.com/thedo32/hotspotplb/blob/master/data/idn.geojson"


firm_all = pd.read_csv('data/nasa_viirs_noaa_oct_2023.csv')
firm_all_prev = pd.read_csv('data/nasa_viirs_noaa_oct_2022.csv')
firm = pd.read_csv('data/hotspot_sumsel.csv')
firm_prev = pd.read_csv('data/hotspot_sumsel_2022.csv')
bmkg = pd.read_csv('data/presipitasi_temp_plb.csv')
firmhs = len(firm_all.index)
sumselhs =len(firm.index)
firmhs_prev = len(firm_all_prev.index)
sumselhs_prev =len(firm_prev.index)


def format_big_number(num):
    if num >= 1e6:
        return f"{num / 1e6:.1f} Mio"
    elif num >= 1e3:
        return f"{num / 1e3:.1f} K"
    elif num >= 1e2:
        return f"{num / 1e3:.1f} K"
    else:
        return f"{num:.2f}"


# tahun sebelumnya dan sekarang
dt_prev = min(bmkg['date'])
dt_now = max(bmkg['date'])


#temperatur sebelumnya dan sekarang
t_prev = bmkg['t_avg'][bmkg['date'] == dt_prev]
t_now =  bmkg['t_avg'][bmkg['date'] == dt_now]
t_avg_prev = t_prev.mean(axis=0)
t_avg_now = t_now.mean(axis=0)

#presipitasi sebelumnya dan sekarang
rr_prev = bmkg['rr_avg'][bmkg['date'] == dt_prev]
rr_now =  bmkg['rr_avg'][bmkg['date'] == dt_now]
rr_avg_prev = rr_prev.mean(axis=0)
rr_avg_now = rr_now.mean(axis=0)



st.markdown("<h1 style='text-align: center; color: #0B60B0;'> Pengaruh Hotspot Di Puncak Musim El Nino"
            " <br> Terhadap Generasi Masa Depan<br><br></h1>", unsafe_allow_html=True)

#perbedaan tahun sebelumnya dan sekarang
hs_diff = 100.0 * ((sumselhs - sumselhs_prev)/sumselhs_prev)
t_diff = 100.0 * ((t_avg_now - t_avg_prev)/t_avg_prev)
rr_diff = 100.0 * ((rr_avg_now - rr_avg_prev)/t_avg_prev)
sumselhs_pct = round(100.0 * (sumselhs/firmhs),2)

st.subheader("Pendahuluan")
with st.container(border=True):
    col_hotspot, col_temp, col_presip = st.columns(3) #add three columns

    with col_hotspot:
      st.metric("Hotspot Sumsel", value=format_big_number(sumselhs), delta=f'{format_big_number(hs_diff)}%', delta_color="off")
      st.write("% dari Hs Indonesia : " + str(sumselhs_pct) + "%")

    with col_temp:
      st.metric("Temperatur Rata2", value=format_big_number(t_avg_now), delta=f'{t_diff:.2f}%',delta_color="off")
      st.write("Unit Pengukuran: Celcius")

    with  col_presip:
      st.metric("Presipitasi Rata2", value=format_big_number(rr_avg_now), delta=f'{rr_diff:.2f}%', delta_color="off")
      st.write( "Unit Pengukuran: mm/hari")

left_cl, main_cl= st.columns([1,8])
with left_cl:
     containup = st.container()
     containup.float()
     containup.markdown("[↗️⬆️↖️](#pendahuluan)", unsafe_allow_html=True)
     with st.container(border=True):
        st.markdown("<h5 style='text-align: left; color: #0B60B0;'>Section:</h5>", unsafe_allow_html=True)
        st.markdown("""
        - [Peta](#peta-sebaran-hotspot-kebakaran-hutan-lahan-bulan-oktober-2023)
        - [Diagram](#diagram-tingkat-ispu-pada-bulan-oktober-2023)
        - [Korrelasi](#korrelasi)
        - [Insight](#insight)
        """, unsafe_allow_html=True)
     st.markdown("<br>", unsafe_allow_html=True)
     with st.container(border=True):
        # st.image("img/free_palestine.png")
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("img/from_river.png")
     st.markdown("<br>", unsafe_allow_html=True)
     with st.container(border=True):
        st.markdown("<p style='text-align: left; color: #0B60B0;'>By: Jeffri Argon</p>", unsafe_allow_html=True)

with (main_cl):
    with st.container(border=True):
        with st.container(border=True):
            st.write("Menurut data [SIPONGI KLHK](%s)" % urlsipongi + " dan [FIRMS NASA](%s)" % urlfirms + " "
                      "pada bulan Oktober 2023, di wilayah Propinsi Sumatera Selatan yang mempunyai penduduk 8,6 juta jiwa (BPS 2022), "
                      "dan mempunyai metropolitan yang berkembang yakni Patungraya Agung yang berpenduduk 2,6 juta jiwa (BPS 2020), "
                      "khususnya Kota Palembang yang berpenduduk sekitar 1,7 juta jiwa (BPS 2022), "
                      "terdapat hotspot terbanyak dari kejadian Bencana Kebakaran Hutan Lahan dibanding propinsi lain di Indonesia, yang diperparah oleh fenomena El Nino. "
                      "Penulis fokus melakukan analisa di Kota Palembang selain karena wikayah itu merupakan wilayah terpadat di Propinsi tersebut, juga karena untuk Data seperti Temperatur, Presipitasi, "
                      "serta Kecepatan Angin karena data didapatkan dari BMKG yang Stasiun dan Akurasi Pengukurannya berada di sekitar Kota Palembang"    
                      "Selain itu fokus analisis juga pada bulan oktober yang merupakan puncak dari musim El Nino Tahun 2023, "
                      "berdasarkan data Temperatur yang tinggi, dan data Presipitasi yang rendah yang mana normalnya musim penghujan di mulai bulan oktober, "
                      "namun menurut data BMKG,  presipitasi sangat rendah di bulan Oktober 2023 tersebut. "
                      "Selain itu juga berdasarkan historikal Data Matrix Sipongi di mana sering terjadi puncak kebakaran hutan lahan di bulan oktober pada tahun terjadinya musim El Nino. "
                      "Kondisi tersebut mengakibatkan terpaparnya polusi kabut asap yang mempunyai risiko tinggi terhadap masyarakat, "
                      "terutama pada kelompok rentan seperti anak-anak dan ibu hamil yang dapat mengancam Generasi Masa Depan")
            # expander for sipongi historical data

            with st.expander("Data Matrix Hotspot Indonesia dari Situs Sipongi KLHK"):
                colmat1, colmat2, colmat3 = st.columns(3)
                with colmat1:
                    st.image("img/hs_2018.png")
                with colmat2:
                    st.image("img/hs_2019.png")
                with colmat3:
                    st.image("img/hs_2020.png")
                colmat4, colmat5, colmat6 = st.columns(3)
                with colmat4:
                    st.image("img/hs_2021.png")
                with colmat5:
                    st.image("img/hs_2022.png")
                with colmat6:
                    st.image("img/hs_2023.png")

            #links sumber bacaan
            st.markdown("* Sumber Bacaan Lebih Lanjut: [BNPB](%s)" % urlbnpb + ", "
                        "[Boston College](%s)" % urlboston + ", "
                        "[Nafas Indonesia](%s)" % urlnafas + ", "
                        "[OTC Digest](%s)" % urlotc + ", "                                                                                                                                                                                                                                                                       
                        "[Halodoc](%s)" % urlhalodoc + ", "
                        "[Kompas TV](%s)" % urlkompastv + ", "
                        "[Liputan 6 SCTV](%s)" % urlsctv, unsafe_allow_html=True)


        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader('Peta Sebaran Hotspot Kebakaran Hutan Lahan Bulan Oktober 2023')
        # st.markdown("<br><h4 style='text-align:"
        #     " center; color: red;'>Peta Sebaran Hotspot Kebakaran Hutan Lahan Bulan Oktober 2023</h4>", unsafe_allow_html=True)


        #tab untuk peta 3 wilayah administrasi
        tab1a, tab1b, tab1c, tab1d = st.tabs(['Kota Palembang', 'Provinsi Sumatera Selatan', 'Indonesia', 'Indonesia Bubble'])

        with tab1a:

            sl1, sl2 = st.columns([1,4])
            with sl1:
                values = st.slider(
                'Radius Sebaran Hotspot (Km)',value=50, min_value=25, max_value=75, step=25)
            if values == 25:
                df1 = gpd.read_file('data/hotspot_plb_25.geojson')
            if values == 50:
                df1 = gpd.read_file('data/hotspot_plb_50.geojson')
            if values == 75:
                df1 = gpd.read_file('data/hotspot_plb_75.geojson')
            # st.write(df2.head(5))
            df1['lon'] = df1.geometry.x  # extract longitude from geometry
            df1['lat'] = df1.geometry.y  # extract latitude from geometry
            df1 = df1[['lon', 'lat']]  # only keep longitude and latitude

            firms_pl = pd.DataFrame(
                df1,
                columns=['lat', 'lon'])

            st.pydeck_chart(pdk.Deck(
                map_provider='carto',
                map_style='dark',
                views=pdk.View(type="mapview", controller=True),
                initial_view_state=pdk.ViewState(
                    latitude=-2.9831,
                    longitude=104.7527,
                    zoom=9,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=firms_pl,
                        get_position='[lon, lat]',
                        get_color='[91, 163, 207, 200]',
                        get_radius=300,
                    ),
                ],
            ))

        #load dataframe
        df = pd.read_csv('data/max_hs_pl_palembang_distinct.csv')
        df0 = pd.read_csv('data/max_distinct_pm25_plb_oct_2023.csv')
        df1 = pd.read_csv('data/max_distinct_pm25_plb_oct_2022.csv')
        df2 = pd.read_csv('data/max_distinct_pm25_plb_aug_2023.csv')
        df3 = pd.read_csv('data/max_distinct_pm25_plb_dec_2023.csv')
        dfispu = pd.read_csv("data/ispu_table.csv")
        

        with st.expander("Analisis Peta"):
            st.write("Dapat dilihat disekitar Kota Palembang terdapat banyak hotspot,"
                     "juga kalau kita melihat ke wilayah propinsi, sebaran hotspot terdapat lebih banyak di "
                     "bagian tenggara propinsi dan tidak jauh dari ibu kota propinsi tersebut. "
                     "Jika keseluruhan di peta Indonesia terdapat kecerahan hostpot hampir mirip di beberapa wilayah, "
                     "kemudian jika melihat peta Indonesia Bubble "
                     "di Sumatera Selatan terdapat 15.848 hotspot, terbanyak dibandingkan propinsi lain, "
                     "dan dibawahnya Kalimantan Tengah sebanyak 13.393 hotspot.")
        
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("Diagram Tingkat ISPU Pada Bulan Oktober 2023")
        
        # threshold1 = 51.0
        # threshold2 = 101.0
        # threshold3 = 201.0
        # threshold4 = 301.0
        #
        with st.container(border=True):
            tabBar, tabArc = st.tabs(['Status ISPU PM 2.5', 'Persentase'])
            with tabBar:
                colLBar, colBar, colRBar = st.columns([1,20, 1])
                with colBar:
                    banding = st.checkbox('Perbandingan', value=False)
                    if banding:
                        bars = alt.Chart(df).mark_bar(size=24).encode(
                            y="Status:O",
                            x=alt.X("count(Value):Q", title="Jumlah Hari"),
                            row="Bulan:N",
                            color=alt.Color("max(Color):N", scale=None)
                        ).properties(height=72, width=600).interactive(bind_x=True,bind_y=True)
                        st.altair_chart(bars)
                    else:
                        bars = alt.Chart(df0).mark_bar(size=27).encode(
                            y="Status:O",
                            x=alt.X("count(Value):Q", title="Jumlah Hari"),
                            color=alt.Color("max(Color):N", scale=None)
                        ).properties(height=270, width=800).interactive()
                        st.altair_chart(bars)

                    with st.expander("Tabel Status ISPU"):
                        bars = alt.Chart(dfispu).mark_bar().encode(
                            y=alt.X("Status", axis=alt.Axis(labels=False)),
                            x=alt.Y("Keterangan", axis=alt.Axis(labels=False)),
                            color=alt.Color("Color:N", scale=None)
                        ).properties(width=720)

                        text = alt.Chart(dfispu).mark_text(
                            align='left',
                            dx=3,
                            fontSize=12,
                            color="#F0EDCF",
                        ).encode(
                            y=alt.X("Status", axis=alt.Axis(labels=False)),
                            x=alt.Y("Keterangan", axis=alt.Axis(labels=False)),
                            text=alt.Y("Text"),
                        )

                        st.altair_chart(bars + text)

            with tabArc:
                colLArc, colArc1, colArc2, colRArc = st.columns([1, 9, 9, 1])
                with colArc1:
                    okt23 = st.checkbox('Oktober 2023',value=True)
                    if okt23:
                        base = alt.Chart(df0).mark_arc(innerRadius=50, outerRadius=105).encode(
                        alt.Color("Persentase:O").legend(None),
                              alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                    # color=alt.Color("max(Color)", scale=None)
                            ).properties(height=300, width=300).interactive()

                        text = base.mark_text(radius=148, size=12).encode(text="Status:N")
                        st.altair_chart(base + text, use_container_width=True)

                with colArc2:
                     okt22 = st.checkbox('Oktober 2022', value=False)
                     if okt22:
                        base = alt.Chart(df1).mark_arc(innerRadius=30, outerRadius=70).encode(
                            alt.Color("Persentase:O").legend(None),
                                alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                                # color=alt.Color("max(Color)", scale=None)
                            ).properties(height=210, width=210).interactive()

                        text = base.mark_text(radius=90, size=11).encode(text="Status:N")
                        st.altair_chart(base + text, use_container_width=True)

                colLArcs, colArcs1, colArcs2, colRArcs = st.columns([1, 4, 4, 1])
                with colArcs1:
                    ags23 = st.checkbox('Agustus 2023', value=False)
                    if ags23:
                        base = alt.Chart(df2).mark_arc(innerRadius=30, outerRadius=70).encode(
                            alt.Color("Persentase:O").legend(None),
                                alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                                # color=alt.Color("max(Color)", scale=None)
                            ).properties(height=210, width=210).interactive()
                        text = base.mark_text(radius=90, size=11).encode(text="Status:N")
                        st.altair_chart(base + text, use_container_width=True)

                with colArcs2:
                    des23 = st.checkbox('Desember 2023', value=False)
                    if des23:
                       base = alt.Chart(df3).mark_arc(innerRadius=30, outerRadius=70).encode(
                              alt.Color("Persentase:O").legend(None),
                              alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                                    # color=alt.Color("max(Color)", scale=None)
                            ).properties(height=210, width=210).interactive()
                       text = base.mark_text(radius=90, size=11).encode(text="Status:N")
                       st.altair_chart(base + text, use_container_width=True)

        #
        # highlight1 = bars.mark_bar(color="blue", opacity=0.2).encode(
        #     y2=alt.Y2(datum=threshold1)
        # ).transform_filter(
        #     alt.datum.Value > threshold1
        # )
        #
        # highlight2 = bars.mark_bar(color="yellow").encode(
        #     y2=alt.Y2(datum=threshold2)
        # ).transform_filter(
        #     alt.datum.Value > threshold2
        # )
        #
        # highlight3 = bars.mark_bar(color="red").encode(
        #     y2=alt.Y2(datum=threshold3)
        # ).transform_filter(
        #     alt.datum.Value > threshold3
        # )
        #
        # rule1 = alt.Chart().mark_rule(size=2).encode(
        #     y=alt.Y(datum=threshold2)
        # )
        #
        # label1 = rule1.mark_text(
        #     x="width",
        #     dx=-2,
        #     align="right",
        #     baseline="bottom",
        #     fontSize=15,
        #     text="TIDAK SEHAT",
        #     color="grey"
        #
        # )
        #
        # rule2 = alt.Chart().mark_rule(size=2).encode(
        #     y=alt.Y(datum=threshold3)
        # )
        #
        # label2 = rule2.mark_text(
        #     x="width",
        #     dx=-2,
        #     align="right",
        #     baseline="bottom",
        #     fontSize=15,
        #     text="SANGAT TIDAK SEHAT",
        #     color="grey"
        # )
        #
        # st.altair_chart(bars + highlight1 + highlight2 + highlight3 + rule1 + label1 +rule2 + label2, use_container_width=True)
               

        with st.expander("Analisis ISPU"):
            st.write("Analisis ISPU fokus pada PM 2.5 yang merupakan partikel"
                     " pencemar paling berpengaruh"
                     " bagi kesehatan - [DitppuLHK](%s)" % url)
            st.write(
                "Particulate Matter (PM2.5) adalah partikel udara yang berukuran lebih kecil dari atau sama dengan 2.5 µm (mikrometer).\n"
                "PM2.5 berbahaya bagi orang-orang dari segala usia namun sangat berbahaya bagi anak-anak. \n"
                "Dibandingkan orang dewasa, tubuh anak-anak lebih rentan terhadap polusi PM2.5 ini. \n "
                "Partikel kecil ini dapat menyebabkan banyak dampak negatif terhadap kesehatan \n"
                "pada anak termasuk asma, penurunan volume otak, disfungsi perilaku, ADHD, Autism Spectrum Disorder (ASD), \n"
                "dan gangguan pertumbuhan paru-paru. \n"
                "Paparan seorang ibu terhadap PM2.5 selama kehamilannya meningkatkan risiko kelahiran prematur, \n"
                " berat badan lahir rendah, dan lahir mati.")
            st.write("Dari diagram di atas dapat kita lihat di Kota Palembang pada Bulan Oktober 2023, mayoritas status pencemaran udara berada di tingkat Tidak Sehat, "
                     "bahkan ada 5 hari di bulan tersebut status pencemaran berada di tingkat Sangat Tidak Sehat, "
                     "yang dapat membahayakan kondisi kesehatan manusia, sangat berisiko terhadap masa depan anak-anak."
                     "Melalui perbandingan antara bulan Oktober 2023 yang menurut Data Matrix Sipongi KLHK di atas merupakan masa puncak terjadinya Kebakaran Hutan Lahan (Karhutla) tahun 2023, dengan saat setahun sebelumnya di Oktober 2022, dengan saat Karhutla tahun 2023 belum mencapai puncak di bulan Agustus, dengan saat Karhutla Tahun 2023 menurun di bulan Desember, "
                     "diperkuat dengan berita di media massa tentang kritikalnya kondisi kabut asap di Bulan OKtober 2023 tersebut, maka dapat dikatakan kondisi kabut asap akibat Karhutla merupakan salah satu penyebab utama memburuknya status ISPU PM 2.5 tersebut."
                     "Selain diagram di atas berikut ini kita bisa lihat analisa korelasi Jarak Rata2 Titik Kebakaran Hutan di sekitar Palembang, Presipitasi,"
                     "Kecapatan Angin, Temperatur dan Kecerahan Hotspot.")



        #dataframe untuk korrelasi
        dfcorr = pd.read_csv('data/pollute_plb_heatmap.csv')

        # data = pd.pivot_table(
        #     data=dfcorr,
        #     index=['Tanggal'.format(datetime)],
        #     aggfunc={
        #         'ISPU_PM_2_5':'max',
        #         'PM2_5':'max',
        #         'PM10':'max',
        #         'Jumlah_Hs':'count',
        #         'Channel_4': 'sum',
        #         'Channel_5': 'sum',
        #         'Jarak':'mean',
        #         'Temperatur':'mean',
        #         'Presipitasi':'mean',
        #         'Kec_Angin':'mean'
        #     }
        # ).reset_index()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("Korrelasi")
        # st.markdown("<br><br><h4 style='text-align: center; color: red;'>Korrelasi ✨ </h4>", unsafe_allow_html=True)


        #korrelasi pm2_5 dengan jarak, curah hujan, kecepatan angin

        option = st.selectbox(
            "Pilih Data yang ingin dikorrelasikan dengan ISPU PM 2.5 Harian",
            ("Data Heatmap Korrelasi", "Jumlah Hs dan ISPU PM 2.5", "Jarak dan ISPU PM 2.5",
             "Presipitasi dan ISPU PM 2.5", "Kecepatan  Angin dan ISPU PM 2.5",
            "Temperatur dan ISPU PM 2.5")
        )

        colL1, colM1, colR1 = st.columns([2, 10, 2])
        heatL, heatC, healR = st.columns([3, 8, 3])
        with colM1:
            if option == "Data Heatmap Korrelasi":
                with heatC:
                    with st.container(border=True):
                        heat = sns.heatmap(dfcorr.corr(),  cmap="Blues", annot=True)
                        st.write(heat.get_figure())

            if option=="Jumlah Hs dan ISPU PM 2.5":
                    scatter= alt.Chart(dfcorr).mark_point(size=50).encode(
                            x=alt.X("Jumlah_Hs:Q", title="Jumlah Hotspot"),
                            y=alt.Y("ISPU:Q", title="ISPU PM 2.5"),
                        ).interactive().properties(height=425)

                    st.altair_chart(scatter +
                                        scatter.transform_regression('Jumlah_Hs', 'ISPU').
                                        mark_line(size=3, color="red", opacity=0.3),
                                        theme='streamlit', use_container_width=True)
                
            if option=="Jarak dan ISPU PM 2.5":
                    scatter= alt.Chart(dfcorr).mark_point(size=50).encode(
                            x=alt.X("Jarak:Q", title="Jarak Rata2(km)"),
                            y=alt.Y("ISPU:Q", title="ISPU PM 2.5"),
                        ).interactive().properties(height=425)

                    st.altair_chart(scatter +
                                        scatter.transform_regression('Jarak', 'ISPU').
                                        mark_line(size=3, color="red", opacity=0.3),
                                        theme='streamlit', use_container_width=True)

            if option=="Presipitasi dan ISPU PM 2.5":
                    scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                            x=alt.X("Presipitasi:Q", title="Presipitasi (mm)"),
                            y=alt.Y("ISPU:Q", title="ISPU PM 2.5"),
                            
                        ).interactive().properties(height=425)

                    st.altair_chart(scatter +
                                        scatter.transform_regression('Presipitasi', 'ISPU').
                                        mark_line(size=3, color="red", opacity=0.3),
                                        theme='streamlit', use_container_width=True)

            if option=="Kecepatan  Angin dan ISPU PM 2.5":
                    scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                            x=alt.X("Kec_Angin:Q", title="Kecepatan Angin (m/detik)"),
                            y=alt.Y("ISPU:Q", title="ISPU PM 2.5"),
                        ).interactive().properties(height=425)

                    st.altair_chart(scatter +
                                        scatter.transform_regression('Kec_Angin', 'ISPU').
                                        mark_line(size=3, color="red", opacity=0.3),
                                        theme='streamlit', use_container_width=True)

            if option=="Temperatur dan ISPU PM 2.5":
                    scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                            x=alt.X("Temper:Q", title="Temperatur (Celcius)"),
                            y=alt.Y("ISPU:Q", title="ISPU PM 2.5"),
                        ).interactive().properties(height=425)

                    st.altair_chart(scatter +
                                        scatter.transform_regression('Temper', 'ISPU').
                                        mark_line(size=3, color="red", opacity=0.3),
                                        theme='streamlit', use_container_width=True)



        with st.expander("Analisis Korrelasi"):
            st.write("Untuk Korrelasi ISPU PM 2.5, terdapat korelasi positif antara Jumlah Hotspot harian dengan nilai ISPU PM 2.5 harian, "
                     "Kemudian hubungan negatif dengan Jarak Rata2 Hotspot semakin dekat,  di mana Jarak semakin tinggi nilai ISPU PM 2.5. "
                     "Begitu juga korrelasi Presipitasi, berkurangnya presipitasi atau curah hujan, maka nilai ISPU PM 2.5 yang semakin tinggi. "
                     "Demikian juga semakin turun kecepatan angin di sekitar Kota Palembang tingkat nilai ISPU PM 2.5 akan meningkat, "
                     "hubungan negatif juga berlaku untuk Temperatur rata2 Kota Palembang dengan nilai ISPU PM 2.5 tersebut.")
            st.write("Mengenai korrelasi kecepatan angin, temperatur dengan ISPU PM 2.5 menunjukkan hubungan yang negatif. "
                     "sepertinya hal ini perlu diteliti lebih lanjut lagi, karena seperti disebutkan sebelumnya data didapatkan dari BMKG yang Stasiun dan Akurasi Pengukurannya berada di sekitar Kota Palembang, "
                     "perlu didapatkan lagi data untuk daerah yang lebih luas dari sekitar Kota Palembang, "
                     "selain  itu juga  menghitung paramater lain seperti Arah Angin Pada Kecepatan Maksimum, Arah Angin Terbanyak, Kelembapan, Lamanya Penyinaran Matahari."
                     "Demikian juga kita bisa menganalisis lebih lanjut  mengenai korrelasi selain dengan ISPU PM 2.5, seperti yang tergambar dalam Diagram Heatmap. "
                     "Harapan penulis ke depan baik untuk penulis atau siapapun yang tertarik dengan penelitian ini, bisa menggali lebih dalam dan berdiskusi "
                     "lagi dengan para ahli Meteorologi Geofisika dan Klimatologi, "
                     "serta dilengkapi dengan data Sosial Ekonomi masyarakat sekitar, untuk penelitian lebih lanjut.")

with st.container(border=True):
    st.subheader("Insight")
    with st.expander("Partikel Kecil Mengancam Generasi Masa Depan"):
        #st.markdown(
        #     "<h4 style='text-align: center; color: red;'>Partikel Kecil Mengancam Generasi Masa Depan</h4>",
        #     unsafe_allow_html=True)
        st.write("Particulate Matter (PM2.5) adalah partikel udara yang berukuran lebih kecil dari atau sama dengan 2.5 µm (mikrometer).\n"
             "PM2.5 berbahaya bagi orang-orang dari segala usia namun sangat berbahaya bagi anak-anak. \n"
             "Dibandingkan orang dewasa, tubuh anak-anak lebih rentan terhadap polusi PM2.5 ini. \n " 
             "Partikel kecil ini dapat menyebabkan banyak dampak negatif terhadap kesehatan \n" 
             "pada anak termasuk asma, penurunan volume otak, disfungsi perilaku, ADHD, Autism Spectrum Disorder (ASD), \n"
             "dan gangguan pertumbuhan paru-paru. \n"
             "Sangatlah penting untuk memikirkan kesehatan anak-anak kita ketika mengatasi polusi udara. Penyakit yang berhubungan dengan polusi udara akan "
             "berdampak pada kesehatan anak-anak seumur hidup mereka."    
             "Paparan seorang ibu terhadap PM2.5 selama kehamilannya meningkatkan risiko kelahiran prematur, \n" 
             " berat badan lahir rendah, dan lahir mati." )
        st.write("Mengingat kepentingan tersebut di atas maka perlu dilakukan perlindungan bagi anak-anak dari bahaya pencemaran udara yang umumnya dimulai pukul 7 pagi di "
                 "saat anak-anak umumnya akan memulai aktivitas belajarnya,"
                 "saat ketika kendaraan bermotor mulai memenuhi jalanan dan apalagi ketika di saat yang bersamaan terjadi paparan kabut asap akibat kebakan hutan lahan."
                 "Untuk mengantisipasi paparan pencemaran udara sangat dianjurkan anak-anak tetap memakai masker, atau jika status udara menjadi sangat tidak sehat bahkan berbahaya, tidak memungkinkan beraktivitas di luar ruangan "
                 "maka diberlakukanlah aktivitas sekolah daring. Selain itu pemerintah juga harus bertekad dan mengerahkan segala sumber daya untuk segera melakukan pemadaman kebakaran hutan lahan"
                 "Selain itu yang paling penting perlu dilakukan langkah pencegahan, menggunakan sumber daya  yang tersedia untuk meng-edukasi masyarakat dan membuat payung-payung "
                 "hukum yang lengkap dan detail yang untuk mencegah terjadinya kebakaran hutan lahan baik yang disengaja maupun tidak disengaja (99% disengajakan oleh manusia menurut BNPB), "
                 "serta kebijakan lain dalam upaya mendatangkan udara yang bersih di wilayah tersebut."
                 "Sehingga paparan pencemaran udara pada anak-anak jauh menurun, sehingga meningkatkan kesehatan dan kecerdasan dari Generasi Masa Depan Indonesia. ")


with st.container(border=True):
    st.markdown("* Sumber Data: [KemenLHK](%s)" % urllhk + ", "
             "[FIRMS NASA](%s)" % urlfirms + ", "
             "[Open Weather Map](%s)" % urlopenwea + ", "
             "[BMKG](%s)" % urlbmkg, unsafe_allow_html=True)

with main_cl:
#tab lain utk peta diloading paling akhir
        with tab1b:
            df2 = gpd.read_file('data/hostpot_sumsel.geojsonl.json')
            # st.write(df2.head(5))
            df2['lon'] = df2.geometry.x  # extract longitude from geometry
            df2['lat'] = df2.geometry.y  # extract latitude from geometry
            df2 = df2[['lon', 'lat']]  # only keep longitude and latitude

            firms = pd.DataFrame(
                df2,
                columns=['lat', 'lon'])

            st.pydeck_chart(pdk.Deck(
                map_provider='carto',
                map_style='dark',
                views=pdk.View(type="mapview", controller=True),
                initial_view_state=pdk.ViewState(
                    latitude=-2.9831,
                    longitude=104.7527,
                    zoom=7,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=firms,
                        get_position='[lon, lat]',
                        get_color='[91, 163, 207, 200]',
                        get_radius=300,
                    ),
                ],
            ))



        with tab1c:
            df = pd.read_csv('data/idn.csv')

            # Create the choropleth bubble map
            fig = px.scatter_mapbox(
                df,
                lat="Latitude",
                lon="Longitude",
                size="Size",  # Bubble size based on the "count" attribute
                mapbox_style="carto-darkmatter",  # Choose a suitable projection
                labels={"Size":"Ukuran Hs/Jumlah Total Hs di Bubble Besar"},
                # hover_name="prov",  # Display count on hover
                color_discrete_sequence=["#5BA3CF"],  # Customize bubble color
                height=600,
                zoom=3.7,
                center=dict(lat=-3.1940, lon=117.5540),  # this will center on the point
            )

            # Show the map
            st.plotly_chart(fig, use_container_width=True)

        with tab1d:
            if st.checkbox("Folium Map", value=False):
                callback = """\
                function (row) {
                    var icon, marker;
                    icon = L.AwesomeMarkers.icon({
                        icon: "map-marker",  markerColor: "blue"});
                    marker = L.marker(new L.LatLng(row[0], row[1]));
                    marker.setIcon(icon);
                    return marker;
                };
                """

                # load data
                points = gpd.read_file('data/idns.geojson')

                # draw map
                m = folium.Map(location=[-3.1940, 117.5540],
                               tiles = 'cartodbdarkmatter',
                               zoom_start=4.2, height=600, control_scale=True)

                # Get x and y coordinates for each point
                # points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
                # points_gjson.add_to(m)

                # Get x and y coordinates for each point
                points["x"] = points["geometry"].x
                points["y"] = points["geometry"].y

                # Create a list of coordinate pairs
                locations = list(zip(points["y"], points["x"]))

                # Create a folium marker cluster
                fast_marker_cluster = FastMarkerCluster(locations, callback=callback )

                # Add marker cluster to map
                fast_marker_cluster.add_to(m)

                # draw maps
                st_folium(m, use_container_width=True)

            else:
                df = pd.read_csv('data/idn_hs_by_prov.csv')
                # Create the choropleth bubble map
                fig = px.scatter_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    size="count",  # Bubble size based on the "count" attribute
                    mapbox_style="carto-darkmatter",  # Choose a suitable projection
                    labels={"count": "Jumlah Hotspot"},
                    hover_name="prov",  # Display count on hover
                    color_discrete_sequence=["#5BA3CF"],  # Customize bubble color
                    height=600,
                    zoom=3.7,
                    center=dict(lat=-3.1940, lon=117.5540),  # this will center on the point
                   )

                # Show the map
                st.plotly_chart(fig, use_container_width=True)
                #st.markdown("Sumber Data Peta: [Geojson](%s)" % urlbubble, unsafe_allow_html=True)