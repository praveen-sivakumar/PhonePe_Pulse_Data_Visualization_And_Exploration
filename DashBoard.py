#------------------------------------------Importing Required Libraries---------------------------------------------

import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px  
#------------------------------------------Page Configuration Setup-------------------------------------------------

st.set_page_config(page_title="Phonepe Pulse",
                   layout="wide",
                   initial_sidebar_state='auto',
                   menu_items={'About':'Application developed by Praveen Sivakumar'}
                   )

#---------------------------------------------Connecting to MySql-----------------------------------------------------

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "root",
  database = "PhonePe_Pulse"
)
mycursor = mydb.cursor(buffered=True)


#---------------------------------------------MySql to DataFrame-----------------------------------------------------

aggregated_transaction_query = "Select * from aggregatedtransaction"
Aggregated_Transaction_DF = pd.read_sql(aggregated_transaction_query,mydb)

aggregated_user_query = "Select * from aggregateduser"
Aggregated_User_DF = pd.read_sql(aggregated_user_query,mydb)

map_transaction_query = "Select * from maptransaction"
Map_Transaction_DF = pd.read_sql(map_transaction_query,mydb)

map_user_query = "Select * from mapuser"
Map_User_DF = pd.read_sql(map_user_query,mydb)

top_transaction_query = "Select * from toptransaction"
Top_Transaction_DF = pd.read_sql(top_transaction_query,mydb)

top_user_query = "Select * from topuser"
Top_User_DF = pd.read_sql(top_user_query,mydb)


#-------------------------------------------Creating Navigation bar-------------------------------------------------

selected = option_menu(
        menu_title = None,
        options=["Home","Dashboard","Geo-Visualization","About"],
        icons=["house-fill","graph-up-arrow",'globe2',"exclamation-lg"],
        default_index=0,
        orientation="horizontal",
        styles={
                "container": {"background-color": "#7F00FF"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"text-align": "centre","--hover-color": "white"},
                "nav-link-selected": {"background-color": "black"}
        }
    )


#------------------------------------------------Setting Title------------------------------------------------------

st.title("Phonepe Pulse Data Visualization and Exploration")

#---------------------------------------------------HomePage---------------------------------------------------------

if selected == 'Home':

    st.markdown('''**The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics.**''') 
    st.markdown('''**In this website extract the data and process it to obtain insights and information that can be visualized in a user-friendly manner.**''')
    
    st.subheader('_How its done_')

    st.markdown('**:red[Step 1] :**  We clone the data from the phonepe pulse github repository https://github.com/PhonePe/pulse')

    st.markdown('**:red[Step 2] :**  We process the data and store in a MySql database in a structured format')

    st.markdown('**:red[Step 3] :**  We create a web application using Streamlit library of Python')

    st.markdown('**:red[Step 4] :**  In the application we provide data visualization option to the user depending the data')

    st.markdown('**:red[Step 5] :**  Data Visualization is been done with the help of python libraries like plotly and pandas')

    st.subheader('_Outcome_')

    st.markdown('**Users can get an insight on the Phonepe Pulse data for the years from 2018 to 2022 in a visually appealing manner and easy to understand.**')
    


#---------------------------------------------------DashBoard---------------------------------------------------------

if selected == 'Dashboard':
    st.write("**Welcome to the :red[dashboard]..! Here you can :red[Explore] and :red[Visualize] the data**")


    #---------------------------------------------------------------------------DataFrames--------------------------------------------------------------------------------
    st.subheader("DataFrames")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("### :red[Explore Transaction Data]")
    
        selected = st.selectbox('### **Choose the type of :red[Data]**',['Select Any', 'Aggregated_Transaction','Map_Transaction','Top_Transaction'])

        if selected == 'Aggregated_Transaction':
            st.dataframe(Aggregated_Transaction_DF)
    
        if selected == 'Map_Transaction':
            st.dataframe(Map_Transaction_DF)

        if selected == 'Top_Transaction':    
            st.dataframe(Top_Transaction_DF)

    with col2:
        st.markdown("### :red[Explore User Data]")

        selected = st.selectbox('### **Choose the type of :red[Data]**',['Select Any', 'Aggregated_User','Map_User','Top_User'])

        if selected == 'Aggregated_User':  
            st.dataframe(Aggregated_User_DF)

        if selected == 'Map_User':    
            st.dataframe(Map_User_DF)

        if selected == 'Top_User':    
            st.dataframe(Top_User_DF)


    st.write('''### ----------------------------------------------------------------------------------------------------------------------------------------------------------''')


    #-------------------------------------------------------------------Data Visualization-------------------------------------------------------------------------------------
    st.subheader("Data-Visualization")

    col1, col2, col3 = st.columns(3)

    with col1:
        dataType = st.selectbox('### **Choose the type of :red[Data]**',['Select Any', 'Aggregated Data','Map Data','Top Data'])

    with col2:
        if dataType == 'Aggregated Data':
            data_to_visualize = st.selectbox('### **Choose the data to :red[Visualize]**', ['Select Any', 'Top 10 States with highest Amount', 'Top 10 Brands with highest number of Users'])

        if dataType == 'Map Data':
            data_to_visualize = st.selectbox('### **Choose the data to :red[Visualize]**', ['Select Any', 'Top 10 District with highest Amount', 'Top 10 District with highest number of Registered Users', 'Top 10 District with highest number of App Opens'])

        if dataType == 'Top Data':
            data_to_visualize = st.selectbox('### **Choose the data to :red[Visualize]**', ['Select Any', 'Top 10 Pincode with highest Amount', 'Top 10 Pincode with highest Registered Users'])

    with col3:
        chart_type = st.selectbox('**Choose the type of :red[Data Visualization]**', ['Select Any', 'Pie Chart', 'Bar Chart'])

    #------------------------------------------------------------------Aggreagated Data------------------------------------------------------------------
   
    if dataType == 'Aggregated Data':
        
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)

    #------------------------------------------------------------------Top 10 States with highest Amount------------------------------------------------------------------
        if data_to_visualize == 'Top 10 States with highest Amount':
            st.markdown("### Top 10 :violet[States] with highest :violet[Amount]")

        
            mycursor.execute(f"select state, sum(count) as Total_Count, sum(amount) as Total_Amount from aggregatedtransaction where year = {Year} and quarter = {Quarter} group by state order by Total_Amount desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Count','Total_Amount'])

            col1, col2 = st.columns(2)

            with col1:
            #---------------------------------------------------Pie Chart-------------------------------------------------
                if chart_type == 'Pie Chart':
                    fig = px.pie(
                        df, 
                        title='Top 10 States with Highest Amount',
                        values='Total_Amount',
                        names='State',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Count'],
                        labels={'Total_Count':'Total_Count'}
                    )

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)

            #---------------------------------------------------Bar Chart-------------------------------------------------
                if chart_type == 'Bar Chart':
                    fig = px.bar(
                        df,
                        title='Top 10 States with Highest Amount',
                        x='Total_Count',
                        y='State',
                        orientation='h',
                        color='Total_Amount',
                        color_continuous_scale=px.colors.sequential.Agsunset
                    )
                    st.plotly_chart(fig,use_container_width=True)

            with col2:
                st.dataframe(df) #DataFrame
   
        #------------------------------------------------------------------Top 10 Brands with highest number of Users------------------------------------------------------------------

        
        if data_to_visualize == 'Top 10 Brands with highest number of Users':
            st.markdown("### Top 10 :violet[Brands] with highest number of :violet[Users]")

            mycursor.execute(f"select brand, sum(count) as Total_Users, avg(percentage)*100 as Average_Percentage from aggregateduser where year = {Year} and quarter = {Quarter} group by brand order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Average_Percentage'])

            col1, col2 = st.columns(2)

            with col1:
            #---------------------------------------------------Pie Chart-------------------------------------------------
                if chart_type == 'Pie Chart':
                    fig = px.pie(
                        df,
                        title='Top 10 brands',
                        values="Total_Users",
                        names="Brand",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Users'],
                        labels={'Total_Users':'Total_Users'}
                    )
                    st.plotly_chart(fig,use_container_width=True)

            #-----------------------------------------------------Bar Chart------------------------------------------------
                if chart_type == 'Bar Chart':
                    fig = px.bar(
                        df,
                        title='Top 10 brands',
                        x="Total_Users",
                        y="Brand",
                        orientation='h',
                        color='Average_Percentage',
                        color_continuous_scale=px.colors.sequential.Agsunset
                    )
                    st.plotly_chart(fig,use_container_width=True)
            with col2:
                st.dataframe(df) #DataFrame
    
    
    
    
    #------------------------------------------------------------------Map Data------------------------------------------------------------------
    
    if dataType == 'Map Data':
        
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)


        #------------------------------------------------------------------Top 10 District with highest Amount------------------------------------------------------------------
        if data_to_visualize == 'Top 10 District with highest Amount':
            st.markdown("### Top  10 :violet[District] with highest :violet[Amount]")

            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from maptransaction where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Count','Total_Amount'])

            col1, col2 = st.columns(2)

            with col1:
            #---------------------------------------------------Pie Chart-------------------------------------------------
                if chart_type == 'Pie Chart':
                    fig = px.pie(
                        df, 
                        title='Top 10 District with highest Amount',
                        values='Total_Amount',
                        names='District',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Count'],
                        labels={'Total_Count':'Total_Count'}
                     )

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)

            #---------------------------------------------------Bar Chart-------------------------------------------------
                if chart_type == 'Bar Chart':
                    fig = px.bar(
                        df,
                        title='Top 10 District with highest Amount',
                        x="Total_Count",
                        y="District",
                        orientation='h',
                        color='Total_Count',
                        color_continuous_scale=px.colors.sequential.Agsunset
                    )
                st.plotly_chart(fig,use_container_width=True)

            with col2:
                st.dataframe(df) #DataFrame
    
        #------------------------------------------------------------------Top 10 District with highest number of Registered Users------------------------------------------------------------------
        if data_to_visualize == 'Top 10 District with highest number of Registered Users':
            st.markdown("### Top 10 :violet[District] with highest number of :violet[Users]")

            mycursor.execute(f"select district , sum(registereduser) as Total_Registered_Users from mapuser where year = {Year} and quarter = {Quarter} group by district order by Total_Registered_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Registered_Users'])
            df.Total_Registered_Users = df.Total_Registered_Users.astype(float)

            col1, col2 = st.columns(2)

            with col1:
            #---------------------------------------------------Pie Chart-------------------------------------------------
                if chart_type == 'Pie Chart':
                    fig = px.pie(
                        df,
                        title='Top 10 District with highest number of Registered Users',
                        values="Total_Registered_Users",
                        names = 'District',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Registered_Users'],
                        labels={'Total_Registered_Users':'Total_Registered_Users'}
                    )       
                    st.plotly_chart(fig,use_container_width=True)

            #---------------------------------------------------Bar Chart-------------------------------------------------
                if chart_type == 'Bar Chart':
                    fig = px.bar(
                        df,
                        title='Top 10 District with highest number of Registered Users',
                        x="Total_Registered_Users",
                        y="District",
                        orientation='h',
                        color='Total_Registered_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset
                    )
                    st.plotly_chart(fig,use_container_width=True)


            with col2:
                st.dataframe(df) #DataFrame
    

        #------------------------------------------------------------------Top 10 District with highest number of App Opens------------------------------------------------------------------
        if data_to_visualize == 'Top 10 District with highest number of App Opens':
            st.markdown("### Top 10 :violet[District] with highest number of :violet[App Opens]")

            mycursor.execute(f"select district , sum(appopens) as Total_AppOpens from mapuser where year = {Year} and quarter = {Quarter} group by district order by Total_AppOpens desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_AppOpens'])
            df.Total_AppOpens = df.Total_AppOpens.astype(float)

            col1, col2 = st.columns(2)

            with col1:
            #---------------------------------------------------Pie Chart-------------------------------------------------
                if chart_type == 'Pie Chart':
                    fig = px.pie(
                        df,
                        title='Top 10 District with highest number of App Opens',
                        values="Total_AppOpens",
                        names = 'District',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_AppOpens'],
                        labels={'Total_AppOpens':'Total_AppOpens'}
                    )       
                    st.plotly_chart(fig,use_container_width=True)

            #---------------------------------------------------Bar Chart-------------------------------------------------
                if chart_type == 'Bar Chart':
                    fig = px.bar(
                        df,
                        title='Top 10 District with highest number of App Opens',
                        x="Total_AppOpens",
                        y="District",
                        orientation='h',
                        color='Total_AppOpens',
                        color_continuous_scale=px.colors.sequential.Agsunset
                    )
                    st.plotly_chart(fig,use_container_width=True)


            with col2:
                st.dataframe(df) #DataFrame
    
    #-------------------------------------------------------------------------Top Data------------------------------------------------------------------------------------
    if dataType == 'Top Data':
        
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)
    
        #------------------------------------------------------------------Top 10 Pincode with highest Amount------------------------------------------------------------------
        if data_to_visualize == 'Top 10 Pincode with highest Amount':
            st.markdown("### Top 10 :violet[Pincode] with highest :violet[Amount]")

            mycursor.execute(f"select pincode, sum(Count) as Total_Count, sum(amount) as Total_Amount from toptransaction where year = {Year} and quarter = {Quarter} group by pincode order by Total_Amount desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Count','Total_Amount'])

            col1, col2 = st.columns(2)

            with col1:
            #---------------------------------------------------Pie Chart-------------------------------------------------
                if chart_type == 'Pie Chart':
                    fig = px.pie(
                        df, 
                        values='Total_Amount',
                        names='Pincode',
                        title='Top 10 Pincode with highest Amount',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Count'],
                        labels={'Total_Count':'Total_Count'}
                    )

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)

            #---------------------------------------------------Bar Chart-------------------------------------------------
                if chart_type == 'Bar Chart':
                    df.Total_Count = df.Total_Count.astype(float)
                    fig = px.bar(
                    df,
                    title='Top 10 Pincode with highest Amount',
                    x="Total_Count",
                    y="Pincode",
                    orientation='h',
                    color='Total_Count',
                    color_continuous_scale=px.colors.sequential.Agsunset
                )
                st.plotly_chart(fig,use_container_width=True)

                with col2:
                    st.dataframe(df) #DataFrame
    
        #------------------------------------------------------------------Top 10 Pincode with highest Registered Users------------------------------------------------------------------
        if data_to_visualize == 'Top 10 Pincode with highest Registered Users':
            st.markdown("### Top 10 :violet[Pincode] with highest number of  :violet[Registered Users]")

            mycursor.execute(f"select Pincode, sum(RegisteredUser) as Total_Users from topuser where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])

            col1, col2 = st.columns(2)

            with col1:
            #---------------------------------------------------Pie Chart-------------------------------------------------
                if chart_type == 'Pie Chart':
                    fig = px.pie(
                        df,
                        title='Top 10 Pincode with highest Registered Users',
                        values='Total_Users',
                        names='Pincode',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Users'])
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)

            #---------------------------------------------------Bar Chart-------------------------------------------------
                if chart_type == 'Bar Chart':
                    df.Total_Users = df.Total_Users.astype(float)
                    fig = px.bar(
                        df,
                        title='Top 10 Pincode with highest Registered Users',
                        x="Total_Users",
                        y="Pincode",
                        orientation='h',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset
                    )
                    st.plotly_chart(fig,use_container_width=True)

                with col2:
                    st.dataframe(df) #DataFrame

    st.write('''### ----------------------------------------------------------------------------------------------------------------------------------------------------------''')


#---------------------------------------------------Geo-Visualization-----------------------------------------------------  

if selected == 'Geo-Visualization':

    #---------------------------------------------------To Map with GeoJson----------------------------------------------
    all_states = [
    'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal pradesh', 'Assam',
    'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra & Nagar Haveli & Daman & Diu', 
    'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 
    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 
    'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry',
    'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 
    'Uttarakhand', 'West Bengal'
    ]

    df2 = pd.DataFrame(all_states)

    #----------------------------------------------------Indian Map Visualization----------------------------------------
   
    def GeoVisualization(data_Frame,location,color):
        fig = px.choropleth(
            data_Frame,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            #geojson="states_india.geojson",
            featureidkey='properties.ST_NM',
            locations=location,
            color=color,
            color_continuous_scale='sunset',
            #hover_data=['State','Total_Transactions'],
         )
        #fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig.update_geos(fitbounds="locations", visible=False)
    

    #-----------------------------------------------------Conditions---------------------------------------------------
    

    geo_Choice = st.selectbox('Choose the data to display',['Select Any',
                                                            'Total Transaction Amount By Each State',
                                                            'Total Registered Users By Each State',
                                                            'Total App Opens By Each State'
                                                        ])


    #-------------------------------------------------Total Transaction Amount By Each State-------------------------------------------------------
    if geo_Choice == 'Total Transaction Amount By Each State':
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)

        st.markdown("## :violet[Total Transaction Amount By Each State]")

        mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_Amount from maptransaction where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_Amount'])
    
        df1.State = df2

        col1,col2 = st.columns(2)

        with col1:
            st.markdown("### GEO-VISUALIZATION")
            fig = GeoVisualization(df1,'State','Total_Amount')
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:
            st.markdown("### DATAFRAME")
            st.dataframe(df1)


    #--------------------------------------------------------Total Registered Users By Each State-------------------------------------------------------

    if geo_Choice == 'Total Registered Users By Each State':
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)

        st.markdown("## :violet[Total Registered Users By Each State]")

        mycursor.execute(f"select State, sum(RegisteredUser) as Registered_User from topuser where year = {Year} and quarter = {Quarter} group by State order by State")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Registered_User'])
    
        df1.State = df2

        col1,col2 = st.columns(2)

        with col1:
            st.markdown("### GEO-VISUALIZATION")
            fig = GeoVisualization(df1,'State','Registered_User')
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:
            st.markdown("### DATAFRAME")
            st.dataframe(df1)


    #--------------------------------------------------------Total App Opens By Each State-------------------------------------------------------

    if geo_Choice == 'Total App Opens By Each State':
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("**Quarter**", min_value=1, max_value=4)

        st.markdown("## :violet[Total Registered Users By Each State]")

        mycursor.execute(f"select State, sum(RegisteredUser) as Registered_User, sum(AppOpens) as App_Opens from mapuser where year = {Year} and quarter = {Quarter} group by State order by State")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Registered_User', 'App_Opens'])
    
        df1.State = df2

        col1,col2 = st.columns(2)

        with col1:
            st.markdown("### GEO-VISUALIZATION")
            fig = GeoVisualization(df1,'State','App_Opens')
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:
            st.markdown("### DATAFRAME")
            st.dataframe(df1)

    #---------------------------------------------------------
        

        
#---------------------------------------------------About-----------------------------------------------------------------

if selected == 'About':
    st.markdown('''The result of this project will be a live geo visualization dashboard that displays
    information and insights from the Phonepe pulse Github repository in an interactive
    and visually appealing manner. The dashboard will have options for users to select different facts and figures to display. The data
    will be stored in a MySQL database for efficient retrieval and the dashboard will be
    dynamically updated to reflect the latest data.''')

    st.markdown('''Users will be able to access the dashboard from a web browser and easily navigate
    the different visualizations and facts and figures displayed. The dashboard will
    provide valuable insights and information about the data in the Phonepe pulse
    Github repository, making it a valuable tool for data analysis and decision-making.''')

    st.markdown('''Overall, the result of this project will be a comprehensive and user-friendly solution
    for extracting, transforming, and visualizing data from the Phonepe pulse Github
    repository.''')

    st.markdown('**:red[Technologies]** : Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly')

    st.markdown('**:red[Domain]** : FINTECH')


    st.markdown('**:red[Github Link]** : https://github.com/praveen-sivakumar/PhonePe_Pulse_Data_Visualization_And_Exploration')

    st.subheader('Project done by **:blue[_Praveen Sivakumar_]**')


#---------------------------------------------------THE END---------------------------------------------------------------