import altair as alt
import pandas as pd
import streamlit as st


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

    combined_df = pd.concate([std_df, sdh_df], ignore_index=True)

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
countries = st.multiselect('Countries', options=country_options, default=country_options)
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
std = st.selectbox('STD', options=std_options)
subset_std = subset[subset["Indicator"] == std]

# multiselect social determinants
sdh_options = ['Households living below the federal poverty level',
               'Population 25 years and older w/o HS diploma',
               'Uninsured',
               'Vacant housing']
sdh = st.selectbox('Social Determinants', options=sdh_options)
subset_sdh = subset[subset["Indicator"] == sdh]
# ### P2.3 ###
#
#
# ### P2.4 ###
# # replace with st.selectbox
# cancer_options = df['Cancer'].unique()
# cancer = st.selectbox('Cancer', options=cancer_options)
# subset = subset[subset["Cancer"] == cancer]
# ### P2.4 ###
#
#
# ### P2.5 ###
# ages = [
#     "Age <5",
#     "Age 5-14",
#     "Age 15-24",
#     "Age 25-34",
#     "Age 35-44",
#     "Age 45-54",
#     "Age 55-64",
#     "Age >64",
# ]
#
# scale_domain = [0.01, 1000]
#
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
