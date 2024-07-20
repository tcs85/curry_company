import streamlit as st 
from PIL import Image

st.set_page_config(page_title="Home",page_icon="🤞",layout='wide')

image=Image.open('logo_curry_company.jpg')
st.sidebar.image(image, width=250)


st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard was built to track the growth metrics of Delivery People and Restaurants.
    
    Access the sidebar to the left to choose the views!!!!
    
    ### How to use this Growth Dashboard?
    - Company View:
        - Managerial View: General behavior metrics.
        - Tactical View: Weekly growth indicators.
        - Geographical View: Geolocation insights.
    - Delivery Person View:
        - Tracking weekly growth indicators.

    - Restaurant View:
        - Weekly growth indicators for restaurants.

    Ask for Help
    souza.eq@gmail.com
    """)
