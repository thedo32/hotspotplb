import altair as alt
import folium
import pandas as pd
import plotly.express as px
import pydeck as pdk
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster
from streamlit_float import *
from streamlit_folium import st_folium
from folium.plugins import LocateControl
import fungsi as fu

st.set_page_config(
    page_title="Forest Fire Hotspots and Air Pollution",
    page_icon="fishtail.png",
    layout="wide",
    menu_items={"About": """##### Impact of Hotspots on October 2023 of El Nino Season Toward Future Generations. 
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

firm = pd.read_csv('data/hotspot_sumsel.csv')
firm_prev = pd.read_csv('data/hotspot_sumsel_2022.csv')
bmkg = pd.read_csv('data/presipitasi_temp_plb.csv')
firmhs = 78759
firmhs_prev = 4928
sumselhs = len(firm.index)
sumselhs_prev = len(firm_prev.index)

# tahun sebelumnya dan sekarang
dt_prev = min(bmkg['date'])
dt_now = max(bmkg['date'])

# temperatur sebelumnya dan sekarang
t_prev = bmkg['t_avg'][bmkg['date'] == dt_prev]
t_now = bmkg['t_avg'][bmkg['date'] == dt_now]
t_avg_prev = t_prev.mean(axis=0)
t_avg_now = t_now.mean(axis=0)

# presipitasi sebelumnya dan sekarang
rr_prev = bmkg['rr_avg'][bmkg['date'] == dt_prev]
rr_now = bmkg['rr_avg'][bmkg['date'] == dt_now]
rr_avg_prev = rr_prev.mean(axis=0)
rr_avg_now = rr_now.mean(axis=0)

# st.markdown("<h1 style='text-align: center; color: #0B60B0;'> Impact of Hotspots on October 2023 of El Nino Season"
#              " <br> Toward Future Generations<br><br></h1>", unsafe_allow_html=True)
fu.stylemd("<h1 style='text-align: center; color: #0B60B0;'> Impact of Hotspots on October 2023 of El Nino Season"
            " <br> Toward Future Generations<br><br></h1>")


# perbedaan hs tahun sebelumnya dan sekarang
idn_diff = 100.0 * ((firmhs - firmhs_prev) / firmhs_prev)
hs_diff = 100.0 * ((sumselhs - sumselhs_prev) / sumselhs_prev)
t_diff = 100.0 * ((t_avg_now - t_avg_prev) / t_avg_prev)
rr_diff = 100.0 * ((rr_avg_now - rr_avg_prev) / t_avg_prev)


st.subheader("Introduction")

with st.container(border=True):
    col_idn, col_hotspot, col_temp, col_presip = st.columns(4)  # add four columns

    with col_idn:
        st.metric("Hotspot Indonesia", value=fu.format_big_number(firmhs), delta=f'{fu.format_big_number(idn_diff)}%',
                  delta_color="off")

    with col_hotspot:
        st.metric("Hotspot South Sumatra Province", value=fu.format_big_number(sumselhs), delta=f'{fu.format_big_number(hs_diff)}%',
                  delta_color="off")

    with col_temp:
        st.metric("Avg Temperature South Sumatra Prov.", value=fu.format_big_number(t_avg_now) + " C", delta=f'{t_diff:.2f}%',
                  delta_color="off")

    with  col_presip:
        st.metric("Avg Precipitation South Sumatra Prov.", value=fu.format_big_number(rr_avg_now) + " mm", delta=f'{rr_diff:.2f}%',
                  delta_color="off")

left_cl, main_cl = st.columns([1, 8])
with left_cl:
    st.page_link("https://hotspotplb.streamlit.app/", label="Indonesia", icon="🏠")
    containup = st.container()
    containup.float()
    containup.markdown("[↗️⬆️↖️](#introduction)", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h5 style='text-align: left; color: #0B60B0;'>Section:</h5>", unsafe_allow_html=True)
        st.markdown("""
        - [Map](#forest-fire-hotspot-propagation-map-october-2023)
        - [Diagram](#pollution-standard-index-chart-october-2023)
        - [Corr.](#correlation)
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
        st.markdown("**Background:**<br>"
                     "According to data from [SIPONGI KLHK](%s)" % urlsipongi + " and [FIRMS NASA](%s)" % urlfirms + " "
                                                                                                           "October 2023, in the :blue region [South Sumatra Province] which has a population of 8.6 million people (BPS 2022),"
                                                                                                           "and has a developing metropolitan area, namely Paturaya Agung, which has a population of 2.6 million people (BPS 2020),"
                                                                                                           "especially :blue [Palembang City with a population of around 1.7 million people] (BPS 2022),"
                                                                                                           "There are :blue [most] hotspots of Land Forest Fire Disaster incidents compared to other provinces in Indonesia, which are exacerbated by the El Nino phenomenon. <br>"
                                                                                                           "**Analysis Focus:**<br>"
                                                                                                           "The author focuses on conducting analysis in Palembang City, not only because it is the most populous area in South Sumatra Province, "
                                                                                                          "but also because of data such as temperature and precipitation,"
                                                                                                           " and wind speed were obtained from BMKG, whose stations and measurement accuracy are located around Palembang."
                                                                                                           "Apart from that, the focus of the analysis is also on October, which is the peak of the 2023 El Nino season.<br>"
                                                                                                           "**El Nino Peak Month:**<br> " ""
                                                                                                           "Under normal conditions the rainy season starts in October,"
                                                                                                           "however, according to BMKG data, :blue[high temperature, very low precipitation] occur in October 2023. Also based on historical Sipongi Data Matrix where "
                                                                                                           ":blue[forest fires often peak in October in the year El Nino occurs].<br> "
                                                                                                           "This condition results in exposure to haze pollution which results in :blue[high risks to the community,"
                                                                                                           "especially in vulnerable groups such as children and pregnant women] which can threaten :blue[Future Generation]",
                    unsafe_allow_html=True)

        st.write("Indonesian Hotspot Matrix Data from the KLHK Sipongi Site")
        st.image('img/data_matrix_sipongi.png', use_column_width=True)

        # links sumber bacaan
        st.caption("Further Reading: [BNPB](%s)" % urlbnpb + ", "
                                                                        "[Boston College](%s)" % urlboston + ", "
                                                                                                             "[Nafas Indonesia](%s)" % urlnafas + ", "
                                                                                                                                                  "[OTC Digest](%s)" % urlotc + ", "
                                                                                                                                                                                "[Halodoc](%s)" % urlhalodoc + ", "
                                                                                                                                                                                                               "[Kompas TV](%s)" % urlkompastv + ", "
                                                                                                                                                                                                                                                 "[Liputan 6 SCTV](%s)" % urlsctv,
                   unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader('Forest Fire Hotspot Propagation Map October 2023')

        # tab untuk peta 3 wilayah administrasi
        tab1a, tab1b, tab1c, tab1d, tab1e = st.tabs(
            ['Palembang City', 'South Sumatera Province', 'Indonesia', 'Indonesia Bubble', 'Indonesia Folium Popup'])

        with tab1a:
            sl1, sl2 = st.columns([1, 4])
            with sl1:
                values = st.slider(
                    'Hotspot Propagation Radius (Km)', value=50, min_value=25, max_value=75, step=25)
                if values == 25:
                    df1 = pd.read_csv('maps/palembang25.csv')
                    bubbletext = [{"text": "438", "lat": -3.47, "lon": 105.96}]
                if values == 50:
                    df1 = pd.read_csv('maps/palembang50.csv')
                    bubbletext = [{"text": "2142", "lat": -3.47, "lon": 105.96}]
                if values == 75:
                    df1 = pd.read_csv('maps/palembang75.csv')
                    bubbletext = [{"text": "6194", "lat": -3.47, "lon": 105.96}]

            st.pydeck_chart(pdk.Deck(
                map_provider='carto',
                map_style='dark',
                views=pdk.View(type="mapview", controller=True),
                initial_view_state=pdk.ViewState(
                    latitude=-2.9831,
                    longitude=104.7527,
                    zoom=8,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df1,
                        get_position='[Longitude, Latitude]',
                        get_color='[91, 163, 207, 200]',
                        get_radius=300,
                        pickable=True,
                    ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=bubbletext,
                        get_position='[lon, lat]',
                        get_color='[91, 163, 207, 200]',
                        get_radius=6000,
                    ),
                    pdk.Layer(
                        'TextLayer',
                        data=bubbletext,
                        get_position='[lon, lat]',
                        gettext='[text]',
                        getSize=12,
                    ),
                ],
            ))

        # load dataframe
        df = pd.read_csv('data/max_hs_pl_palembang_distinct_en.csv')
        df0 = pd.read_csv('data/max_distinct_pm25_plb_oct_2023_en.csv')
        df1 = pd.read_csv('data/max_distinct_pm25_plb_oct_2022_en.csv')
        df2 = pd.read_csv('data/max_distinct_pm25_plb_aug_2023_en.csv')
        df3 = pd.read_csv('data/max_distinct_pm25_plb_dec_2023_en.csv')

        with st.expander("Map Analysis"):
            st.markdown("Can be seen: blue [around Palembang City there are many hotspots],"
                         "if we look at the South Sumatra Province region, there are more hotspots in the area."
                         ":blue[southeast part of the province and not far from the provincial capital]."
                         "Overall on Indonesia map, the hotspot brightness seems almost the same in several regions,"
                         "Then if you look at the Indonesia Bubble map"
                         "in South Sumatra there are 15,848 hotspots, :blue [the most hotspots compared to other provinces],"
                         "follow by Central Kalimantan province which has 13,393 hotspots, out of 78,759 total hotspots in Indonesia.<br><br>",
                        unsafe_allow_html=True)

        st.subheader("Pollution Standard Index Chart October 2023")

        tabBar, tabArc = st.tabs(['Pollution Standard Status of PM 2.5', 'Percentage'])
        with tabBar:
            colLBar, colBar, colRBar = st.columns([1, 20, 1])
            with colBar:
                banding = st.checkbox('Comparison', value=False)
                if banding:
                    bars = alt.Chart(df).mark_bar(size=24).encode(
                        y="Status:O",
                        x=alt.X("count(Value):Q", title="Jumlah Hari"),
                        row="Bulan:N",
                        color=alt.Color("max(Color):N", scale=None)
                    ).properties(height=72, width=600).interactive(bind_x=True, bind_y=True)
                    st.altair_chart(bars)
                else:
                    bars = alt.Chart(df0).mark_bar(size=25).encode(
                        y="Status:O",
                        x=alt.X("count(Value):Q", title="Jumlah Hari"),
                        color=alt.Color("max(Color):N", scale=None)
                    ).properties(height=200, width=800).interactive()
                    st.altair_chart(bars)

                # st.write("Tabel Status ISPU")
                # bars = alt.Chart(dfispu).mark_bar(size=15).encode(
                #             y=alt.X("Status", axis=alt.Axis(labels=False)),
                #             x=alt.Y("Keterangan", axis=alt.Axis(labels=False)),
                #             color=alt.Color("Color:N", scale=None)
                #         ).properties(width=720)
                #
                # text = alt.Chart(dfispu).mark_text(
                #             align='left',
                #             dx=2,
                #             fontSize=13,
                #             color="#F0EDCF",
                #         ).encode(
                #             y=alt.X("Status", axis=alt.Axis(labels=False)),
                #             x=alt.Y("Keterangan", axis=alt.Axis(labels=False)),
                #             text=alt.Y("Text"),
                #         )
                #
                # st.altair_chart(bars + text, use_container_width=True)
                st.image("img/poll_index.png", use_column_width=True)

        with tabArc:
            colLArc, colArc1, colArc2, colRArc = st.columns([1, 9, 9, 1])
            with colArc1:
                okt23 = st.checkbox('October 2023', value=True)
                if okt23:
                    base = alt.Chart(df0).mark_arc(innerRadius=50, outerRadius=105).encode(
                        alt.Color("Persentase:O").legend(None),
                        alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                        # color=alt.Color("max(Color)", scale=None)
                    ).properties(height=300, width=300).interactive()

                    text = base.mark_text(radius=148, size=12).encode(text="Status:N")
                    st.altair_chart(base + text, use_container_width=True)

            with colArc2:
                okt22 = st.checkbox('October 2022', value=False)
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
                ags23 = st.checkbox('August 2023', value=False)
                if ags23:
                    base = alt.Chart(df2).mark_arc(innerRadius=30, outerRadius=70).encode(
                        alt.Color("Persentase:O").legend(None),
                        alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                        # color=alt.Color("max(Color)", scale=None)
                    ).properties(height=210, width=210).interactive()

                    text = base.mark_text(radius=90, size=11).encode(text="Status:N")
                    st.altair_chart(base + text, use_container_width=True)

            with colArcs2:
                des23 = st.checkbox('December 2023', value=False)
                if des23:
                    base = alt.Chart(df3).mark_arc(innerRadius=30, outerRadius=70).encode(
                        alt.Color("Persentase:O").legend(None),
                        alt.Theta("count(Value):Q", title="Jumlah Hari").stack(True),
                        # color=alt.Color("max(Color)", scale=None)
                    ).properties(height=210, width=210).interactive()

                    text = base.mark_text(radius=90, size=11).encode(text="Status:N")
                    st.altair_chart(base + text, use_container_width=True)

        with st.expander("Pollution Standard Index Analysis"):
            st.write("Pollution Standard Index analysis focuses on PM 2.5 which is particulate matter"
                      "most influential polluter"
                      " for health - [DitppuLHK](%s)" % url)
            st.markdown(
                "From the diagram above we can see that in Palembang, October 2023, the majority of air pollution status is at the: blue [Unhealthy] level,"
                 "There were even 5 days in that month where the pollution status was at level: blue [Very Unhealthy],"
                 "which can endanger human health conditions, greatly risking the future of children."
                 "By comparing October 2023, which according to the Sipongi KLHK Data Matrix above is the peak period for the occurrence of Land Forest Fires (Karhutla) in 2023, with the previous year in October 2022, with the time when Forest and Land Fires in 2023 had not yet reached their peak in August, with The 2023 forest and land fires will decline in December,"
                 "reinforced by the news in the mass media about the critical condition of the haze in October 2023, it can be said: blue [the haze condition due to forest and land fires is one of the main causes of the worsening ISPU PM 2.5 status]."
                 "In addition to the diagram above, we can see below: blue [Correlation Analysis] Number of Hotspots, Average Distance, Precipitation,"
                 "Wind Speed and Temperature.<br><br>", unsafe_allow_html=True)

        # dataframe untuk korrelasi
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
        st.subheader("Correlation")

        # korrelasi pm2_5 dengan jarak, curah hujan, kecepatan angin

        option = st.selectbox(
            "Select the data you want to correlate with the Daily ISPU PM 2.5",
            ("Correlation Heatmap Data", "Hs Amount and Pollution Index of PM 2.5", "Hs Distance and Pollution Index of PM 2.5",
             "Precipitation and Pollution Index of PM 2.5", "Wind Speed and Pollution Index of PM 2.5",
             "Temperature and Pollution Index of PM 2.5")
        )

        colL1, colM1, colR1 = st.columns([2, 10, 2])

        with colM1:
            if option == "Correlation Heatmap Data":
                # heat = sns.heatmap(dfcorr.corr(),  cmap="Blues", annot=True)
                # st.write(heat.get_figure())
                st.image('img/corrheatmap.png', use_column_width=True)

            if option == "Hs Amount and Pollution Index of PM 2.5":
                scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                    x=alt.X("Jumlah_Hs:Q", title="Hotspot Amount"),
                    y=alt.Y("ISPU:Q", title="Pollution Index of PM 2.5"),
                ).interactive().properties(height=425)

                st.altair_chart(scatter +
                                scatter.transform_regression('Jumlah_Hs', 'ISPU').
                                mark_line(size=3, color="red", opacity=0.3),
                                theme='streamlit', use_container_width=True)

            if option == "Hs Distance and Pollution Index of PM 2.5":
                scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                    x=alt.X("Jarak:Q", title="Average Distance (km)"),
                    y=alt.Y("ISPU:Q", title="Pollution Index of PM 2.5"),
                ).interactive().properties(height=425)

                st.altair_chart(scatter +
                                scatter.transform_regression('Jarak', 'ISPU').
                                mark_line(size=3, color="red", opacity=0.3),
                                theme='streamlit', use_container_width=True)

            if option == "Precipitation and Pollution Index of PM 2.5":
                scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                    x=alt.X("Presipitasi:Q", title="Precipitation (mm)"),
                    y=alt.Y("ISPU:Q", title="Pollution Index of PM 2.5"),

                ).interactive().properties(height=425)

                st.altair_chart(scatter +
                                scatter.transform_regression('Presipitasi', 'ISPU').
                                mark_line(size=3, color="red", opacity=0.3),
                                theme='streamlit', use_container_width=True)

            if option == "Win Speed and Pollution Index of PM 2.5":
                scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                    x=alt.X("Kec_Angin:Q", title="Wind Speed (m/s)"),
                    y=alt.Y("ISPU:Q", title="Pollution Index of PM 2.5"),
                ).interactive().properties(height=425)

                st.altair_chart(scatter +
                                scatter.transform_regression('Kec_Angin', 'ISPU').
                                mark_line(size=3, color="red", opacity=0.3),
                                theme='streamlit', use_container_width=True)

            if option == "Temperature and Pollution Index of PM 2.5":
                scatter = alt.Chart(dfcorr).mark_point(size=50).encode(
                    x=alt.X("Temper:Q", title="Temperature (Celcius)"),
                    y=alt.Y("ISPU:Q", title="Pollution Index of PM 2.5"),
                ).interactive().properties(height=425)

                st.altair_chart(scatter +
                                scatter.transform_regression('Temper', 'ISPU').
                                mark_line(size=3, color="red", opacity=0.3),
                                theme='streamlit', use_container_width=True)

        with st.expander("Correlation Analysis"):
            st.markdown(
                "For ISPU PM 2.5 Correlation, there is :blue [positive correlation] between the number of daily Hotspots and the daily ISPU PM 2.5 value,"
                "Then: blue [negative correlation] with the Average Distance of Hotspots where the Distance is the higher the ISPU PM 2.5 value."
                "Likewise, the correlation of Precipitation, :blue [reduced precipitation or rainfall, the higher the ISPU PM 2.5 value]."
                "Similarly, as the wind speed decreases around Palembang City, the ISPU PM 2.5 value will increase,"
                "The negative relationship also applies to the average temperature of Palembang City with an ISPU PM value of 2.5 <br> "
                "Regarding the correlation of wind speed, temperature with ISPU PM 2.5 shows a negative relationship."
                "It seems that this needs to be investigated further, because as previously mentioned the data was obtained from BMKG, whose stations and measurement accuracy are located around the city of Palembang,"
                "more data needs to be obtained for a wider area than around Palembang City,"
                "Apart from that, it also calculates other parameters such as Wind Direction at Maximum Speed, Most Wind Direction, Humidity, Length of Sunlight."
                "Similarly, we can also analyze further regarding correlations other than ISPU PM 2.5, as depicted in the Heatmap Diagram."
                "The author's hope for the future, both the author and anyone interested in this research, can dig deeper and discuss"
                "again with Geophysical Meteorology and Climatology experts,"
                "and equipped with socio-economic data of the surrounding community, for further research.",
                unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("Insight")
    with st.expander("Tiny Particles Threaten Future Generations"):
        st.markdown(
            "Particulate Matter (PM2.5) is air particles smaller than or equal to 2.5 µm (micrometers)."
             ":blue[PM2.5 is dangerous] for people of all ages and is even very dangerous for children."
             "These small particles can cause many :blue[negative impacts on health"
             "in children including asthma, decreased brain volume, behavioral dysfunction, ADHD, Autism Spectrum Disorder (ASD),"
             "and impaired lung growth]."
             "It's important to think about our children's health when addressing air pollution. Diseases related to air pollution will"
             "impacts children's health throughout their lives."
             "A :blue[mother's exposure to PM2.5 during her pregnancy increases the risk of preterm birth,"
             "low birth weight, and stillbirth].<br>"
             "Air pollution generally starts at 7 am in the morning"
             "when children generally start their learning activities,"
             "when motorized vehicles start to fill the streets and especially when at the same time there is exposure to smoke haze due to forest land fires.<br>"
             "Given the above interests, it is necessary to protect children from the dangers of air pollution:<ul>"
             "<li>To anticipate exposure to air pollution, it is very necessary: blue [children still wear masks], or if the air status becomes very unhealthy or even dangerous, outdoor activities are not possible"
             "then apply :blue[online school activities].</li>"
             "<li>Apart from that, the government must also be determined and mobilize all resources to immediately extinguish land forest fires </li>"
             "<li>Then the most important thing is to take preventive measures, using available resources to :blue[educate the public and make umbrellas"
             "complete and detailed regulation :blue [to prevent the occurrence of land forest fires] whether intentional or unintentional :blue[(99% intentional by humans according to BNPB)],"
             "as well as other policies in an effort to bring clean air to the region. </li></ul> "
             "So that children's exposure to air pollution is greatly reduced, thereby improving the health and intelligence of :blue [Indonesia's Future Generation.] ",
            unsafe_allow_html=True)

fu.stylecapt("Data Source: [KemenLHK](%s)" % urllhk + ", "
                                                        "[FIRMS NASA](%s)" % urlfirms + ", "
                                                                                        "[Open Weather Map](%s)" % urlopenwea + ", "
                                                                                                                                "[BMKG](%s)" % urlbmkg
                )


with main_cl:
    # tab lain utk peta diloading paling akhir
    with tab1b:
        df2 = pd.read_csv('maps/sumsel.csv')
        bubbletext = [{"text": "15848", "lat": -3.47, "lon": 106.139}]

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
                    data=df2,
                    get_position='[Longitude, Latitude]',
                    get_color='[91, 163, 207, 200]',
                    get_radius=300,
                    pickable=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=bubbletext,
                    get_position='[lon, lat]',
                    get_color='[91, 163, 207, 200]',
                    get_radius=12000,
                ),
                pdk.Layer(
                    'TextLayer',
                    data=bubbletext,
                    get_position='[lon, lat]',
                    gettext='[text]',
                    getSize=12,
                ),
            ],
        ))

    with tab1c:
        df = pd.read_csv('maps/idn.csv')

        # Create the choropleth bubble map
        fig = px.scatter_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            size="Jumlah",  # Bubble size based on the "count" attribute
            mapbox_style="carto-darkmatter",  # Choose a suitable projection
            labels={"Jumlah": "Jumlah (Total di Bubble Besar x100)"},
            # hover_name="prov",  # Display count on hover
            color_discrete_sequence=["#5BA3CF"],  # Customize bubble color
            height=600,
            zoom=3.7,
            center=dict(lat=-3.1940, lon=117.5540),  # this will center on the point
        )

        # Show the map
        st.plotly_chart(fig, use_container_width=True)

    with tab1d:
        if st.checkbox("Interactive Folium Map - Slower", value=False):

            # set callback
            callback = """\
                            function (row) {
                                    var icon, marker;
                                    icon = L.AwesomeMarkers.icon({
                                        icon: "fire", iconColor: "#86BCDC", iconSize: [5,5]});
                                    marker = L.marker(new L.LatLng(row[0], row[1]) );
                                    marker.setIcon(icon);
                                    return marker;
                            };
                            """

            # draw basemap
            m = folium.Map(location=[-3.1940, 117.5540],
                           tiles='cartodbdarkmatter',
                           zoom_start=2,
                           control_scale=True,
                           zoom_control="bottomleft",
                           prefer_canvas=True)


            # Get x and y coordinates for each point
            # points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
            # points_gjson.add_to(m)

            # Get x and y coordinates for each point
            points = pd.read_csv('maps/idns.csv')

            # Extract latitude and longitude columns
            locations = list(zip(points["Latitude"], points["Longitude"]))

            # Create a folium marker cluster
            fast_marker_cluster = FastMarkerCluster(locations, callback=callback, control=True)
            LocateControl(auto_start=True)
            fast_marker_cluster.add_to(m)

            # add maps to streamlit
            st_folium(m, height=450, use_container_width=True)

        else:
            df = pd.read_csv('maps/idn_hs_by_prov.csv')
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

    with tab1e:
        # draw basemap
        m = folium.Map(location=[-3.1940, 117.5540],
                       tiles='cartodbdarkmatter',
                       zoom_start=2, control_scale=True)

        if st.checkbox("Show Hotspot? Don't bother, make or order your coffee while loading", value=False, disabled=True):


            # Get x and y coordinates for each point
            # points_gjson = folium.features.GeoJson(points, name="Hotspot Indonesia")
            # points_gjson.add_to(m)
            # Get x and y coordinates for each point
            points = pd.read_csv('maps/idns.csv')

        # Extract latitude and longitude columns
            marker_cluster = MarkerCluster()
            for _, row in points.iterrows():
                popup = f"Latitude: {row['Latitude']}<br>Longitude: {row['Longitude']}"
                folium.Marker([row['Latitude'], row['Longitude']], popup=popup).add_to(marker_cluster)

            marker_cluster.add_to(m)

        # Add maps to streamlit
        st_folium(m, height=450, use_container_width=True, key=123)

        # st.markdown("Sumber Data Peta: [Geojson](%s)" % urlbubble, unsafe_allow_html=True)