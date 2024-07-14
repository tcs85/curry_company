# Libraries
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import streamlit
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
import folium

streamlit.set_page_config(page_title="company_view",layout='wide')
# Import Dataset


df=pd.read_csv('train.csv')
df1=df.copy()
print(df1.head())



# Functions




# Filtering Dataset to remove NaN
selected_lines=(df1['Delivery_person_Age']!='NaN ')
df1=df1.loc[selected_lines,:].copy()

selected_lines=(df1['Road_traffic_density'] !='NaN ')
df1=df1.loc[selected_lines,:].copy()

selected_lines=(df1['City'] !='NaN ')
df1=df1.loc[selected_lines, :].copy()

selected_lines=(df1['Festival']!= 'NaN ')
df1=df1.loc[selected_lines,:].copy()

selected_lines=(df1['multiple_deliveries']!='NaN ')
df1=df1.loc[selected_lines,:].copy()

# Converting the columns from text to numbers
df1['Delivery_person_Age']=df1['Delivery_person_Age'].astype(int)
df1['multiple_deliveries']=df1['multiple_deliveries'].astype(int)
df1['Delivery_person_Ratings']=df1['Delivery_person_Ratings'].astype(float)

# Converting Order_Date column to datetime
df1['Order_Date']=pd.to_datetime(df1['Order_Date'],format='%d-%m-%Y')
# print(df1.dtypes)
# Removing spaces in the column
df1.loc[:,'ID']=df1.loc[:,'ID'].str.strip()
df1.loc[:,'Road_traffic_density']=df1.loc[:,'Road_traffic_density'].str.strip()
df1.loc[:,'Type_of_order']=df1.loc[:,'Type_of_order'].str.strip()
df1.loc[:,'Road_traffic_density']=df1.loc[:,'Road_traffic_density'].str.strip()
df1.loc[:,'City']=df1.loc[:,'City'].str.strip()
df1.loc[:,'Festival']=df1.loc[:,'Festival'].str.strip()
df1.loc[:,'ID']=df1.loc[:,'ID'].str.strip()

# removing the min string from the column data
df1['Time_taken(min)']=df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
df1['Time_taken(min)']=df1['Time_taken(min)'].astype(int)



# Company view

# Columns
cols=['ID', 'Order_Date']

# Lines
df_aux=df1.loc[:,cols].groupby('Order_Date').count().reset_index()

# Plot bar chart using Plotly
px.bar(df_aux, x='Order_Date', y='ID')

# =============================================================================================================
# Sidebar
# =============================================================================================================

streamlit.header("MarketPlace - Customer View")
image=Image.open('logo_curry_company.jpg')

streamlit.sidebar.image(image, width=250)
streamlit.sidebar.markdown('# Cury Company')
streamlit.sidebar.markdown('## Fastest Delivery in Town')
streamlit.sidebar.markdown("""___""")


date_slider=streamlit.sidebar.slider(
                                'Select a Date',
                                value = datetime(2022, 4, 5),
                                min_value = datetime(2022, 2, 11),
                                max_value = datetime(2022, 4, 6),
                                format='DD-MM-YY')

# st.dataframe(df1) # check dates in the dateframe
streamlit.write('Selected Date', date_slider)
streamlit.sidebar.markdown("""___""")	

traffic_options=streamlit.sidebar.multiselect(
                        'Select the traffic density',
                        ['Low','Medium','High','Jam'],
                        default=['Low','Medium','High','Jam']
                        )

# Date Filter
selected_lines=df1['Order_Date']<date_slider
df1=df1.loc[selected_lines, :]

# Traffic Filter
selected_lines=df1['Road_traffic_density'].isin(traffic_options)
df1=df1.loc[selected_lines, :]


# =============================================================================================================
# Streamlit Layout
# =============================================================================================================

tab1, tab2, tab3 = streamlit.tabs(['Managerial Vision', 'Tactical Vision', 'Geographical Vision'])

with tab1:
    # Order Metric
    with streamlit.container():
        # columns selection
        cols=['ID', 'Order_Date']
        # lines selection
        df_aux=df1.loc[:,cols].groupby('Order_Date').count().reset_index()
        # Header
        streamlit.markdown('# Orders by Day')
        #Plot bar chart with plotly
        fig=px.bar(df_aux, x='Order_Date', y='ID')
        streamlit.plotly_chart(fig, use_container_width=True)
        
    
    
    with streamlit.container():
        col1, col2 = streamlit.columns(2)
        with col1:
            streamlit.markdown('# Traffic Order Share')
            df_aux=df1.loc[:,['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux['percent_deliveries']=df_aux['ID']/df_aux['ID'].sum()
            fig=px.pie(df_aux, values='percent_deliveries', names='Road_traffic_density')
            streamlit.plotly_chart(fig, use_container_width=True)
        with col2:
            streamlit.markdown('# Traffic Order City')
            df_aux=df1.loc[:,['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
            fig=px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
            streamlit.plotly_chart(fig, use_container_width=True)        
            

        
        
with tab2:
    with streamlit.container():
        streamlit.markdown('# Weekly Orders')
        df1['week_of_year']=df1['Order_Date'].dt.strftime('%U')
        df_aux=df1.loc[:,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        fig=px.line(df_aux, x='week_of_year', y='ID')
        streamlit.plotly_chart(fig, use_container_width=True)
    
    with streamlit.container():
        streamlit.markdown('# Orders Share by Week')
        df_aux01=df1.loc[:,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        df_aux02=df1.loc[:,['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
        df_aux=pd.merge(df_aux01,df_aux02, on='week_of_year')
        df_aux['order_by_delivery']=df_aux['ID']/df_aux['Delivery_person_ID']
        fig=px.line(df_aux, x='week_of_year', y='order_by_delivery')
        streamlit.plotly_chart(fig, use_container_width=True)
    
with tab3:
    streamlit.markdown('# Orders Map')
    # streamlit.markdown('# Orders by Day')
    df_aux=df1.loc[:,['City', 'Road_traffic_density','Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
        
    map=folium.Map()
    
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],location_info['Delivery_location_longitude']],popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static(map, width=1024, height=600)
    map
# streamlit run company_view.py

