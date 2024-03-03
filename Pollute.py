from datetime import datetime
import geopandas as gpd
import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_float import *
import altair as alt



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



st.set_page_config(
    page_title = "Polusi Udara dan Hotspot Kebakaran Lahan Hutan",
    page_icon="fishtail.png",
    layout="wide",
)
float_init()

def format_big_number(num):
    if num >= 1e6:
        return f"{num / 1e6:.3f} Mio"
    elif num >= 1e3:
        return f"{num / 1e3:.3f} K"
    elif num >= 1e2:
        return f"{num / 1e3:.3f} K"
    else:
        return f"{num:.3f}"


firm_all = pd.read_csv('data/nasa_viirs_noaa_oct_2023.csv')
firm_all_prev = pd.read_csv('data/nasa_viirs_noaa_oct_2022.csv')
firm = pd.read_csv('data/hotspot_sumsel.csv')
firm_prev = pd.read_csv('data/hotspot_sumsel_2022.csv')
bmkg = pd.read_csv('data/curah_hujan_temp_plb.csv')
firmhs = len(firm_all.index)
sumselhs =len(firm.index)
firmhs_prev = len(firm_all_prev.index)
sumselhs_prev =len(firm_prev.index)


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



st.markdown("<h2 style='text-align: center; color: orange;'> Pengaruh Hotspot Di Musim El Nino"
            " <br> Terhadap Generasi Masa Depan Indonesia <br><br></h2>", unsafe_allow_html=True)

#perbedaan tahun sebelumnya dan sekarang
hs_diff = 100.0 * ((sumselhs - sumselhs_prev)/sumselhs_prev)
t_diff = 100.0 * ((t_avg_now - t_avg_prev)/t_avg_prev)
rr_diff = 100.0 * ((rr_avg_now - rr_avg_prev)/t_avg_prev)
sumselhs_pct = round(100.0 * (sumselhs/firmhs),2)

st.subheader("Pendahuluan")
with st.container(border=True):
    col_hotspot, col_temp, col_presip = st.columns(3) #add three columns

    with col_hotspot:
      st.metric("Hotspot Sumsel", value=format_big_number(sumselhs), delta=f'{hs_diff:.0f}%')
      st.write("% dari Hs Indonesia : " + str(sumselhs_pct) + "%")

    with col_temp:
      st.metric("Temperatur Rata2", value=format_big_number(t_avg_now), delta=f'{t_diff:.2f}%')
      st.write("Unit Pengukuran: Celcius")

    with  col_presip:
      st.metric("Presipitasi Rata2", value=format_big_number(rr_avg_now), delta=f'{rr_diff:.2f}%')
      st.write( "Unit Pengukuran: mm/hari")

left_cl, main_cl= st.columns([1,8])
with left_cl:
     containup = st.container()
     containup.float()
     with containup:
         st.markdown("""
                 [Up🔝](#pendahuluan)
                 """, unsafe_allow_html=True)

     with st.container(border=True):
        st.markdown("<h5 style='text-align: left; color: orange;'>Section:</h5>", unsafe_allow_html=True)
        st.markdown("""
        - [Pendahuluan](#pendahuluan)
        - [Peta](#peta-sebaran-hotspot-kebakaran-hutan-lahan-bulan-oktober-2023)
        - [Diagram](#diagram-tingkat-ispu-harian-pada-bulan-oktober-2023)
        - [Korrelasi](#korrelasi)
        - [Insight](#insight)
        """, unsafe_allow_html=True)
     st.markdown("<br>", unsafe_allow_html=True)
     with st.container(border=True):
        st.image("data/free_palestine.png")
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("data/from_river.png")
     st.markdown("<br>", unsafe_allow_html=True)
     with st.container(border=True):
        st.markdown("<p style='text-align: left; color: orange;'>By: Jeffri Argon</p>", unsafe_allow_html=True)


     #css function for column
     # def local_css(file_name):
     #     with open(file_name) as f:
     #         st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
     #
     # local_css("style.css")

with main_cl:
    with st.container(border=True):
        with st.container(border=True):
            st.write("Menurut data [SIPONGI KLHK](%s)" % urlsipongi + " dan [FIRMS NASA](%s)" % urlfirms + " pada bulan Oktober 2023, di wilayah Propinsi Sumatera Selatan yang mempunyai penduduk 8,6 juta jiwa (BPS 2022), dan mempunyai metropolitan yang berkembang yakni Patungraya Agung yang berpenduduk 2,6 juta jiwa (BPS 2020), khususnya Kota Palembang yang berpenduduk sekitar 1,7 juta jiwa (BPS 2022), terjadi puncak kejadian Bencana Kebakaran Hutan Lahan yang diperparah oleh fenomena El Nino. Kejadian ini mengakibatkan terpaparnya polusi kabut asap yang mempunyai risiko tinggi terhadap masyarakat, terutama pada kelompok rentan seperti anak-anak dan ibu hamil yang dapat mengancam Generasi Masa Depan Indonesia")
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader('Peta Sebaran Hotspot Kebakaran Hutan Lahan Bulan Oktober 2023')
        # st.markdown("<br><h4 style='text-align:"
        #     " center; color: red;'>Peta Sebaran Hotspot Kebakaran Hutan Lahan Bulan Oktober 2023</h4>", unsafe_allow_html=True)

        #tab untuk peta 3 wilayah administrasi
        tab1, tab2, tab3 = st.tabs(['Kota Palembang', 'Provinsi Sumatera Selatan', 'Indonesia'])


        with tab1:

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
                        get_color='[200, 30, 0, 200]',
                        get_radius=300,
                    ),
                ],
            ))


        df = pd.read_csv('data/max_hs_pl_palembang_distinct.csv')

        data = pd.pivot_table(
            data=df,
            index=['tgl'],
            aggfunc={
                'Value':pd.Series.nunique,
                'Tanggal':pd.Series.nunique,
            }
        ).reset_index()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("Diagram Tingkat ISPU Harian Pada Bulan Oktober 2023")
        # st.markdown("<br><h4 style='text-align: center; color: red;'>Tingkat ISPU PM 2.5 per Hari di Bulan Oktober 2023</h4>", unsafe_allow_html=True)

        threshold1 = 51.0
        threshold2 = 101.0
        threshold3 = 201.0
        threshold4 = 301.0

        bars = alt.Chart(df).mark_bar(color="green", opacity=0.2).encode(
            x="Tanggal:O",
            y="Value:Q",
        )

        highlight1 = bars.mark_bar(color="blue", opacity=0.2).encode(
            y2=alt.Y2(datum=threshold1)
        ).transform_filter(
            alt.datum.Value > threshold1
        )

        highlight2 = bars.mark_bar(color="yellow").encode(
            y2=alt.Y2(datum=threshold2)
        ).transform_filter(
            alt.datum.Value > threshold2
        )

        highlight3 = bars.mark_bar(color="red").encode(
            y2=alt.Y2(datum=threshold3)
        ).transform_filter(
            alt.datum.Value > threshold3
        )

        rule1 = alt.Chart().mark_rule(size=2).encode(
            y=alt.Y(datum=threshold2)
        )

        label1 = rule1.mark_text(
            x="width",
            dx=-2,
            align="right",
            baseline="bottom",
            fontSize=15,
            text="TIDAK SEHAT",
            color="grey"

        )

        rule2 = alt.Chart().mark_rule(size=2).encode(
            y=alt.Y(datum=threshold3)
        )

        label2 = rule2.mark_text(
            x="width",
            dx=-2,
            align="right",
            baseline="bottom",
            fontSize=15,
            text="SANGAT TIDAK SEHAT",
            color="grey"
        )

        st.altair_chart(bars + highlight1 + highlight2 + highlight3 + rule1 + label1 +rule2 + label2, use_container_width=True)

        left_co, cent_co,last_co = st.columns([1,10,1])
        with cent_co:
            st.write("✨ ISPU fokus pada PM 2.5 yang merupakan partikel"
             " pencemar paling berpengaruh"
             " bagi kesehatan - [DitppuLHK](%s)" % url)
            st.image("data/kategori_ispu.png")


        #dataframe untuk korrelasi
        df2 = pd.read_csv('data/pollute_plb_75_b.csv')

        data = pd.pivot_table(
            data=df2,
            index=['Tanggal'.format(datetime)],
            aggfunc={
                'ISPU_PM_2_5':'max',
                'PM2_5':'max',
                'PM10':'max',
                'Hotspot_harian':'count',
                'Jarak':'mean',
                'Kecerahan_Channel_4':'mean',
                'Kecerahan_Channel_5':'mean',
                'Temperatur':'mean',
                'Curah_Hujan':'mean',
                'Kecepatan_Angin':'mean'
            }
        ).reset_index()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("Korrelasi")
        # st.markdown("<br><br><h4 style='text-align: center; color: red;'>Korrelasi ✨ </h4>", unsafe_allow_html=True)
        tab4, tab5 = st.tabs(['Korrelasi PM2.5', 'Korrelasi Hotspot'])

        #korrelasi pm2_5 dengan jarak, curah hujan, kecepatan angin
        with tab4:
            jarak_hs, hujan_hs, angin_hs = st.columns(3)

            with jarak_hs:
                st.markdown("<h5 style='text-align: center; color: white;'>Jarak Hs rata2 (km) dan ISPU PM 2.5 Harian</h5>", unsafe_allow_html=True)
                scatter2 = alt.Chart(data).mark_point().encode(
                    x="Jarak:Q",
                    y="ISPU_PM_2_5:Q",
                )

                st.altair_chart(scatter2, theme='streamlit',  use_container_width=True)

            with hujan_hs:
                st.markdown("<h5 style='text-align: center; color: white;'>Presipitasi rata2 (mm) dan ISPU PM 2.5 Harian</h5>", unsafe_allow_html=True)
                scatter = alt.Chart(df2).mark_point().encode(
                    x="Curah_Hujan:Q",
                    y="ISPU_PM_2_5:Q",
                )

                st.altair_chart(scatter, theme='streamlit',  use_container_width=True)

            with angin_hs:
                st.markdown("<h5 style='text-align: center; color: white;'>Angin rata2 (m/dtk) dan ISPU PM 2.5 Harian</h5>", unsafe_allow_html=True)
                scatter = alt.Chart(df2).mark_point().encode(
                    x="Kecepatan_Angin:Q",
                    y="ISPU_PM_2_5:Q",
                )

                st.altair_chart(scatter, theme='streamlit',  use_container_width=True)


            #korrelasi dengan pm2_5 dengan temperatur, kecerahan channel 4 dan 5
            temp_hs, bright4_hs , bright5_hs = st.columns(3)

            with temp_hs:
                st.markdown("<h5 style='text-align: center; color: white;'>Temperatur rata2 (C) dan ISPU PM 2.5 Harian</h5>", unsafe_allow_html=True)
                scatter2 = alt.Chart(data).mark_point().encode(
                    x="Temperatur:Q",
                    y="ISPU_PM_2_5:Q",
                    color=alt.Color("Temperatur:Q", scale=alt.Scale(scheme='reds'), legend=alt.Legend(orient="bottom"))
                )

                st.altair_chart(scatter2, theme='streamlit',  use_container_width=True)

            with bright4_hs:
                st.markdown("<h5 style='text-align: center; color: white;'>Hs Channel 4 rata2 (K)  dan ISPU PM 2.5 Harian</h5>", unsafe_allow_html=True)
                scatter = alt.Chart(data).mark_point().encode(
                    x="Kecerahan_Channel_4:Q",
                    y="ISPU_PM_2_5:Q",
                    color=alt.Color("Kecerahan_Channel_4:Q", scale=alt.Scale(scheme='reds'), legend=alt.Legend(orient="bottom"))
                )

                st.altair_chart(scatter, theme='streamlit',  use_container_width=True)

            with bright5_hs:
                st.markdown("<h5 style='text-align: center; color: white;'>Hs Channel 5 rata2 (K) dan ISPU PM 2.5 Harian</h5>", unsafe_allow_html=True)
                scatter = alt.Chart(data).mark_point().encode(
                    x="Kecerahan_Channel_5:Q",
                    y="ISPU_PM_2_5:Q",
                    color=alt.Color("Kecerahan_Channel_5:Q", scale=alt.Scale(scheme='reds'), legend=alt.Legend(orient="bottom"))
                )

                st.altair_chart(scatter, theme='streamlit',  use_container_width=True)

        with tab5:
            # korrelasi jumlah hotspot dengan curah hujan, temperatur

            hujan_hss, angin_hss = st.columns(2)
            with hujan_hss:
                st.markdown("<h5 style='text-align: center; color: white;'>Presipitasi rata2 (mm) dan Jumlah Hotspot Harian</h5>", unsafe_allow_html=True)
                scatter = alt.Chart(data).mark_point().encode(
                    x="Curah_Hujan:Q",
                    y="Hotspot_harian:Q",
                )

                st.altair_chart(scatter, theme='streamlit',  use_container_width=True)

            with angin_hss:
                st.markdown("<h5 style='text-align: center; color: white;'>Kecepatan Angin rata2 (C) dan Jumlah Hotspot Harian</h5>", unsafe_allow_html=True)
                scatter2 = alt.Chart(data).mark_point().encode(
                x="Kecepatan_Angin:Q",
                y="Hotspot_harian:Q",
                 )

                st.altair_chart(scatter2, theme='streamlit',  use_container_width=True)


            temp_hss, bright4_hss, bright5_hss = st.columns(3)
            with temp_hss:
                st.markdown("<h5 style='text-align: center; color: white;'>Temperatur rata2 (C) dan Jumlah Hotspot Harian</h5>", unsafe_allow_html=True)
                scatter2 = alt.Chart(data).mark_point().encode(
                    x="Temperatur:Q",
                    y="Hotspot_harian:Q",
                    color=alt.Color("Temperatur:Q", scale=alt.Scale(scheme='reds'), legend=alt.Legend(orient="bottom") )
                )

                st.altair_chart(scatter2, theme='streamlit',  use_container_width=True)

            with bright4_hss:
                st.markdown("<h5 style='text-align: center; color: white;'>Temperatur rata2 (C) dan Hs Channel 4 (K) rata2 Harian</h5></h5>",unsafe_allow_html=True)
                scatter = alt.Chart(data).mark_point().encode(
                    x="Temperatur:Q",
                    y="Kecerahan_Channel_4:Q",
                color=alt.Color("Kecerahan_Channel_4:Q", scale=alt.Scale(scheme='reds'), legend=alt.Legend(orient="bottom") )
                )

                st.altair_chart(scatter, use_container_width=True)

            with bright5_hss:
                st.markdown("<h5 style='text-align: center; color: white;'>Temperatur rata2 (C) dan Hs Channel 5 rata2 (K) Harian</h5>",unsafe_allow_html=True)
                scatter2 = alt.Chart(data).mark_point().encode(
                    x="Temperatur:Q",
                    y="Kecerahan_Channel_5:Q",
                    color=alt.Color("Kecerahan_Channel_5:Q", scale=alt.Scale(scheme='reds'), legend=alt.Legend(orient="bottom") )
                )

                st.altair_chart(scatter2, theme='streamlit', use_container_width=True)

with st.container(border=True):
    st.subheader("Insight")
    st.markdown(
            "<h4 style='text-align: center; color: red;'>Partikel Kecil Mengancam Generasi Masa Depan Indonesia</h4>",
            unsafe_allow_html=True)
    st.write("Particulate Matter (PM2.5) adalah partikel udara yang berukuran lebih kecil dari atau sama dengan 2.5 µm (mikrometer).\n"
             "PM2.5 berbahaya bagi orang-orang dari segala usia namun sangat berbahaya bagi anak-anak. \n"
             "Dibandingkan orang dewasa, tubuh anak-anak lebih rentan terhadap polusi PM2.5 ini. \n " 
             "Partikel kecil ini dapat menyebabkan banyak dampak negatif terhadap kesehatan \n" 
             "pada anak termasuk asma, penurunan volume otak, disfungsi perilaku, ADHD, Autism Spectrum Disorder (ASD), \n"
             "dan gangguan pertumbuhan paru-paru. \n"
             "Paparan seorang ibu terhadap PM2.5 selama kehamilannya meningkatkan risiko kelahiran prematur, \n" 
             " berat badan lahir rendah, dan lahir mati.")
    st.write("Mengingat kepentingan tersebut di atas maka perlu dilakukan antara lain: "
             " - Langkah Pencegahan ini yang paling penting!: Menggunakan sumber daya  yang tersedia meng-edukasi masyarakat dan membuat payung-payung hukum yang lengkap dan detail yang untuk mencegah terjadinya kebakaran hutan lahan baik yang disengaja maupun tidak disengaja (99% disengajakan oleh manusia menurut BNPB). Kemudian belajar lagi dari propinsi tentangga untuk pencegahan kebakaran hutan lahan."
             " - Langkah Kesiapsiagaan: Menyiapkan alat pelindung, pengobatan, pangan yang cukup. Juga menyiapkan kurikulum-kurikulum untuk belajar daring jika diperlukan ketika terjadi kekeringan dan diikuti bencana Karhutla lagi, untuk melindungi Generasi Masa Depan, juga penyiapan mitigasi dan evakuasi bencana yang diperlukan."
             " - Langkah Kedaruratan dan Pemulihan: Mengerahkan sumber daya yang ada dalam hal pemadaman, pembuatan saluran-saluran air yang memadai, serta sarana dan prasarana lain yang mendukung kedaruratan dan pemulihan bencana.")

with st.container(border=True):
    st.write("✨ Untuk Korrelasi: Data Jarak dan Kecerahan Hotspot dihitung dalam radius maksimal 75km Kota Palembang, menyesuaikan dengan Data Temperatur, Presipitasi, serta Kecepatan Angin, yang Stasiun dan Akurasi Pengukurannya Berada di Sekitar Kota Palembang")
with st.container(border=True):
    st.markdown("* Sumber Data: [KemenLHK](%s)" % urllhk + ", "
             "[FIRMS NASA](%s)" % urlfirms + ", "
             "[Open Weather Map](%s)" % urlopenwea + ", "
             "[BMKG](%s)" % urlbmkg + ", "
             "[Boston College](%s)" % urlboston + ", "
             "[Nafas Indonesia](%s)" % urlnafas + ", "
             "[OTC Digest](%s)" % urlotc + ", "
             "[Halodoc](%s)" % urlhalodoc + ", "
             "[Kompas TV](%s)" % urlkompastv + ", "
             "[Liputan 6 SCTV](%s)" % urlsctv, unsafe_allow_html=True)

with main_cl:
#tab lain utk peta diloading paling akhir
        with tab2:
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
                        get_color='[200, 30, 0, 200]',
                        get_radius=300,
                    ),
                ],
            ))

        with tab3:
            df3 = gpd.read_file('data/idn.geojson')
            df3['lon'] = df3.geometry.x  # extract longitude from geometry
            df3['lat'] = df3.geometry.y  # extract latitude from geometry
            df3 = df3[['lon', 'lat']]  # only keep longitude and latitude

            firms_idn = pd.DataFrame(
                df3,
                columns=['lat', 'lon'])

            st.pydeck_chart(pdk.Deck(
                map_provider='carto',
                map_style='dark',
                views=pdk.View(type="mapview", controller=True),
                initial_view_state=pdk.ViewState(
                    latitude=-3.1952,
                    longitude=117.6524,
                    zoom=3.5,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=firms_idn,
                        get_position='[lon, lat]',
                        get_color='[200, 30, 0, 200]',
                        get_radius=300,
                    ),
                ],
            ))
