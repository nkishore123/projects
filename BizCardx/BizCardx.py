import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import cv2
from PIL import Image
import numpy as np
import io
import re
import mysql.connector as mysql
import pandas as pd

icon = Image.open("C:/Users/kisho/Downloads/ocr icon.png")
st.set_page_config(page_title='Biz card',
                   page_icon=icon,
                   layout = "wide",
                   initial_sidebar_state = "expanded")

option = option_menu(None, ["Home", "Upload", "Modify", 'About'],
                     icons=['house', 'cloud-upload', "list-task", 'person-vcard-fill'],
                     menu_icon="cast", default_index=0, orientation="horizontal",
                     styles={
                         "container": {"padding": "0!important", "background-color": "grey"},
                         "icon": {"color": "orange", "font-size": "15px"},
                         "nav-link": {"font-size": "15px", "text-align": "center", "margin": "5px",
                                      "--hover-color": "teal"},
                         "nav-link-selected": {"background-color": "red"},
                     }
                     )
mydb = mysql.connect(host="localhost",
                     user="root",
                     password="Kishore@95",
                     database="BizCarx")
mycursor = mydb.cursor()
query = """Create table if not exists business_cards(
                        id int auto_increment primary key,
                        card_holder_name varchar(50),
                        designation varchar(50),
                        phone varchar(50),
                        mail varchar(50),
                        website varchar(50),
                        area varchar(50),
                        city varchar(50),
                        state varchar(50),
                        pincode varchar(50),
                        company_name varchar(50),
                        bin_img LONGBLOB);"""
mycursor.execute(query)

if option == 'Home':
    st.title("Home")
    col1,col2 = st.columns(2,gap="large")
    with col1:
        st.write('### :orange[Project Name]: BizCardX: Extracting Business Card Data with OCR')
        st.write(
            '### :orange[Technologies Used]: OCR,streamlit, MySql')
        st.write(
            '''### :orange[Overview]: In this Streamlit app we can upload an image of business card and it will extract data from the image, we can also store the data in mysql database. We can also modify and delete a ccertain reecord based on our interest''')
    with col2:
        image = Image.open("C:/Users/kisho/Downloads/ocr logo.jpg")
        st.image(image)
elif option == "Upload":
    st.title("Upload an Image")
    image = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])
    if image is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.success("Image Uploaded Successfully")
            st.image(image)
        with col2:
            with st.spinner("Please wait processing image..."):
                image_bytes = image.read()
                reader = easyocr.Reader(['en'], gpu=False)
                result = reader.readtext(image_bytes)

                pil_image = Image.open(io.BytesIO(image_bytes))
                img = np.array(pil_image)
                for i in result:
                    top_left = tuple(map(int,i[0][0]))
                    bottom_right = tuple(map(int,i[0][2]))
                    text = i[1]
                    font = cv2.FONT_HERSHEY_SIMPLEX

                    img = cv2.rectangle(img,top_left,bottom_right,(0,0,255),5)
                    img = cv2.putText(img,text,top_left,font,1,(0,255,0),2,cv2.LINE_AA)
                st.success('Got the details')
                st.image(img, channels="BGR")
        def img_to_binary(file):
            pil_image = Image.open(image)
            with io.BytesIO() as buffer:
                pil_image.save(buffer, format="PNG")
                binary_image = buffer.getvalue()
            return binary_image
        data = {'card_holder_name':[],'designation':[],'phone': [],'mail':[],'website': [],'area': [],'city': [],'state':[],
                'pincode':[],'company_name':[],'binary_image':img_to_binary(image)}

        def get_data(result):
            for ind,i in enumerate(result):
                # card_holder
                if ind == 0:
                    data['card_holder_name'] = i[1]
                #designation
                elif ind == 1:
                    data['designation'] = i[1]
                # email
                elif '@' in i[1]:
                    data['mail'].append(i[1])
                #phone
                elif '-' in i[1]:
                    data['phone'].append(i[1])
                    if len(data['phone']) >1:
                        data['phone'] = ' & '.join(data['phone'])
                # website
                elif 'www ' in i[1].lower() or 'www.' in i[1].lower():
                    data['website'] = i[1]
                elif 'WWW' in i[1]:
                    data['website'] =result[4][1]+'.'+result[5][1]
                # Area
                elif re.fullmatch('^[0-9]+ [a-zA-Z]+$',i[1]): #2
                    data['area'] = i[1]
                    data['city'] = result[7][1]
                elif re.findall('^[0-9]+ [a-zA-Z ]+,, [a-zA-Z ,;]+',i[1]): #4
                    r = ' '.join(re.findall('^[0-9]+ [a-zA-Z ]+,, [a-zA-Z ,;]+',i[1]))
                    data['area'] = ' '.join(r.split(' ')[0:3])
                    data['city'] = ''.join(r.split(' ')[-2])
                    data['state'] = ''.join(r.split(' ')[-1])
                elif re.findall('^[0-9]+ [a-zA-Z ,]+; [a-zA-Z]+',i[1]): #5
                    data['area'] = ' '.join(i[1].split(' ')[0:3])
                    data['city'] = i[1].split(' ')[-2]
                    data['state'] = i[1].split(' ')[-1]
                elif re.findall('[0-9]+ [a-zA-Z]+ [a-zA-Z]+ , [a-zA-Z]+',i[1]): #1
                    data['area'] = ' '.join(i[1].split(' ')[0:3])
                    data['city'] = i[1].split(' ')[-1]
                # state
                elif re.findall('^[a-zA-Z]+ [0-9]+', i[1]):
                    data['state'] = i[1].split()[0]
                    data['pincode'] = i[1].split()[-1]
                elif re.findall('[0-9]+', i[1]):
                    data['pincode'] = i[1]
                #company
                elif ind == len(result)-1 and i[1].isupper():
                    data['company_name'] = result[-2][1]+' '+result[-1][1]
                elif ind == len(result)-1 and len(i[1])>10:
                    data['company_name'] = result[-1][1]
                elif ind == len(result)-1 and len(i[1])>5:
                    data['company_name'] = result[-3][1]+' '+result[-1][1]
                elif ind == len(result)-1:
                    data['company_name'] = result[-4][1]+' '+result[-2][1]
        get_data(result)
        st.markdown('### Extracted data')
        df = pd.DataFrame(data)
        st.dataframe(df)
        if st.button("Upload to DataBase"):
            for i, row in df.iterrows():
                query = "INSERT INTO business_cards(card_holder_name,designation,phone,mail,website,area,city,state,pincode,company_name,bin_img) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(query,tuple(row))
                mydb.commit()
            st.success("Successfully Uploaded")
elif option == 'Modify':
    col1,col2,col3 = st.columns([1.5,1.5,1],gap='large')
    with col2:
        st.subheader('Alter or Delete data')
    col1,col2 = st.columns(2,gap='large')
    try:
        with col1:
            mycursor.execute('Select card_holder_name from business_cards')
            names = []
            for i in mycursor.fetchall():
                names.append(i[0])
            selected = st.selectbox('Select One',options=names)

            mycursor.execute(f"Select card_holder_name,designation,phone,mail,website,area,city,state,pincode,company_name from business_cards where card_holder_name = '{selected}'")
            result = mycursor.fetchone()

            card_holder_name = st.text_input("card_holder_name",result[0])
            designation = st.text_input("designation", result[1])
            phone = st.text_input("phone", result[2])
            mail = st.text_input("mail", result[3])
            website = st.text_input("website", result[4])
            area = st.text_input("area", result[5])
            city = st.text_input("city", result[6])
            state = st.text_input("state", result[7])
            pincode = st.text_input("pincode", result[8])
            company_name = st.text_input("company_name", result[9])

            if st.button("Commit changes to DB"):
                mycursor.execute("update business_cards set card_holder_name=%s,designation=%s,phone=%s,mail=%s,website=%s,"
                                 "area=%s,city=%s,state=%s,pincode=%s,company_name=%s where card_holder_name = %s",
                                 (card_holder_name,designation,phone,mail,website,area,city,state,pincode,company_name,selected))
                mydb.commit()
                st.success('Updated successfully')
        with col2:
            mycursor.execute('Select card_holder_name from business_cards')
            names = []
            for i in mycursor.fetchall():
                names.append(i[0])
            name = st.selectbox('Select name', options=names)
            st.markdown(f"You selected {name}")
            st.markdown("Do you want to proceed?")
            if st.button("Yes"):
                mycursor.execute(f"Delete From business_cards where card_holder_name = '{name}'")
                mydb.commit()
                st.success("successfully deleted")
    except:
        st.warning("No data in table")

elif option == 'About':
    st.title(':technologist: About')

    st.write('## :red[Name]: Kishorekumar Nadipena')
    st.write(
        '### :red[LinkedIn]: kishorekumar-nadipena :link: [link](https://www.linkedin.com/in/kishorekumar-nadipena/)')
    st.write('### :red[github]: github.com/nkishore123 :link: [link](https://github.com/nkishore123)')
