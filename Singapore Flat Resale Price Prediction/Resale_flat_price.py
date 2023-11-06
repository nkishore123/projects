import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler

st.set_page_config(page_title='Copper Modelling',layout='wide')

with st.sidebar:
    option = option_menu(None,options=['Home','Prediction','About'],icons=['house','graph-up','person-vcard-fill'])
if option == 'Home':
    st.title("Welcome")
    col1, col2 = st.columns([1,0.5],gap='small')
    with col1:
        st.write('### :green[Project Name]: Singapore Resale Flat Prices Prediction')
        st.write(
            '### :green[Technologies Used]: Python, Data Preprocessing,EDA, Streamlit')
        st.write('### :green[Domain]: Real Estate')
    with col2:
        st.image('https://condolaunch.sg/wp-content/uploads/sites/177/2023/04/kelvin-zyteng-LMq-rTluKfQ-unsplash-min-1536x1024.jpg')
    st.write("### :green[Overview]: The objective of this project is to develop a machine learning model and deploy it as a user-friendly web application that predicts the resale prices of flats in Singapore. ")
elif option == 'Prediction':
    col1,col2,col3 = st.columns(3)
    with col2:
        st.title(':orange[Singapore Resale Flat Price]')

    town_options = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
       'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
       'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
       'KALLANG/WHAMPOA', 'MARINE PARADE', 'QUEENSTOWN', 'SENGKANG',
       'SERANGOON', 'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN',
       'LIM CHU KANG', 'SEMBAWANG', 'BUKIT PANJANG', 'PASIR RIS',
       'PUNGGOL']
    flat_type_options = ['1 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', '2 ROOM', 'EXECUTIVE',
       'MULTI GENERATION', 'MULTI-GENERATION']
    storey_range_options = ['10 TO 12', '04 TO 06', '07 TO 09', '01 TO 03', '13 TO 15',
       '19 TO 21', '16 TO 18', '25 TO 27', '22 TO 24', '28 TO 30',
       '31 TO 33', '40 TO 42', '37 TO 39', '34 TO 36', '06 TO 10',
       '01 TO 05', '11 TO 15', '16 TO 20', '21 TO 25', '26 TO 30',
       '36 TO 40', '31 TO 35', '46 TO 48', '43 TO 45', '49 TO 51']
    flat_model_options = ['IMPROVED', 'NEW GENERATION', 'MODEL A', 'STANDARD', 'SIMPLIFIED',
       'MODEL A-MAISONETTE', 'APARTMENT', 'MAISONETTE', 'TERRACE',
       '2-ROOM', 'IMPROVED-MAISONETTE', 'MULTI GENERATION',
       'PREMIUM APARTMENT', 'Improved', 'New Generation', 'Model A',
       'Standard', 'Apartment', 'Simplified', 'Model A-Maisonette',
       'Maisonette', 'Multi Generation', 'Adjoined flat',
       'Premium Apartment', 'Terrace', 'Improved-Maisonette',
       'Premium Maisonette', '2-room', 'Model A2', 'DBSS', 'Type S1',
       'Type S2', 'Premium Apartment Loft', '3Gen']

    with st.form('form'):
        col1,col2 = st.columns(2,gap='large')
        # ['month', 'floor_area_sqm', 'lease_commence_date', 'year','town', 'flat_type', 'storey_range',flat_model]
        with col1:
            month = st.selectbox('Month',options=[i for i in range(1,13)])
            floor_area_sqm = st.text_input('floor_area_sqm')
            lease_commence_date = st.selectbox('lease_commence_date',placeholder='select',options=[i for i in range(1966,2023)])
            year = st.selectbox('lease_commence_date',options=[i for i in range(1990,2023)])
        with col2:
            town = st.selectbox('town',options=town_options)
            flat_type = st.selectbox('flat_type',options=flat_type_options)
            storey_range = st.selectbox('storey_range',options=storey_range_options)
            flat_model = st.selectbox('flat_model',options=flat_model_options)

            predict = st.form_submit_button('predict selling price')
        try:
            if predict:
                with st.spinner('Getting Price'):
                    with open("C:/Users/kisho/notebooks/Resale_flat_price.pkl",'rb') as f:
                        model = pickle.load(f)
                    with open("C:/Users/kisho/notebooks/town_ohe.pkl", 'rb') as f:
                        town_ohe = pickle.load(f)
                    with open("C:/Users/kisho/notebooks/flat_type_ohe.pkl",'rb') as f:
                        flat_type_ohe = pickle.load(f)
                    with open("C:/Users/kisho/notebooks/storey_range_ohe.pkl",'rb') as f:
                        storey_range_ohe = pickle.load(f)
                    with open("C:/Users/kisho/notebooks/flat_model_ohe.pkl",'rb') as f:
                        flat_model_ohe = pickle.load(f)
                    with open("C:/Users/kisho/notebooks/Resale_flat_scaler.pkl",'rb') as f:
                        scaler = pickle.load(f)

                    town = town_ohe.transform([[town]]).toarray()
                    flat_type = flat_type_ohe.transform([[flat_type]]).toarray()
                    storey_range = storey_range_ohe.transform([[storey_range]]).toarray()
                    flat_model = flat_model_ohe.transform([[flat_model]]).toarray()

                    month = np.array([[month]])
                    floor_area_sqm = np.array([[floor_area_sqm]])
                    lease_commence_date = np.array([[lease_commence_date]])
                    year = np.array([[year]])

                    x = np.concatenate(
                        [month, floor_area_sqm, lease_commence_date, year, town, flat_type, storey_range, flat_model],
                        axis=1)
                    x = scaler.transform(x)
                    prediction = model.predict(x)[0]
                    st.markdown(f'### The Selling Price is :green[{prediction}]')
        except:
            st.error("Enter valid details")
else:
    st.title(':technologist: About')

    st.write('## :red[Name]: Kishorekumar Nadipena')
    st.write(
        '### :red[LinkedIn]: kishorekumar-nadipena :link: [link](https://www.linkedin.com/in/kishorekumar-nadipena/)')
    st.write('### :red[github]: github.com/nkishore123 :link: [link](https://github.com/nkishore123)')