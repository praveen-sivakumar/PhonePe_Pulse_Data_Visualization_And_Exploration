# PhonePe_Pulse_Data_Visualization_And_Exploration
This project is to create a live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner.

* ### Libraries 
1. os 
2. json  
3. mysql.connector 
4. pandas  
5. json 
6. git.repo.base
7. plotly.express
8. streamlit
9. streamlit_option_menu

* ### Data Extraction

  In this step we are cloning the data from the github repository. (Data is in the form of json)

* ### Data Transformation

  In this step we are converting all the JSON files into CSV format.

* ### Data Insertion

  In this step we are creating a database in MySql. Then we insert our dat into this database with the proper table.

 * ### Streamlit Application

   We are the using the streamlit library to creat a application where users can explore the data. To make it more interactive many features like charts, dataframes and geo-visualization are been made.

* ### Data Retrieval

  In the application, inorder for the data to be visually represented, we are connecting to the database we created and we retrive the data depending on the conditions.

# Files

* ### DataETL.ipynb

     In this file we clone the data, transform it and store in the database.
  
* ### DashBoard.py

     In this file, we write the code for streamlit application (UI) and the features like charts, dataframes, geo-visualization and also for the data retrieval.

* ### states_india.geojson

     This geojson file is required for geo-visualization using choropleth from the plotly-express library. 
