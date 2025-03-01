import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import streamlit as st
from sklearn.preprocessing import LabelEncoder
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Set up the Streamlit app configuration
st.set_page_config(layout="wide", page_title="The DATA EXPLORER App", page_icon=":rocket:")

# Web App Title
st.markdown('''
# **The DATA EXPLORER App**

"Here Data Explorer App That Can Make Easy to analyze and visualize your data. You can upload your CSV data and get insights into your data. You can also perform data cleaning, data transformation, and data visualization."

"DataExplore: Discover Insights, Cleanse Data, Excel in Analysis!"
 
---
''')

# Upload CSV data
st.sidebar.header('1. Upload your CSV data')
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

# Helper function to remove duplicate values
def remove_duplicates(dataframe):
    return dataframe.drop_duplicates()

# Helper function to replace missing values based on strategy
def replace_missing_values(dataframe, strategy):
    if strategy == "Replace with 0":
        return dataframe.fillna(0)
    elif strategy == "Replace with mean":
        numeric_columns = dataframe.select_dtypes(include=[np.number]).columns
        dataframe[numeric_columns] = dataframe[numeric_columns].fillna(dataframe[numeric_columns].mean())
        return dataframe
    elif strategy == "Replace with median":
        numeric_columns = dataframe.select_dtypes(include=[np.number]).columns
        dataframe[numeric_columns] = dataframe[numeric_columns].fillna(dataframe[numeric_columns].median())
        return dataframe
    return dataframe

# Helper function to convert categorical data to numerical
def convert_categorical_to_numerical(df):
    label_encoder = LabelEncoder()

    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str)  # Convert all values to strings
        df[col] = label_encoder.fit_transform(df[col])

    return df

# Main Streamlit app
def main():
    global uploaded_file

    if uploaded_file is not None:
        def load_csv():
            csv = pd.read_csv(uploaded_file)
            return csv

        df = load_csv()

        st.header("Data Visualization Options")
        plot_types = st.multiselect("Select Plot Types:", ['Scatter', 'Line', 'Bar', 'Count', 'Histogram', 'Box', 'Heatmap', 'Pair'])

        # Plotting selected plots
        if 'Scatter' in plot_types:
            st.subheader("Scatter Plot")
            selected_x_column = st.selectbox("Select the X-axis column:", df.columns)
            selected_y_column = st.selectbox("Select the Y-axis column:", df.columns)

            height = st.slider("Select the height of the scatter plot:", min_value=1, max_value=20, value=10)
            fig, ax = plt.subplots(figsize=(10, height))
            sns.scatterplot(x=selected_x_column, y=selected_y_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Line' in plot_types:
            st.subheader("Line Plot")
            selected_x_column = st.selectbox("Select the X-axis column:", df.columns)
            selected_y_column = st.selectbox("Select the Y-axis column:", df.columns)

            height = st.slider("Select the height of the line plot:", min_value=1, max_value=20, value=10)
            fig, ax = plt.subplots(figsize=(10, height))
            sns.lineplot(x=selected_x_column, y=selected_y_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Bar' in plot_types:
            st.subheader("Bar Plot")
            selected_x_column = st.selectbox("Select the X-axis column:", df.columns)
            selected_y_column = st.selectbox("Select the Y-axis column:", df.columns)

            height = st.slider("Select the height of the bar plot:", min_value=1, max_value=20, value=10)
            fig, ax = plt.subplots(figsize=(10, height))
            sns.barplot(x=selected_x_column, y=selected_y_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Count' in plot_types:
            st.subheader("Count Plot")
            selected_column = st.selectbox("Select a column:", df.columns)

            height = st.slider("Select the height of the count plot:", min_value=1, max_value=20, value=10)
            fig, ax = plt.subplots(figsize=(10, height))
            sns.countplot(x=selected_column, data=df, ax=ax)
            st.pyplot(fig)

        if 'Histogram' in plot_types:
            st.subheader("Histogram")
            selected_column = st.selectbox("Select a column:", df.columns)

            height = st.slider("Select the height of the histogram plot:", min_value=1, max_value=20, value=10)
            fig, ax = plt.subplots(figsize=(10, height))
            sns.histplot(df[selected_column], kde=True, ax=ax)
            st.pyplot(fig)

        if 'Box' in plot_types:
            st.subheader("Box Plot")
            target_column = st.selectbox("Select a column:", df.columns)
            selected_column = st.selectbox("Select a column:", df.columns)
            
            box_height = st.slider("Select the height of the Box Plot:", min_value=1, max_value=20, value=10)
            fig_box, ax_box = plt.subplots(figsize=(10, box_height))
            sns.boxplot(x=selected_column, y=target_column, data=df, ax=ax_box)
            st.pyplot(fig_box)

        if 'Heatmap' in plot_types:
            st.subheader("Heatmap")
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            correlation_matrix = df[numeric_columns].corr()

            height = st.slider("Select the height of the heatmap:", min_value=1, max_value=20, value=10)
            fig, ax = plt.subplots(figsize=(10, height))
            sns.heatmap(correlation_matrix, annot=True, ax=ax)
            st.pyplot(fig)

        if 'Pair' in plot_types:
            st.subheader("Pair Plot")
            sns.pairplot(df, height=4)
            st.pyplot()

        # Data Transformation Options
        st.header("Data Transformation Options")
        if st.checkbox("Remove Duplicate Values"):
            df = remove_duplicates(df)

        if st.checkbox("Replace Missing Values"):
            missing_value_strategy = st.selectbox(
                "Choose missing value replacement strategy:",
                ["Leave as NaN", "Replace with 0", "Replace with mean", "Replace with median"]
            )
            df = replace_missing_values(df, missing_value_strategy)

        if st.checkbox("Convert Categorical Data to Numerical"):
            df = convert_categorical_to_numerical(df)

        # Display Processed Data
        st.header("Processed DataFrame")
        st.dataframe(df)
        
        if st.button("Download Processed DataFrame as CSV"):
            processed_csv = df.to_csv(index=False)
            href = f'<a href="data:file/csv,{processed_csv}" download="processed_dataframe.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
            
        # EDA Report
        st.header("EDA Report")
        if st.checkbox("Show Report"):
            pr = ProfileReport(df, explorative=True)
            st_profile_report(pr)

    else:
        st.info('Awaiting for CSV file to be uploaded.')

if __name__ == "__main__":
    main()
