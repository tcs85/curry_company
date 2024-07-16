# curry_company
This repository contains files and scripts to build a company strategy dashboard.
Source: https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset?select=train.csv
This a training project with educational purpose.

#### Content:
1 - Business Problem
2 - Assumptions Made for the Analysis
3- Solution Strategy
4- Top 3 Data Insights
5 - Final Product of the Project
6 - Conclusion
7 - Next Steps

   - **1 - Business Problem:**
     - The Cury Company is a technology company that created an application connecting restaurants, delivery personnel, and customers. Through this application, it is possible to order food from any registered restaurant and receive it at home via a registered delivery person.
     - The company conducts business among restaurants, delivery personnel, and customers, generating a lot of data on deliveries, order types, weather conditions, delivery ratings, etc. Although deliveries are increasing, the CEO lacks full visibility of the company’s growth KPIs.
     - My role as a Data Scientist is to create data solutions for delivery. However, before training algorithms, the company's need is to have the main strategic KPIs organized in a single tool for the CEO to consult and make simple but important decisions.
     - The Cury Company follows a Marketplace business model, intermediating business among three main clients: restaurants, delivery personnel, and customers. To track the growth of these businesses, the CEO wants to see the following growth metrics:

   - **Metrics for the Company:** #Company View
     1. Number of orders per day.
     2. Number of orders per week.
     3. Distribution of orders by traffic type.
     4. Comparison of order volume by city and traffic type.
     5. Number of orders per delivery person per week.
     6. Central location of each city by traffic type.

   - **Metrics for Delivery Personnel:** #Delivery View
     1. Youngest and oldest delivery personnel.
     2. Best and worst vehicle condition.
     3. Average rating per delivery person.
     4. Average rating and standard deviation by traffic type.
     5. Average rating and standard deviation by weather conditions.
     6. Top 10 fastest delivery personnel by city.
     7. Top 10 slowest delivery personnel by city.

   - **Metrics for Restaurants:** #Associates View
     1. Number of unique delivery personnel.
     2. Average distance between restaurants and delivery locations.
     3. Average delivery time and standard deviation by city.
     4. Average delivery time and standard deviation by city and order type.
     5. Average delivery time and standard deviation by city and traffic type.
     6. Average delivery time during festivals.

   - The goal of this project is to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.

### 2 - Assumptions Made for the Analysis:
1. The analysis was conducted with data from 11/02/2022 to 06/04/2022.
2. The assumed business model was Marketplace.
3. The three main business views were: company view, delivery view, and associates view.

### 3- Solution Strategy:
- The strategic panel was developed using metrics that reflect the three main views of the company's business model:
  1. **Company Growth View:**
    - Orders per day
    - Percentage of orders by traffic conditions
    - Number of orders by type and by city
    - Orders per week
    - Number of orders by delivery type
    - Number of orders by traffic conditions and city type

  2. **Delivery Personnel Growth View:**
    - Age of the oldest and youngest delivery personnel
    - Best and worst vehicle rating
    - Average rating per delivery person
    - Average rating by traffic conditions
    - Average rating by weather conditions
    - Average time of the fastest delivery person
    - Average time of the fastest delivery person by city
    
  3. **Restaurant Growth View:**
    - Number of unique orders
    - Average distance traveled
    - Average delivery time during festivals and normal days
    - Standard deviation of delivery time during festivals and normal days
    - Average delivery time by city
    - Distribution of average delivery time by city
    - Average delivery time by order type



### 4- Top 3 Data Insights:
1. The seasonality of order quantity is daily. There is an approximately 10% variation in the number of orders on sequential days.
2. Semi-Urban type cities do not have low, medium and high traffic conditions.
3. The largest variations in delivery time occur during sunny weather.

### 5 - Final Product of the Project:
- An online dashboard, hosted in the cloud and accessible from any device connected to the internet.
- The dashboard can be accessed through this link: [https://project-curry-company.streamlit.app/](https://project-curry-company.streamlit.app/)

### 6 - Conclusion:
- The goal of this project is to create a set of charts and/or tables that display these metrics in the best possible way for the CEO.
- From the Company’s perspective, it can be concluded that the number of orders grew between week 06 and week 13 of the year 2022.

### 7 - Next Steps:
1. Reduce the number of metrics.
2. Create new filters.
3. Add new business views.

### In the Next Class:
**Class 64: Writing the README**
