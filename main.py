import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt

# Set the Streamlit app layout and styling
st.set_page_config(layout="wide", page_title="Customer Churn Dasboard")
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stMetric-label {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌟 Customer Churn Prediction")

# Read the dataset
data = pd.read_excel('data_with_prediction.xlsx')

# Load the feature importance data
feature_importance_file = "feature_importances.xlsx"
feature_importance_df = pd.read_excel(feature_importance_file)

# Load the saved model
model_filename = "small_churn_model.pkl"
with open(model_filename, "rb") as file:
    rf_model = pickle.load(file)

# Default input values (from the first row of your example data)
default_values = {
    'Payment Delay': 27,
    'CustomerID': 1,
    'Tenure': 25,
    'Usage Frequency': 14,
    'Gender_Male': 0,
    'Support Calls': 4,
}

# Sidebar setup
st.sidebar.image("simple logo for Customer Churn Prediction project.png", use_column_width=True)
st.sidebar.header("🔮 Churn Prediction")

# Input fields in the sidebar with default values
data_inputs = {}
for col, default in default_values.items():
    input_type = int if isinstance(default, int) else float
    data_inputs[col] = st.sidebar.number_input(f"{col}", value=default, format="%d" if input_type == int else "%.2f")

# Convert inputs into a DataFrame for prediction
input_df = pd.DataFrame([data_inputs])

# Total Customers in the Data
total_customers = data['CustomerID'].nunique()
median_tenure = data['Tenure'].median()
average_spend = data['Total Spend'].mean()
Usage_frequency = data['Usage Frequency'].mean()

# Cards info
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label='👥 Total Customers', value=total_customers)
with col2:
    st.metric(label='📅 Average Tenure', value=f"{median_tenure:.2f} Days")
with col3:
    st.metric(label='💰 Average Spending', value=f"${average_spend:.2f}")
with col4:
    st.metric(label='🔄 Usage Frequency', value=f"{int(Usage_frequency)} times/month")

# Predict Churn Probability
with st.container():
    st.subheader("🎯 Churn Probability")
    if st.button("Predict Churn Probability"):
        churn_prob = rf_model.predict_proba(input_df)[0][1]
        churn_label = "Yes" if churn_prob > 0.5 else "No"
        st.success(f"Prediction: {churn_label} (Probability: {churn_prob:.2f})")
    else:
        st.info("Enter inputs on the left and click 'Predict Churn Probability'.")

# Layout with two columns
with st.container():
    left_col, right_col = st.columns(2)

    # Feature Importance
    with left_col:
        st.subheader("📊 Feature Importance")
        fig = px.bar(
            feature_importance_df.sort_values("Importance", ascending=True),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance",
            labels={"Variable": "Features", "Feature Importance Score": "Importance"},
            width=700,
            height=500,
        )
        st.plotly_chart(fig)

    # Churn Rate Distribution
    with right_col:
        st.subheader("📈 Churn Rate Distribution")
        churn_counts = data['Churn'].value_counts()
        fig, ax = plt.subplots()
        ax.bar(churn_counts.index, churn_counts.values, color=['bisque', 'red'])
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Not Churned', 'Churned'])
        ax.set_title('Churn Rate Distribution')
        ax.set_ylabel('Number of Customers')
        st.pyplot(fig)

# Additional Insights
with st.container():
    col_a, col_b = st.columns(2)

    # Tenure vs. Churn Rate
    with col_a:
        st.subheader("⏳ Churn Rate by Tenure")
        tenure_churn = data.groupby('Tenure')['Churn'].mean()
        fig = px.line(
            x=tenure_churn.index,
            y=tenure_churn.values,
            labels={'x': 'Tenure (Months)', 'y': 'Churn Rate'},
            title='Churn Rate by Customer Tenure'
        )
        st.plotly_chart(fig)

    # Support Calls vs. Churn Rate
    with col_b:
        st.subheader("📞 Churn Rate by Support Calls")
        calls_churn = data.groupby('Support Calls')['Churn'].mean()
        fig = px.bar(
            x=calls_churn.index,
            y=calls_churn.values,
            labels={'x': 'Number of Support Calls', 'y': 'Churn Rate'},
            title='Churn Rate by Support Calls'
        )
        st.plotly_chart(fig)

# Spending and Usage Frequency Insights
with st.container():
    col_c, col_d = st.columns(2)

    # Usage Frequency vs. Churn Rate
    with col_c:
        st.subheader("🔄 Usage Frequency vs. Churn Rate")
        usage_churn = data.groupby('Usage Frequency')['Churn'].mean()
        fig = px.bar(
            x=usage_churn.index,
            y=usage_churn.values,
            labels={'x': 'Usage Frequency', 'y': 'Churn Rate'},
            title='Churn Rate by Usage Frequency',
        )
        st.plotly_chart(fig)

    # Spending vs. Churn
    with col_d:
        st.subheader("💸 Average Spending by Churn Rate")
        avg_spending = data.groupby('Total Spend')['Churn'].mean()
        fig = px.line(
            x=avg_spending.index,
            y=avg_spending.values,
            labels={'x': 'Average Spending', 'y': 'Churn Status'},
            title='Average Spending by Churn Status',
            color_discrete_sequence=['firebrick']  # Differentiate colors for churned and non-churned
        )
        st.plotly_chart(fig)