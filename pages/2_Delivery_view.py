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

streamlit.set_page_config(page_title="delivery_view",layout='wide')
# Import Dataset
df=pd.read_csv(r'../FTC_Python/train.csv')
df1=df.copy()
print(df1.head())

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

streamlit.header("MarketPlace - Delivery Person View")
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

tab1, tab2, tab3 = streamlit.tabs(['Managerial Vision', '_', '_'])

with tab1:
    # Order Metric
    with streamlit.container():
        streamlit.title('Overall Metrics')
        
        col1, col2, col3, col4 = streamlit.columns(4, gap='large')
        
        with col1:
            # streamlit.subheader('Highest Age')
            highest_age=df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Highest Age', highest_age)
        with col2:
            # streamlit.subheader('Lowest Age')
            lowest_age=df1.loc[:,'Delivery_person_Age'].min()
            col2.metric('Lowest Age', lowest_age)           
        with col3:
            # streamlit.subheader('Best Vehicle Condition')
            best_vehicle_condition=df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Best Vehc. Condition', best_vehicle_condition)
        with col4:
            # streamlit.subheader('Worst Vehicle Condition')
            worse_vehicle_condition=df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Worse Vehc. Condition', worse_vehicle_condition)        
    with streamlit.container():
        streamlit.markdown("""___""")
        streamlit.title('Rating')
        
        col1, col2= streamlit.columns(2, gap='large')
        with col1:
            streamlit.markdown('##### Average Rating per Delivery Person')
            df_avg_ratings_per_deliver=(df1.loc[:,['Delivery_person_Ratings', 'Delivery_person_ID']]
                                        .groupby('Delivery_person_ID')
                                        .mean()
                                        .reset_index())
            df_avg_ratings_per_deliver['Delivery_person_Ratings']=df_avg_ratings_per_deliver['Delivery_person_Ratings'].round(2)
            streamlit.dataframe(df_avg_ratings_per_deliver)
        with col2:
            streamlit.markdown('##### Average Rating per Traffic Density')
            df_avg_std_rating_by_traffic=(df1.loc[:,['Delivery_person_Ratings', 'Road_traffic_density']]
                                          .groupby('Road_traffic_density')
                                          .agg({'Delivery_person_Ratings':['mean', 'std']}))
            df_avg_std_rating_by_traffic.columns=['delivery_mean', 'delivery_std']
            df_avg_std_rating_by_traffic['delivery_mean']=df_avg_std_rating_by_traffic['delivery_mean'].round(2)
            df_avg_std_rating_by_traffic['delivery_std']=df_avg_std_rating_by_traffic['delivery_std'].round(2)
            streamlit.dataframe(df_avg_std_rating_by_traffic)
            
            streamlit.markdown('##### Average Rating per Weather Condition') 
            df_avg_std_rating_by_weather=(df1.loc[:,['Delivery_person_Ratings', 'Weatherconditions']]
                                          .groupby('Weatherconditions')
                                          .agg({'Delivery_person_Ratings':['mean', 'std']}))
            df_avg_std_rating_by_weather.columns=['delivery_mean', 'delivery_std']
            df_avg_std_rating_by_weather['delivery_mean']=df_avg_std_rating_by_weather['delivery_mean'].round(2)
            df_avg_std_rating_by_weather['delivery_std']=df_avg_std_rating_by_weather['delivery_std'].round(2)
            streamlit.dataframe(df_avg_std_rating_by_weather)

    with streamlit.container():
        streamlit.markdown("""___""")
        streamlit.title('Delivery Speed')

        col1, col2= streamlit.columns(2, gap='large')
        with col1:
            streamlit.markdown('##### Fastest Delivery Person')
            df2=(df1.loc[:,['Delivery_person_ID', 'City', 'Time_taken(min)']]
            .groupby(['City', 'Delivery_person_ID'])
            .mean()
            .sort_values(['City', 'Time_taken(min)'], ascending=True).reset_index())
            
            df_aux01=df2.loc[df2['City'] == 'Metropolitian', :].head(10).round(0)
            df_aux02=df2.loc[df2['City'] == 'Urban', :].head(10).round()
            df_aux03=df2.loc[df2['City']=='Semi-Urban', :].head(10).round(0)
            
            df3=pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            streamlit.dataframe(df3)
            
            
        with col2:
            streamlit.markdown('##### Lowest Delivery Person')  
            df2=(df1.loc[:,['Delivery_person_ID', 'City', 'Time_taken(min)']]
            .groupby(['City', 'Delivery_person_ID'])
            .mean()
            .sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index())
            
            df_aux01=df2.loc[df2['City'] == 'Metropolitian', :].head(10).round(0)
            df_aux02=df2.loc[df2['City'] == 'Urban', :].head(10).round()
            df_aux03=df2.loc[df2['City']=='Semi-Urban', :].head(10).round(0)
            
            df3=pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            streamlit.dataframe(df3)
            
                  

# streamlit run company_view.py

