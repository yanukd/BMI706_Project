import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data


### P1.2 ###

@st.cache_data
def load_data():
    # import std data
    std_df = pd.read_csv('https://raw.githubusercontent.com/YoyoMan0414/BMI706_Project/main/STD_by_state.csv')
    # import social determinants data
    sdh_df = pd.read_csv('https://raw.githubusercontent.com/YoyoMan0414/BMI706_Project/main/SD_health.csv')

    # convert object data type to numeric
    std_df['Cases'] = pd.to_numeric(std_df['Cases'].str.replace(',', ''), errors='coerce')
    std_df['Rate per 100000'] = pd.to_numeric(std_df['Rate per 100000'], errors='coerce')
    sdh_df['Numerator'] = pd.to_numeric(sdh_df['Numerator'].str.replace(',', ''), errors='coerce')

    std_df['Year'] = std_df['Year'].str.replace(r"\(COVID-19 Pandemic\)", "", regex=True).str.strip()
    sdh_df['Year'] = sdh_df['Year'].str.replace(r"\(COVID-19 Pandemic\)", "", regex=True).str.strip()

    combined_df = pd.concat([std_df, sdh_df], ignore_index=True)

    return combined_df


# load data
df = load_data()

# title
st.write("## STD Dashboard")
#
# replace with st.slider
min_year, max_year = df['Year'].min(), df['Year'].max()
year = st.slider('Year', min_value=int(min_year), max_value=int(max_year))
subset = df[df["Year"] == year]

# st.multiselect countries
country_options = df['Geography'].unique()
countries = st.multiselect('Countries', options=country_options)
# Create a radio button to choose between all countries or only selected
display_option = st.radio(
    "Display all countries or only selected countries?",
    ('All', 'Selected')
)
if display_option == 'Selected':
    # Filter the dataframe for selected countries
    subset = subset[subset["Geography"].isin(countries)]
else:
    # Use the full dataframe
    subset = subset

# st.multiselect std types
std_options = ['Chlamydia',
               'Congenital Syphilis',
               'Early Non-Primary, Non-Secondary Syphilis',
               'Gonorrhea',
               'Primary and Secondary Syphilis']
std = st.multiselect('STD', options=std_options, default = std_options)
subset_std = subset[subset["Indicator"].isin(std)]

# multiselect social determinants
sdh_options = ['Households living below the federal poverty level',
               'Population 25 years and older w/o HS diploma',
               'Uninsured',
               'Vacant housing']
sdh = st.multiselect('Social Determinants', options=sdh_options, default = sdh_options)
subset_sdh = subset[subset["Indicator"].isin(sdh)]

# std map
source = alt.topo_feature(data.world_110m.url, 'countries')

width = 600
height = 300
project = 'equirectangular'

# a gray map using as the visualization background
# std_data = subset_std.groupby('Geography')['Numerator'].sum().reset_index()

background = alt.Chart(source
                       ).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)

# selector = alt.selection_single(
#     # add your code here
#     on='click',
#     fields=['Country']
# )

chart_base = alt.Chart(source).properties(
    width=width,
    height=height
).project(project
          ).transform_lookup(
    lookup="id",
    from_=alt.LookupData(subset_std, 'FIPS', ['Geography','Cases']),
).properties(
    title='STD cases worldwide in {year}'
)
# Map values
num_scale = alt.Scale(domain=[subset_std['Cases'].min(), subset_std['Cases'].max()])
num_color = alt.Color('Cases:Q', scale=num_scale)
std_map = chart_base.mark_geoshape().encode(
    color=num_color,
    tooltip=['Cases:Q', 'Geography:N']
)

map_left = background + std_map
st.altair_chart(map_left, use_container_width=True)

# chart = alt.Chart(subset).mark_rect().encode(
#     x=alt.X("Age:O", sort=ages),
#     y=alt.Y("Country:N"),
#     color=alt.Color("Rate:Q", scale=alt.Scale(type='log', domain=scale_domain, clamp=True)),
#     tooltip=["Country", "Age", "Rate"]
# ).properties(
#     title=f"{cancer} mortality rates for {'males' if sex == 'M' else 'females'} in {year}",
# )
#
# # population bar chart
# population = subset.groupby('Country')['Pop'].sum().reset_index()
# chart2 = alt.Chart(population).mark_bar().encode(
#     x=alt.X("Pop:Q", title="Sum of popukation size"),
#     y=alt.Y("Country:N", sort='-x'),
#     tooltip=["Country", "Pop"]
# )
# ### P2.5 ###
#
# st.altair_chart(chart, use_container_width=True)
#
# st.altair_chart(chart2, use_container_width=True)
#
# countries_in_subset = subset["Country"].unique()
# if len(countries_in_subset) != len(countries):
#     if len(countries_in_subset) == 0:
#         st.write("No data avaiable for given subset.")
#     else:
#         missing = set(countries) - set(countries_in_subset)
#         st.write("No data available for " + ", ".join(missing) + ".")
