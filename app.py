import streamlit as st
import pandas as pd
from utils import add_features, customer_type, run_kmeans
import plotly.express as px


st.set_page_config(
    page_title="Streaming Analytics Dashboard",
    page_icon="📺",
    layout="wide"
)




st.title('Streaming Customer Analytics')

uploaded_file = st.file_uploader('Upload the CSV file', type=['csv'])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df = add_features(df)

    df['segment'] = df.apply(customer_type, axis=1)

    df, kmeans_model = run_kmeans(df)



    discount_users = df[(df["segment"] == "Dormant") | ((df["segment"] == "Risky") & (df["engagement_level"] == "Medium"))]

    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Discount Targets", "User Behavior", "ML Clusters"])
    
    with tab1:
    
        st.subheader("Key Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Users", len(df))
        with col2:
            st.metric("Loyal Users", len(df[df["segment"]=="Loyal"]))

        with col3:
            st.metric("Discount Targets", len(discount_users))
    

    
        st.subheader('Customer Segments Distribution')

        segment_count = df['segment'].value_counts().reset_index()
        segment_count.columns = ['Segment', 'Count']

        fig = px.pie(segment_count,
                    names='Segment',
                    values='Count',
                    title='Loyal vs Dormant vs Risky')

        st.plotly_chart(fig)


        st.subheader("Average watchtime by segment")

        avg_watch = df.groupby("segment")["Watch_Time_Hours"].mean().reset_index()

        fig2 = px.bar(avg_watch,
                    x="segment",
                    y="Watch_Time_Hours",
                    title="Engagement Comparison")

        st.plotly_chart(fig2)

    with tab2:
        st.subheader("Recommended Users for Discount")
        
        
        
        st.write(f"Total Target Users: **{len(discount_users)}**")

        st.dataframe(
            discount_users[[
                "User_ID",
                "Watch_Time_Hours",
                "days_since_last_login",
                "engagement_level",
                "segment"
            ]]
        )


        csv = discount_users.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Discounted List",
            data = csv,
            file_name="discounted_users.csv",
            mime="text/csv")



    with tab3:
        st.subheader("User Behavior Scatter Plot")

        fig3 = px.scatter(
            df,
            x="days_since_last_login",
            y="Watch_Time_Hours",
            color="segment",
            title="Recency vs Engagement",
            hover_data=["User_ID", "engagement_level"])
        st.plotly_chart(fig3)



    with tab4:
        st.subheader("KMeans Clusters")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Cluster Statistics")

            st.dataframe(
                df.groupby("ml_cluster")[["Watch_Time_Hours", "days_since_last_login"]].mean())
            
        with col2:
            fig = px.scatter(
                df,
                x="days_since_last_login",
                y="Watch_Time_Hours",
                color=df["ml_cluster"].astype(str),
                title="KMeans Clusters",
                hover_data=["User_ID", "segment"])

            st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **How Segments Are Defined**

    - Loyal: High engagement & active within 60 days  
    - Dormant: Medium/High engagement but inactive 60–120 days  
    - Risky: Low engagement or inactive >120 days  

    Discount Strategy: Dormant + Risky (Medium engagement)
    """)


else:
    st.info("Please upload a CSV file to continue")


st.warning("""
**Dataset Requirement Notice**

To use this dashboard with your own data, the uploaded CSV must contain these mandatory columns:

- User_ID
- Watch_Time_Hours
- Last_Login (valid date format)
- Subscription_Type

The segmentation logic and K-Means clustering are built using these fields.
Missing or renamed columns may lead to errors or incorrect insights.
""")




