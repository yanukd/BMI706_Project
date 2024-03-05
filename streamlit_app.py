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
    sdh_df['Year'] = pd.to_numeric(sdh_df['Year'], errors='coerce')
    std_df['Year'] = pd.to_numeric(std_df['Year'], errors='coerce')

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

year_sdh = st.slider('Year', min_value = 2011, max_value=int(max_year))
subset_sdh = df[df["Year"] == year_sdh]
# # st.multiselect countries
# country_options = df['Geography'].unique()
# countries = st.multiselect('Countries', options=country_options)
# # Create a radio button to choose between all countries or only selected
# display_option = st.radio(
#     "Display all countries or only selected countries?",
#     ('All', 'Selected')
# )
# if display_option == 'Selected':
#     # Filter the dataframe for selected countries
#     subset = subset[subset["Geography"].isin(countries)]
# else:
#     # Use the full dataframe
#     subset = subset

#subset = subset[subset["Geography"].isin(countries)]

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
subset_sdh = subset_sdh[subset_sdh["Indicator"].isin(sdh)]

# std map
source = alt.topo_feature(data.us_10m.url, 'states')
std_data = subset_std.groupby(['Geography', 'Year', 'FIPS'])['Cases'].sum().reset_index()

width = 600
height = 300
project = 'albersUsa'

# a gray map using as the visualization background

background = alt.Chart(source
                       ).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)

selector = alt.selection_single(
    # add your code here
    on='click',
    fields=['states']
)

chart_base = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).add_selection(selector
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(std_data, "FIPS", ['Geography','Cases']),
    )
# Map values

num_scale = alt.Scale(domain=[std_data['Cases'].min(), std_data['Cases'].max()], scheme='oranges')
num_color = alt.Color(field="Cases", type="quantitative", scale=num_scale)
std_map = chart_base.mark_geoshape().encode(
    color=num_color,
    tooltip=['Cases:Q', 'Geography:N']
).transform_filter(
    selector
    ).properties(
    title=f'STD Cases in U.S. {year}'
)

map_left = background + std_map
st.altair_chart(map_left, use_container_width=True)


# sdh map
sdh_data = subset_sdh.groupby(['Geography', 'Year', 'FIPS'])['Numerator'].sum().reset_index()

chart_base_sdh = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).add_selection(selector
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(sdh_data, "FIPS", ['Geography','Numerator']),
    )

num_scale = alt.Scale(domain=[sdh_data['Numerator'].min(), sdh_data['Numerator'].max()], scheme='oranges')
num_color = alt.Color(field="Numerator", type="quantitative", scale=num_scale)
sdh_map = chart_base_sdh.mark_geoshape().encode(
    color=num_color,
    tooltip=['Numerator:Q', 'Geography:N']
).transform_filter(
    selector
    ).properties(
    title=f'Social Determinants Numerator in U.S. {year}'
)

map_right = background + sdh_map
st.altair_chart(map_right, use_container_width=True)

# countries_in_subset = subset["Country"].unique()
# if len(countries_in_subset) != len(countries):
#     if len(countries_in_subset) == 0:
#         st.write("No data avaiable for given subset.")
#     else:
#         missing = set(countries) - set(countries_in_subset)
#         st.write("No data available for " + ", ".join(missing) + ".")