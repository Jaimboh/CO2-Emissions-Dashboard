import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

@st.cache_data
def get_countries_data(): 
    url = "https://github.com/alanjones2/CO2/raw/master/data/countries_df.csv"
    return pd.read_csv(url)

@st.cache_data
def get_continent_data():
    url = 'https://github.com/alanjones2/CO2/raw/master/data/continents_df.csv'
    return pd.read_csv(url)

@st.cache_data
def get_world_data():
    url = 'https://github.com/alanjones2/CO2/raw/master/data/world_df.csv'
    return pd.read_csv(url)

@st.cache_data
def get_group_data():
    url = 'https://github.com/alanjones2/CO2/raw/master/data/income_types_df.csv'
    return pd.read_csv(url)

df_countries = get_countries_data()
df_continents = get_continent_data()
df_world = get_world_data()
df_groups = get_group_data()

year = st.slider('Select year', 1850, 2020, 1950)
max_val = df_countries['Annual CO₂ emissions'].max()

fig1 = px.choropleth(df_countries[df_countries['Year'] == year], locations="Code",
                    color="Annual CO₂ emissions",
                    hover_name="Entity",
                    range_color=(0, max_val),
                    color_continuous_scale=px.colors.sequential.Blues)

start_month, end_month = st.select_slider(
    'Select a range of months',
    options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    value=('Jan', 'Dec')
)

st.write('You selected months between', start_month, 'and', end_month)

continents = df_continents['Entity'].unique()
selected_continent = st.selectbox('Select country or group', continents)
df = df_continents.loc[df_continents['Entity'].isin(selected_continent)]
fig2 = px.line(df, "Year", "Annual CO₂ emissions")

selected_continents = st.multiselect('Select country or group', continents, continents)
df = df_continents[df_continents['Year'] >= 2010]
df = df[df_continents['Entity'].isin(selected_continents)]
fig3 = px.bar(df, "Year", "Annual CO₂ emissions", color="Entity", barmode='group')

chart = st.radio(
    "Select the chart that you would like to display",
    ('World Map', 'Continent Emissions', 'Comparing continents')
)

if chart == 'World Map':
    st.plotly_chart(fig1)
elif chart == 'Continent Emissions':
    st.plotly_chart(fig2)
elif chart == 'Comparing continents':
    st.plotly_chart(fig3)



st.title("A Simple CO2 Emissions Dashboard")
st.write("An example of a Streamlit layout using a sidebar")

with st.sidebar:
    st.header('Select a chart to be displayed')
    chart = st.radio(
        "Select the chart that you would like to display",
        ('World Map', 'Continent Emissions', 'Comparing continents')
    )

st.title("A Simple CO2 Emissions Dashboard")
st.info("An example of a Streamlit layout using columns")

with st.container():
    if chart == 'World Map':
        st.header("Global emissions since 1850")
        st.info("Select a year with the slider to see the intensity of emissions change in each country")
        st.plotly_chart(fig1)

with st.container():
    col1, col2 = st.columns((2, 4))

    with col1:
        st.header("Continental emissions since 1850")
        st.info("Select a single continent or compare continents")
        st.plotly_chart(fig2)

    with col2:
        st.header("Comparing continents")
        st.info("To add or remove continents, select them from the menu")
        st.plotly_chart(fig3)

with st.container():
    tab1, tab2 = st.columns(2)

    with tab1:
        st.header("Continental emissions since 1850")
        st.plotly_chart(fig2)

    with tab2:
        st.header("Comparing continents since 1850")
        st.plotly_chart(fig3)
