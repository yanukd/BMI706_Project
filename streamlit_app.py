import altair as alt
import pandas as pd
import streamlit as st


### P1.2 ###

@st.cache
def load_data():
    # import std data
    std_df = pd.read_csv('https://raw.githubusercontent.com/YoyoMan0414/BMI706_Project/main/STD_by_state.csv')
    # import social determinants data
    sdh_df = pd.read_csv('https://raw.githubusercontent.com/YoyoMan0414/BMI706_Project/main/SD_health.csv')

    # convert object data type to numeric
    std_df['Cases'] = pd.to_numeric(std_df['Cases'].str.replace(',', ''), errors='coerce')
    std_df['Rate per 100000'] = pd.to_numeric(std_df['Rate per 100000'], errors='coerce')
    sdh_df['Numerator'] = pd.to_numeric(sdh_df['Numerator'].str.replace(',', ''), errors='coerce')

    # pivot table
    # STD Table
    pivoted_std_df = std_df.pivot(index=['FIPS', 'Geography', 'Year'], columns='Indicator',
                                  values=['Cases', 'Rate per 100000'])

    # Rename the pivoted columns and reset index in a concise way
    pivoted_std_df.columns = [f'{indicator}_{val}'.lower().replace(' ', '_') for val, indicator in
                              pivoted_std_df.columns]
    pivoted_std_df = pivoted_std_df.reset_index()

    # Social Determinants of Health Table
    pivoted_sdh_df = sdh_df.pivot(index=['FIPS', 'Geography', 'Year'], columns='Indicator',
                                  values=['Numerator', 'Percent'])

    # Rename the pivoted columns and reset index in a concise way
    pivoted_sdh_df.columns = [f'{indicator}_{val}'.lower().replace(' ', '_') for val, indicator in
                              pivoted_sdh_df.columns]
    pivoted_sdh_df = pivoted_sdh_df.reset_index()

    df = pd.merge(pivoted_std_df, pivoted_sdh_df, on=['FIPS', 'Geography', 'Year'], how='left')

    df['Year'] = df['Year'].str.replace(r"\(COVID-19 Pandemic\)", "", regex=True).str.strip()

    return df


# Uncomment the next line when finished
df = load_data()


# ### P1.2 ###
#
#
# st.write("## Age-specific cancer mortality rates")
#
# ### P2.1 ###
# # replace with st.slider
# min_year, max_year = df['Year'].min(), df['Year'].max()
# year = st.slider('Year', min_value=int(min_year), max_value=int(max_year))
# subset = df[df["Year"] == year]
# ### P2.1 ###
#
#
# ### P2.2 ###
# # replace with st.radio
# sex_options = ['M', 'F']
# sex = st.radio('Sex', options=sex_options)
# subset = subset[subset["Sex"] == sex]
# ### P2.2 ###
#
#
# ### P2.3 ###
# # replace with st.multiselect
# # (hint: can use current hard-coded values below as as `default` for selector)
# country_options = df['Country'].unique()
# default_countries = [
#     "Austria",
#     "Germany",
#     "Iceland",
#     "Spain",
#     "Sweden",
#     "Thailand",
#     "Turkey",
# ]
# countries = st.multiselect('Countries', options=country_options, default=default_countries)
# subset = subset[subset["Country"].isin(countries)]
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
