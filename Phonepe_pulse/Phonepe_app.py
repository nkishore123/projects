import plotly.express as px
import json
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import mysql.connector as mysql

mydb = mysql.connect(host="localhost",
                     user="root",
                     password="Kishore@95",
                     database="Phonepe")
mycursor = mydb.cursor()

st.set_page_config(page_title='Phonepe Pulse vizualization',
                   page_icon="📺",
                   layout = "wide",
                   initial_sidebar_state = "expanded")

with st.sidebar:
    option = option_menu(menu_title='Menu',
                         options = ['Home','Charts','Maps','About'],
                         icons=['house',"bar-chart","globe-central-south-asia", "exclamation-circle"])
if option == 'Home':
    st.title("Welcome")
    col1, col2 = st.columns([2,1])
    with col1:

        st.write('### :violet[Project Name]: Phonepe Pulse Data Visualization and Exploration')
        st.write('### :violet[Technologies Used]: Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly')
        st.write('### :violet[Domain]: Fintech')
        st.write('''### :violet[Overview]: This project is about a live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner.''')
    with col2:
        image = Image.open("C:/Users/kisho/Downloads/phonepe_logo.jpg")
        st.image(image)

elif option == 'Charts':
    Type = st.sidebar.selectbox("**Type**", ("Select One","Transactions", "Users"))
    st.subheader(f'Select Preferences')
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")
    with col1:
        states = []
        query = 'Select DISTINCT state From aggregate_transactions'
        mycursor.execute(query)
        for i in mycursor:
            states.append(i[0])
        all_s = st.checkbox('All_States', True)
        state = st.selectbox('State', options=states, disabled=all_s)
    with col2:
        years = []
        query = 'Select DISTINCT year From aggregate_transactions'
        mycursor.execute(query)
        for i in mycursor:
            years.append(i[0])

        all_y = st.checkbox('All_Years', True)
        year = st.slider('Year', min_value = min(years),max_value = max(years),step=1, disabled=all_y)
        year = tuple([0, year])
        if all_y:
            year = tuple(years)
    with col3:
        all_q = st.checkbox('All_Quarters', True)
        quarter = st.slider('Quarter', 1, 4, 1,disabled=all_q)
        quarter = tuple([0, quarter])
        if all_q:
            quarter = (1, 2, 3, 4)

    st.divider()
    if Type == 'Transactions':
        col1, col2= st.columns([1, 3], gap="large")
        with col1:
            cat = st.radio('On which category', ['Transaction_Type', 'District', 'PinCode'])
            arc = st.radio('Select one', ['Transaction_Amount', 'Transactions_Count'])
            chart_type = st.radio('type of chart', ['Pie', 'Bar'])
        with col2:
            st.subheader(f'{chart_type} chart of {arc} based on {cat}')

            if cat == 'Transaction_Type':
                if arc == 'Transaction_Amount':
                    if all_s:
                        query = f'Select transaction_type Type,sum(transactions_amount) Total_Amount FROM aggregate_transactions where year IN {year} and quarter IN {quarter} GROUP BY transaction_type'
                    else:
                        query = f'''Select transaction_type Type,sum(transactions_amount) Total_Amount 
                                    from (SELECT * 
                                          FROM aggregate_transactions
                                          WHERE state = '{state}') sub
                                    where year IN {year} and quarter IN {quarter} GROUP BY transaction_type'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['Type', 'Total_Amount'])

                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='Type',
                                     values='Total_Amount',
                                     color='Type')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='Type',
                                     y='Total_Amount',
                                     color='Type')

                        st.plotly_chart(fig, use_container_width=True)
                elif arc == 'Transactions_Count':
                    if all_s:
                        query = f'Select transaction_type Type,sum(transactions_count) Count FROM aggregate_transactions where year IN {year} and quarter IN {quarter} GROUP BY transaction_type'
                    else:
                        query = f'''Select transaction_type Type,sum(transactions_count) Count 
                                    from (SELECT * 
                                          FROM aggregate_transactions
                                          WHERE state = '{state}') sub
                                    where year IN {year} and quarter IN {quarter} GROUP BY transaction_type'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['Type', 'Count'])
                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='Type',
                                     values='Count',
                                     color='Type')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='Type',
                                     y='Count',
                                     color='Type')

                        st.plotly_chart(fig, use_container_width=True)

            elif cat == 'District':
                if arc == 'Transaction_Amount':
                    if all_s:
                        query = f'Select district District,sum(transactions_amount) Total_Amount FROM map_transactions where year IN {year} and quarter IN {quarter} GROUP BY District ORDER BY Total_Amount DESC LIMIT 10'
                    else:
                        query = f'''Select district District,sum(transactions_amount) Total_Amount 
                                from (SELECT * 
                                      FROM map_transactions
                                      WHERE state = '{state}') sub
                                where year IN {year} and quarter IN {quarter} GROUP BY District
                                ORDER BY Total_Amount DESC
                                LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Amount'])

                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='District',
                                     values='Total_Amount',
                                     color='District')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='District',
                                     y='Total_Amount',
                                     color='District')

                        st.plotly_chart(fig, use_container_width=True)
                elif arc == 'Transactions_Count':
                    if all_s:
                        query = f'Select district District,sum(transactions_count) Count FROM map_transactions where year IN {year} and quarter IN {quarter} GROUP BY District ORDER BY COUNT DESC LIMIT 10'

                    else:
                        query = f'''Select district District,sum(transactions_count) Count 
                                from (SELECT * 
                                      FROM map_transactions
                                      WHERE state = '{state}') sub
                                where year IN {year} and quarter IN {quarter} GROUP BY District
                                ORDER BY Count DESC
                                LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Count'])
                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='District',
                                     values='Count',
                                     color='District')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='District',
                                     y='Count',
                                     color='District')

                        st.plotly_chart(fig, use_container_width=True)

            elif cat == 'PinCode':
                if arc == 'Transaction_Amount':
                    if all_s:
                        query = f'Select pincode PinCode,sum(transactions_amount) Total_Amount FROM top_transactions where year IN {year} and quarter IN {quarter} GROUP BY PinCode ORDER BY Total_Amount DESC LIMIT 10'

                    else:
                        query = f'''Select pincode PinCode,sum(transactions_amount) Total_Amount 
                            from (SELECT * 
                                  FROM top_transactions
                                  WHERE state = '{state}') sub
                            where year IN {year} and quarter IN {quarter} GROUP BY PinCode
                            ORDER BY Total_Amount DESC
                            LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['PinCode', 'Total_Amount'])

                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='PinCode',
                                     values='Total_Amount',
                                     color='PinCode')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='PinCode',
                                     y='Total_Amount',
                                     color='PinCode')

                        st.plotly_chart(fig, use_container_width=True)
                elif arc == 'Transactions_Count':
                    if all_s:
                        query = f'Select pincode PinCode,sum(transactions_count) Count FROM top_transactions where year IN {year} and quarter IN {quarter} GROUP BY PinCode ORDER BY COUNT DESC LIMIT 10'
                    else:
                        query = f'''Select pincode PinCode,sum(transactions_count) Count 
                                from (SELECT * 
                                      FROM top_transactions
                                      WHERE state = '{state}') sub
                                where year IN {year} and quarter IN {quarter} GROUP BY PinCode
                                ORDER BY COUNT DESC
                                LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['PinCode', 'Count'])
                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='PinCode',
                                     values='Count',
                                     color='PinCode')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='PinCode',
                                     y='Count',
                                     color='PinCode')

                        st.plotly_chart(fig, use_container_width=True)

    elif Type == 'Users':
        col1, col2= st.columns([1, 3], gap="large")
        with col1:
            cat = st.radio('On which category', ['Brand', 'District', 'PinCode'])

            if cat == 'Brand':
                arc = st.radio('Select one', ['Users_Count','Percentage'])
            elif cat == 'District':
                arc = st.radio('Select one', ['Registered_Users','App_Opens'])
            else:
                arc = st.radio('Select one', ['Registered_Users'])

            chart_type = st.radio('type of chart', ['Pie', 'Bar'])

        with col2:
            st.subheader(f'{chart_type} chart of {arc} based on {cat}')

            if cat == 'Brand':
                if arc == 'Users_Count':
                    if all_s:
                        query = f'Select brand Brand,sum(Users_Count) Total_Users FROM aggregate_users where year IN {year} and quarter IN {quarter} GROUP BY Brand ORDER BY Total_Users DESC LIMIT 10 '
                    else:
                        query = f'''Select brand Brand,sum(Users_Count) Total_Users
                                    from (SELECT * 
                                          FROM aggregate_users
                                          WHERE state = '{state}') sub
                                    where year IN {year} and quarter IN {quarter}
                                    GROUP BY Brand ORDER BY Total_Users DESC 
                                    LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users'])

                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='Brand',
                                     values='Total_Users',
                                     color='Brand')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='Brand',
                                     y='Total_Users',
                                     color='Brand')

                        st.plotly_chart(fig, use_container_width=True)
                elif arc == 'Percentage':
                    if all_s:
                        query = f'Select brand Brand,sum(percentage) percent FROM aggregate_users where year IN {year} and quarter IN {quarter} GROUP BY Brand ORDER BY percent DESC LIMIT 10 '
                    else:
                        query = f'''Select brand Brand,sum(percentage) percent
                                    from (SELECT * 
                                          FROM aggregate_users
                                          WHERE state = '{state}') sub
                                    where year IN {year} and quarter IN {quarter}
                                    GROUP BY Brand ORDER BY percent DESC 
                                    LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'percent'])

                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='Brand',
                                     values='percent',
                                     color='Brand')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='Brand',
                                     y='percent',
                                     color='Brand')

                        st.plotly_chart(fig, use_container_width=True)

            elif cat == 'District':
                if arc == 'Registered_Users':
                    if all_s:
                        query = f'Select district District,sum(Registered_Users) Total_Users FROM map_users where year IN {year} and quarter IN {quarter} GROUP BY District ORDER BY Total_Users DESC LIMIT 10'
                    else:
                        query = f'''Select district District,sum(Registered_Users) Total_Users 
                                from (SELECT * 
                                      FROM map_users
                                      WHERE state = '{state}') sub
                                where year IN {year} and quarter IN {quarter} GROUP BY District
                                ORDER BY Total_Users DESC
                                LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users'])

                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='District',
                                     values='Total_Users',
                                     color='District')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='District',
                                     y='Total_Users',
                                     color='District')

                        st.plotly_chart(fig, use_container_width=True)
                elif arc == 'App_Opens':
                    if all_s:
                        query = f'Select district District,sum(App_Opens) App_Opens FROM map_users where year IN {year} and quarter IN {quarter} GROUP BY District ORDER BY App_Opens DESC LIMIT 10'

                    else:
                        query = f'''Select district District,sum(App_Opens) App_Opens 
                                from (SELECT * 
                                      FROM map_users
                                      WHERE state = '{state}') sub
                                where year IN {year} and quarter IN {quarter} GROUP BY District
                                ORDER BY App_Opens DESC
                                LIMIT 10'''
                    mycursor.execute(query)

                    df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'App_Opens'])
                    if chart_type == 'Pie':
                        fig = px.pie(df,
                                     names='District',
                                     values='App_Opens',
                                     color='District')

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        fig = px.bar(df,
                                     x='District',
                                     y='App_Opens',
                                     color='District')

                        st.plotly_chart(fig, use_container_width=True)

            elif cat == 'PinCode':
                if all_s:
                    query = f'Select pincode PinCode,sum(registered_users) Registered_Users FROM top_users where year IN {year} and quarter IN {quarter} GROUP BY PinCode ORDER BY Registered_Users DESC LIMIT 10'

                else:
                    query = f'''Select pincode PinCode,sum(registered_users) Registered_Users 
                        from (SELECT * 
                              FROM top_users
                              WHERE state = '{state}') sub
                        where year IN {year} and quarter IN {quarter} GROUP BY PinCode
                        ORDER BY Registered_Users DESC
                        LIMIT 10'''
                mycursor.execute(query)

                df = pd.DataFrame(mycursor.fetchall(), columns=['PinCode', 'Registered_Users'])

                if chart_type == 'Pie':
                    fig = px.pie(df,
                                 names='PinCode',
                                 values='Registered_Users',
                                 color='PinCode')

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)
                else:
                    fig = px.bar(df,
                                 x='PinCode',
                                 y='Registered_Users',
                                 color='PinCode')

                    st.plotly_chart(fig, use_container_width=True)

elif option == 'Maps':
    Type = st.sidebar.selectbox("**Type**", ("Select One","Transactions", "Users"))
    st.subheader(f'Select Preferences')
    col1, col2,col3,col4 = st.columns([0.3 ,1.1,0.3,0.5], gap="small")
    with col1:
        all_y = st.checkbox('All_Years', True)
    with col2:
        years = []
        query = 'Select DISTINCT year From aggregate_transactions'
        mycursor.execute(query)
        for i in mycursor:
            years.append(i[0])

        year = st.radio('Year',years , disabled=all_y,horizontal=True)
        year = tuple([0, year])
        if all_y:
            year = tuple(years)
    with col3:
        all_q = st.checkbox('All_Quarters', True)
    with col4:
        quarter = st.radio('Quarter', [1,2,3,4],disabled=all_q,horizontal=True)
        quarter = tuple([0, quarter])
        if all_q:
            quarter = (1, 2, 3, 4)

    if Type == "Transactions":
        map,data = st.columns([2,1])
        with map:
            query = f'SELECT state,sum(transactions_amount) Amount, sum(Transactions_count) count FROM aggregate_transactions where year in {year} and quarter in {quarter} GROUP BY state'
            mycursor.execute(query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Amount', 'Total_Transactions'])
            df2 = pd.read_csv("C:/Users/kisho/Datasets/states.csv")
            df['State'] = df2

            fig = px.choropleth(df,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Amount',
                                title = 'Transaction_Amount',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

            fig = px.choropleth(df,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                title='Total_Transactions',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)
        with data:
            st.write("#### Transactions")
            st.write("All Phonepe Transactions (UPIs,Wallets,Cards)")
            query = f'SELECT sum(transactions_count) FROM aggregate_transactions where year in {year} and quarter in {quarter}'
            mycursor.execute(query)
            for i in mycursor:
                x = i[0]
            st.markdown(f"### :blue[{x}]")

            col1,col2 = st.columns([1,0.8])
            with col1:
                st.write("Total payment Value")
                query = f'SELECT ROUND(sum(transactions_Amount)/10000000,2) FROM aggregate_transactions where year in {year} and quarter in {quarter}'
                mycursor.execute(query)
                for i in mycursor:
                    x = i[0]
                st.markdown(f"#### :blue[{x} Cr]")
            with col2:
                st.write("Avg.Trans Value")
                query = f'SELECT ROUND(sum(transactions_amount)/sum(transactions_count),2) FROM aggregate_transactions where year in {year} and quarter in {quarter}'
                mycursor.execute(query)
                for i in mycursor:
                    x = i[0]
                st.markdown(f"#### :blue[₹{x}]")


            st.write('#### Categories')
            query = f'SELECT Transaction_type,ROUND(sum(transactions_Amount)/10000000,2) amount FROM aggregate_transactions where year in {year} and quarter in {quarter} GROUP BY Transaction_type '
            mycursor.execute(query)
            for i in mycursor:
                col1,col2 = st.columns([1.3,0.7])
                with col1:
                    st.write(i[0])
                with col2:
                    st.write(f'###### :blue[₹{i[1]} Cr]')

            tab1,tab2,tab3 = st.tabs(['State','District','Pincode'])
            with tab1:
                st.write('#### Top 10 states')
                query = f'SELECT state,ROUND(sum(transactions_Amount)/10000000,2) amount FROM aggregate_transactions where year in {year} and quarter in {quarter} GROUP BY state ORDER BY amount DESC LIMIT 10'
                mycursor.execute(query)
                for i in mycursor:
                    col1, col2 = st.columns([1.3, 0.7])
                    with col1:
                        st.write(i[0])
                    with col2:
                        st.write(f'###### :blue[₹{i[1]} Cr]')
            with tab2:
                st.write('#### Top 10 Districts')
                query = f'SELECT district,ROUND(sum(transactions_Amount)/10000000,2) amount FROM map_transactions where year in {year} and quarter in {quarter} GROUP BY district ORDER BY amount DESC LIMIT 10'
                mycursor.execute(query)
                for i in mycursor:
                    col1, col2 = st.columns([1.3, 0.7])
                    with col1:
                        st.write(i[0])
                    with col2:
                        st.write(f'###### :blue[₹{i[1]} Cr]')
            with tab3:
                st.write('#### Top 10 PinCodes')
                query = f'SELECT pincode,ROUND(sum(transactions_Amount)/10000000,2) amount FROM top_transactions where year in {year} and quarter in {quarter} GROUP BY pincode ORDER BY amount DESC LIMIT 10'
                mycursor.execute(query)
                for i in mycursor:
                    col1, col2 = st.columns([1.3, 0.7])
                    with col1:
                        st.write(f'##### {i[0]}')
                    with col2:
                        st.write(f'###### :blue[₹{i[1]} Cr]')

    if Type == "Users":
        map,data = st.columns([2,1])
        with map:
            query = f'SELECT state,sum(registered_users) total_users, sum(app_opens) total_appopens FROM map_users where year in {year} and quarter in {quarter} GROUP BY state'
            mycursor.execute(query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'total_users', 'total_appopens'])
            df2 = pd.read_csv("C:/Users/kisho/Datasets/states.csv")
            df['State'] = df2

            fig = px.choropleth(df,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='total_users',
                                title = 'Registered Users',
                                color_continuous_scale='YlOrRd')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

            fig = px.choropleth(df,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='total_appopens',
                                title='App_Opens',
                                color_continuous_scale='YlOrRd')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        with data:
            st.write("#### Users")
            col1,col2 = st.columns(2)
            with col1:
                st.write("Total Registered Users")
                query = f'SELECT sum(registered_users) FROM map_users where year in {year} and quarter in {quarter}'
                mycursor.execute(query)
                for i in mycursor:
                    x = i[0]
                st.markdown(f"### :blue[{x}]")
            with col2:
                st.write("Total App opens")
                query = f'SELECT sum(app_opens) FROM map_users where year in {year} and quarter in {quarter}'
                mycursor.execute(query)
                for i in mycursor:
                    x = i[0]
                st.markdown(f"### :blue[{x}]")

            tab1,tab2,tab3 = st.tabs(['State','District','Pincode'])
            with tab1:
                st.write('#### Top 10 states')
                query = f'SELECT state,ROUND(sum(registered_users)/10000000,2) count FROM map_users where year in {year} and quarter in {quarter} GROUP BY state ORDER BY count DESC LIMIT 10'
                mycursor.execute(query)
                for i in mycursor:
                    col1, col2 = st.columns([1.3, 0.7])
                    with col1:
                        st.write(i[0])
                    with col2:
                        st.write(f'###### :blue[₹{i[1]} Cr]')
            with tab2:
                st.write('#### Top 10 Districts')
                query = f'SELECT district,ROUND(sum(registered_users)/10000000,2) amount FROM map_users where year in {year} and quarter in {quarter} GROUP BY district ORDER BY amount DESC LIMIT 10'
                mycursor.execute(query)
                for i in mycursor:
                    col1, col2 = st.columns([1.3, 0.7])
                    with col1:
                        st.write(i[0])
                    with col2:
                        st.write(f'###### :blue[₹{i[1]} Cr]')
            with tab3:
                st.write('#### Top 10 PinCodes')
                query = f'SELECT pincode,ROUND(sum(registered_users)/10000000,2) amount FROM top_users where year in {year} and quarter in {quarter} GROUP BY pincode ORDER BY amount DESC LIMIT 10'
                mycursor.execute(query)
                for i in mycursor:
                    col1, col2 = st.columns([1.3, 0.7])
                    with col1:
                        st.write(f'##### {i[0]}')
                    with col2:
                        st.write(f'###### :blue[₹{i[1]} Cr]')

elif option == 'About':
    st.title(':technologist: About')

    st.write('## :red[Name]: Kishorekumar Nadipena')
    st.write('### :red[LinkedIn]: kishorekumar-nadipena :link: [link](https://www.linkedin.com/in/kishorekumar-nadipena/)')
    st.write('### :red[github]: github.com/nkishore123 :link: [link](https://github.com/nkishore123)')
