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
from haversine import haversine, Unit
import numpy as np

streamlit.set_page_config(page_title="Associate_view",layout='wide')

#======================================================================================================
# -------------------------------------Functions-------------------------------------------------------
#======================================================================================================


# Cleaning Dataset Function
def clean_code(df1):
    """This Function will clean the dataframe

        Cleaning Steps:
            1. Remove NaN
            2. Converting the columns from text to numbers
            3. Converting Order_Date column to datetime
            4. Removing spaces in the column
            5. Removing the min string from the column data        
        
            Input: Dataframe
            Output: Dataframe
        """
        
        
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

    return df1



# Delivery Time Chart
def chart_delivery_time(df1):
    df_aux=df1.loc[:,['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns=['avg_time', 'std_time']
    df_aux=df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Control',
        x=df_aux['City'],
        y=df_aux['avg_time'],
        error_y=dict(type='data', array=df_aux['std_time'])
    ))            

    fig.update_layout(
        title='Average Time with Error Bars',
        xaxis_title='City',
        yaxis_title='Average Time',
        barmode='group'
    )
    return fig

# Average Distance by City
def average_distance_by_city(df1):
    cols=['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df1['distance']=df1.loc[:,cols].apply(lambda x:
        haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),axis=1)
    avg_distance=df1.loc[:,['City','distance']].groupby('City').mean().reset_index()
    fig=go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0,0.1,0,0])])
    return fig

# Average Std Time Distance by Traffic and City
def avg_std_time_by_traffic_density(df1):
        
    df_aux=(df1.loc[:,['City', 'Time_taken(min)', 'Road_traffic_density']]
    .groupby(['City', 'Road_traffic_density'])
    .agg({'Time_taken(min)': ['mean', 'std']}))
    df_aux.columns=['avg_time', 'std_time']
    df_aux=df_aux.reset_index()
    fig=px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', 
                    color='std_time', color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig



# =============================================================================================================
# ---------------------------------------Begining of the Code--------------------------------------------------
# =============================================================================================================

# ------------------
# Import Dataset
# ------------------
df=pd.read_csv('train.csv')
df1=df.copy()

# ------------------
# Cleaning Data
# ------------------
df1=clean_code(df)



# ------------------
# Filters
# ------------------

# Columns
cols=['ID', 'Order_Date']

# Lines
df_aux=df1.loc[:,cols].groupby('Order_Date').count().reset_index()

# Plot bar chart using Plotly
px.bar(df_aux, x='Order_Date', y='ID')

# =============================================================================================================
# Sidebar
# =============================================================================================================

streamlit.header("Restaurants View")
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

tab1, tab2, tab3 = streamlit.tabs(['Managerial Vision', '', ''])

with tab1:
    with streamlit.container(): #1
        streamlit.title('Overall Metrics')
        col1, col2, = streamlit.columns(2, gap='large')

        with col1:
            delivery_unique=len(df1.loc[:,'Delivery_person_ID'].unique())
            col1.metric('Delivery Unique', delivery_unique)

        with col2:
            cols=['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance']=df1.loc[:,cols].apply(lambda x: haversine(
                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                (x['Delivery_location_latitude'], x['Delivery_location_longitude']),
                unit=Unit.KILOMETERS
                ), axis=1)
            col2.metric('Distance', df1.loc[:,'distance'].mean().round(0))
    with streamlit.container(): #2
        streamlit.markdown("""___""")        
        col1, col2, col3, col4 = streamlit.columns(4, gap='large')
        with col1:
            df_aux=(df1.loc[:,['Time_taken(min)', 'Festival']	]
                    .groupby('Festival')
                    .agg({'Time_taken(min)': ['mean', 'std']}))
            df_aux.columns=['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            df_aux=df_aux.loc[df_aux['Festival']=='Yes', 'avg_time'].round(0)
            col1.metric('Avg Time on Fest', df_aux)
        with col2:
            df_aux=(df1.loc[:,['Time_taken(min)', 'Festival']	]
                    .groupby('Festival')
                    .agg({'Time_taken(min)': ['mean', 'std']}))
            df_aux.columns=['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            df_aux=df_aux.loc[df_aux['Festival']=='Yes', 'std_time'].round(0)
            col2.metric('Std Time on Fest', df_aux)
        with col2:
            df_aux=(df1.loc[:,['Time_taken(min)', 'Festival']	]
                    .groupby('Festival')
                    .agg({'Time_taken(min)': ['mean', 'std']}))
            df_aux.columns=['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            df_aux=df_aux.loc[df_aux['Festival']=='No', 'avg_time'].round(0)
            col3.metric('Avg time w/o Fest', df_aux)
        with col3:
            df_aux=(df1.loc[:,['Time_taken(min)', 'Festival']	]
                    .groupby('Festival')
                    .agg({'Time_taken(min)': ['mean', 'std']}))
            df_aux.columns=['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            df_aux=df_aux.loc[df_aux['Festival']=='No', 'std_time'].round(0)
            col4.metric('Std time w/o Fest', df_aux)

    with streamlit.container(): #3
        streamlit.markdown("""___""")
        col1,col2=streamlit.columns(2, gap='large')
        with col1:
            fig=chart_delivery_time(df1)
            streamlit.plotly_chart(fig)
                            


        
        with col2:
            streamlit.markdown('###### Distance Distribution')    
            df_aux=(df1.loc[:,['City', 'Time_taken(min)', 'Type_of_order']]
                    .groupby(['City', 'Type_of_order'])
                    .agg({'Time_taken(min)': ['mean', 'std']})
                    .round(2))
            df_aux.columns=['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            streamlit.dataframe(df_aux)
        
    with streamlit.container(): #4
        streamlit.markdown("""___""")
        col1, col2 = streamlit.columns(2, gap='large')
        with col1:
            streamlit.markdown('###### Average Distance by City')
            fig=average_distance_by_city(df1)
            streamlit.plotly_chart(fig)

            
        with col2:
            streamlit.markdown('###### Average and Standard Deviation Time by Traffic Density and City')                     
            fig=avg_std_time_by_traffic_density(df1)
            streamlit.plotly_chart(fig)

        
# streamlit run company_view.py

