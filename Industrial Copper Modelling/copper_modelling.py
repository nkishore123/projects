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
        st.write('### :green[Project Name]: Industrial Copper Modeling')
        st.write(
            '### :green[Technologies Used]: Python scripting, Data Preprocessing,EDA, Streamlit')
        st.write('### :green[Domain]: Manufacturing')
    with col2:
        st.image('https://thumbs.dreamstime.com/b/d-illustration-copper-as-element-periodic-table-grey-illuminated-atom-design-background-orbiting-electrons-shows-name-179569453.jpg')
    st.write("### :green[Overview]: This is a machine learning project which consists both regression and classification models "
             "to predict either selling price or status based on user's choice. A user can choose between regression and classifier, give the required fields to predict the outcome.")
elif option == 'Prediction':
    st.title(':green[Industrial Copper Modelling]')
    tab1,tab2 = st.tabs(['Regression','Classification'])
    product_refs = [1670798778, 1668701718, 628377, 640665, 611993,
                    1668701376, 164141591, 1671863738, 1332077137, 640405,
                    1693867550, 1665572374, 1282007633, 1668701698, 628117,
                    1690738206, 628112, 640400, 1671876026, 164336407,
                    164337175, 1668701725, 1665572032, 611728, 1721130331,
                    1693867563, 611733, 1690738219, 1722207579, 929423819,
                    1665584320, 1665584662, 1665584642]
    countries = [28, 25, 30, 32, 38, 78, 27, 77, 113, 79, 26, 39, 40, 84, 80, 107, 89]
    with tab1:
        with st.form('form'):
            col1,col2 = st.columns(2,gap='large')
            # ['quantity tons','customer','country','application','thickness','width','product_ref','item_type','status']
            with col1:
                quantity = st.text_input('quantity tons')
                customer = st.text_input('customer (min : 12458.0 & max: 30408185.0)')
                country = st.selectbox('country',options=countries)
                application = st.text_input('application (min : 2 & max: 99)')
                thickness = st.text_input('thickness')
            with col2:
                width = st.text_input('width')
                product_ref = st.selectbox('product_ref',options = product_refs)
                item_type = st.radio('item_type',options= ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR'],horizontal=True)
                status = st.radio('status',options=['Won','Lost'],horizontal=True)
                predict = st.form_submit_button('predict selling price')
                try:
                    if predict:
                        with st.spinner('Getting Price'):
                            with open("C:/Users/kisho/notebooks/copper_rfr.pkl",'rb') as f:
                                model = pickle.load(f)
                            with open("C:/Users/kisho/notebooks/ohe1.pkl", 'rb') as f:
                                ohe1 = pickle.load(f)
                            with open("C:/Users/kisho/notebooks/ohe2.pkl",'rb') as f:
                                ohe2 = pickle.load(f)
                            with open("C:/Users/kisho/notebooks/scaler.pkl",'rb') as f:
                                scaler = pickle.load(f)


                            sample = np.array([[np.log(float(quantity)),customer,country,application,np.log(float(thickness)),width,product_ref,item_type,status]])
                            nums = [quantity,customer,country,application,thickness,width,product_ref]
                            if all(nums)>0:
                                a = sample[:,:7]
                            b = ohe1.transform(sample[:,[7]]).toarray()
                            c = ohe2.transform(sample[:,[8]]).toarray()
                            x = np.concatenate([a,b,c],axis=1)
                            y = scaler.transform(x)
                            z = model.predict(y)
                            prediction = np.exp(z)[0]
                            st.markdown(f'### The Selling Price is :green[{prediction}]')
                except:
                    st.error("Enter valid details")

    with tab2:
        with st.form('form2'):
            col1,col2 = st.columns(2,gap='large')
            # ['quantity tons','customer','country','application','thickness','width','product_ref','item_type','status']
            with col1:
                quantity = st.text_input('quantity tons')
                customer = st.text_input('customer (min : 12458.0 & max: 30408185.0)')
                country = st.selectbox('country',options=countries)
                application = st.text_input('application (min : 2 & max: 99)')
                thickness = st.text_input('thickness')
            with col2:
                width = st.text_input('width')
                product_ref = st.selectbox('product_ref',options = product_refs)
                item_type = st.radio('item_type',options= ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR'],horizontal=True)
                selling_price = st.text_input('selling_price')
                predict = st.form_submit_button('predict status')
                try:
                    if predict:
                        with st.spinner('Getting Status'):
                            with open("C:/Users/kisho/notebooks/copper_rfc.pkl",'rb') as f:
                                model = pickle.load(f)
                            with open("C:/Users/kisho/notebooks/ohe3.pkl", 'rb') as f:
                                ohe3 = pickle.load(f)
                            with open("C:/Users/kisho/notebooks/le.pkl",'rb') as f:
                                le = pickle.load(f)
                            with open("C:/Users/kisho/notebooks/scaler1.pkl",'rb') as f:
                                scaler1 = pickle.load(f)


                            sample = np.array([[np.log(float(quantity)),customer,country,application,np.log(float(thickness)),width,product_ref,np.log(float(selling_price)),item_type]])
                            nums = [quantity,customer,country,application,thickness,width,product_ref,selling_price]
                            if all(nums)>0:
                                a = sample[:,:8]
                            b = ohe3.transform(sample[:,[8]]).toarray()
                            x = np.concatenate([a,b],axis=1)
                            y = scaler1.transform(x)
                            z = model.predict(y)
                            prediction = le.inverse_transform(z)[0]
                            st.markdown(f'### The Status is :green[{prediction}]')
                except:
                    st.warning('Enter valid Details')
else:
    st.title(':technologist: About')

    st.write('## :red[Name]: Kishorekumar Nadipena')
    st.write(
        '### :red[LinkedIn]: kishorekumar-nadipena :link: [link](https://www.linkedin.com/in/kishorekumar-nadipena/)')
    st.write('### :red[github]: github.com/nkishore123 :link: [link](https://github.com/nkishore123)')