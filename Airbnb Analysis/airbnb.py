import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from PIL import Image
import geopandas as gpd

st.set_page_config(page_title='Airbnb Analysis',
                   page_icon=":flight:",
                   layout = "wide",
                   initial_sidebar_state = "expanded")
with st.sidebar:
    option = option_menu(None, ['Home', 'Analysis', 'Map', 'About'],
                         icons=['house', 'graph-up', "globe-central-south-asia", 'gear'],
                         menu_icon="cast", default_index=0, orientation="vertical"
                         )
df = pd.read_csv("C:/Users/Kisho/Datasets/simplified_airbnb.csv")

if option == 'Home':
    st.title("Welcome")
    col1, col2 = st.columns([2,1])
    with col1:
        st.write('### :green[Project Name]: Airbnb Analysis')
        st.write('### :green[Technologies Used]: Python scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, Tableau')
        st.write('### :green[Domain]: Travel Industry, Property Management and Tourism')

    with col2:
        image = Image.open("C:/Users/kisho/Downloads/airbnb.png")
        st.image(image)
    st.write(
        '''### :green[Overview]: This project is about a dashboard that displays information and insights from the Airbnb data in an interactive and visually appealing manner.''')

elif option == 'Analysis':
    with st.sidebar:
        countries = df['country'].unique()
        country = st.multiselect(label='select a country', options=countries)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        all = st.checkbox('All neighbourhoods')
    with col2:
        cities = df[df['country'].isin(country)]['host_neighbourhood'].unique()
        city = st.selectbox(label='select a neighbourhood', options=cities,disabled=all)
    with col3:
        type = st.selectbox(label="select a property",options=['property_type', 'room_type', 'bed_type'])
    with col4:
        measure = st.selectbox(label='select a measure',options=['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating'])
    with col5:
        metric = st.radio(label="Select One",options=['Sum','Avg'])
    if metric == 'Avg':
        a = df.groupby(['host_neighbourhood',type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee', 'review_scores_rating']].mean().reset_index()
    else:
        a = df.groupby(['host_neighbourhood', type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].sum().reset_index()
    if not all:
        b = a[a['host_neighbourhood'] == city]
    else:
        if metric=='Avg':
            a = df.groupby(['country',type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee', 'review_scores_rating']].mean().reset_index()
        else:
            a = df.groupby(['country', type])[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].sum().reset_index()
        b = a[a['country'].isin(country)]
    with st.expander('View Dataframe'):
        st.write(b.style.background_gradient(cmap="Reds"))


    if type == 'property_type' or measure == 'review_scores_rating':
        try:
            b['text'] = b['country'] + '<br>' + b[measure].astype(str)
            fig = px.bar(b, x=type, y=measure, color='country', text='text')
        except:
            b['text'] = b['host_neighbourhood'] + '<br>' + b[measure].astype(str)
            fig = px.bar(b, x=type,y=measure,color=type,text='text')
        st.plotly_chart(fig,use_container_width=True)
    elif type == 'bed_type':
        fig = px.pie(b, names=type, values=measure, color=measure,hole=0.5)
        fig.update_traces(textposition='outside', textinfo='label+percent')
        st.plotly_chart(fig, use_container_width=True)
    # ['label', 'text', 'value', 'percent']

    else:
        fig = px.pie(b, names=type, values=measure, color=measure)
        fig.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig, use_container_width=True)
elif option == 'Map':
    with st.sidebar:
        measure = st.selectbox(label='select a measure', options=['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price','cleaning_fee', 'review_scores_rating'])

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    merged_data = pd.merge(world, df, left_on='name', right_on='country', how='inner')

    a = merged_data.groupby('country')[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].mean().reset_index()
    b = merged_data.groupby('country')['iso_a3'].first()
    c = pd.merge(a,b,left_on='country', right_on='country', how='inner')
    fig = px.choropleth(c,
                        locations='iso_a3',
                        color=measure,
                        hover_name='country',
                        projection='natural earth', # 'natural earth','equirectangular', 'mercator', 'orthographic', 'azimuthal equal area'
                        color_continuous_scale='YlOrRd')
    fig.update_layout(
        title=f'Avg {measure}',
        geo=dict(
            showcoastlines=True,
            coastlinecolor='Black',
            showland=True,
            landcolor='white'
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    a = merged_data.groupby('country')[['bedrooms', 'beds', 'number_of_reviews', 'bathrooms', 'price', 'cleaning_fee','review_scores_rating']].sum().reset_index()
    b = merged_data.groupby('country')['iso_a3'].first()
    c = pd.merge(a, b, left_on='country', right_on='country', how='inner')
    fig = px.choropleth(c,
                        locations='iso_a3',
                        color=measure,
                        hover_name='country',
                        projection='natural earth',
                        # 'natural earth','equirectangular', 'mercator', 'orthographic', 'azimuthal equal area'
                        color_continuous_scale='YlOrRd')
    fig.update_layout(
        title=f'Total {measure}',
        geo=dict(
            showcoastlines=True,
            coastlinecolor='Black',
            showland=True,
            landcolor='white'
        )
    )
    st.plotly_chart(fig, use_container_width=True)

elif option == 'About':
    st.title(':technologist: About')

    st.write('## :red[Name]: Kishorekumar Nadipena')
    st.write('### :red[LinkedIn]: kishorekumar-nadipena :link: [link](https://www.linkedin.com/in/kishorekumar-nadipena/)')
    st.write('### :red[github]: github.com/nkishore123 :link: [link](https://github.com/nkishore123)')