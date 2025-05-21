import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------
# Streamlit Dashboard for BU Performance using CSV files
# ---------------------------
# This dashboard reads data from CSV files:
# - Overall_BU.csv : Contains overall BU performance data (originally from sheet 1)
# - BU1.csv        : Contains BU1 specific data (originally from sheet 2)
#
# The dashboard has 4 tabs:
# 1. Overall BU Performance (loads Overall_BU.csv)
# 2. BU1 (loads BU1.csv)
# 3. BU2 (placeholder text)
# 4. BU3 (placeholder text)
#
# If CSV files are missing, mock data will be used as fallback.
#
# CSV files must have the expected columns as per the original Excel structure.
# For example, the date column is expected to be named 'Unnamed: 19' with date strings like '28/02/2025'.
# Adjust column names if your CSV structure differs.
# ---------------------------

st.set_page_config(page_title="BU Performance Dashboard", layout="wide")

# CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 1rem 2rem;
    }
    .tab-content {
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 0 10px rgb(0 0 0 / 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Data Loading Functions
# ---------------------------

def load_csv_data(file_path):
    """
    Load CSV data from the given file path.
    Returns a pandas DataFrame or None if file not found.
    """
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
            return None
    else:
        return None

# ---------------------------
# Data Processing Functions
# ---------------------------

def process_csv_data(df_overall, df_bu1):
    """
    Process the loaded CSV data into a dictionary of dataframes and summary info.
    This function is adapted from the original process_excel_data logic.
    
    Parameters:
    - df_overall: DataFrame loaded from Overall_BU.csv
    - df_bu1: DataFrame loaded from BU1.csv
    
    Returns:
    - data: dict containing processed data for dashboard use
    """
    data = {}

    # Process Overall BU data
    if df_overall is not None:
        # Filter data for Feb 28, 2025 and Jan 31, 2025 based on 'Month' column (date column)
        feb_data_overall = df_overall[df_overall['Month'] == '2025-02']
        jan_data_overall = df_overall[df_overall['Month'] == '2025-01']

        try:
            data['overall'] = {
                'feb_budget': feb_data_overall['Budget'].sum() if 'Budget' in feb_data_overall.columns else None,
                'feb_expense': feb_data_overall['Expense'].sum() if 'Expense' in feb_data_overall.columns else None,
                'jan_budget': jan_data_overall['Budget'].sum() if 'Budget' in jan_data_overall.columns else None,
                'jan_expense': jan_data_overall['Expense'].sum() if 'Expense' in jan_data_overall.columns else None,
                'feb_data': feb_data_overall,
                'jan_data': jan_data_overall
            }
        except Exception as e:
            st.warning(f"Error processing Overall_BU.csv data: {e}")
            data['overall'] = {}

    else:
        data['overall'] = {}

    # Process BU1 data
    if df_bu1 is not None:
        # Filter data for Feb 28, 2025 and Jan 31, 2025 based on 'Bulan Quality' column (date column)
        feb_data_bu1 = df_bu1[df_bu1['Bulan Quality'] == '2025-02']
        jan_data_bu1 = df_bu1[df_bu1['Bulan Quality'] == '2025-01']

        try:
            data['bu1'] = {
                'feb_budget': feb_data_bu1['Budget Finance'].sum() if 'Budget Finance' in feb_data_bu1.columns else None,
                'feb_expense': feb_data_bu1['Expense Finance'].sum() if 'Expense Finance' in feb_data_bu1.columns else None,
                'jan_budget': jan_data_bu1['Budget Finance'].sum() if 'Budget Finance' in jan_data_bu1.columns else None,
                'jan_expense': jan_data_bu1['Expense Finance'].sum() if 'Expense Finance' in jan_data_bu1.columns else None,
                'feb_data': feb_data_bu1,
                'jan_data': jan_data_bu1
            }
        except Exception as e:
            st.warning(f"Error processing BU1.csv data: {e}")
            data['bu1'] = {}
    else:
        data['bu1'] = {}

    return data

# ---------------------------
# Mock Data Generation (Fallback)
# ---------------------------

def generate_mock_data():
    """
    Generate mock data dictionary for dashboard when CSV files are missing.
    """
    mock_data = {
        'overall': {
            'feb_budget': 300000,
            'feb_expense': 250000,
            'jan_budget': 280000,
            'jan_expense': 230000,
            'feb_data': pd.DataFrame({
                'BU': ['BU1', 'BU2', 'BU3'],
                'Budget': [100000, 100000, 100000],
                'Expense': [90000, 80000, 80000],
                'Month': ['2025-02', '2025-02', '2025-02']
            }),
            'jan_data': pd.DataFrame({
                'BU': ['BU1', 'BU2', 'BU3'],
                'Budget': [90000, 95000, 95000],
                'Expense': [85000, 90000, 85000],
                'Month': ['2025-01', '2025-01', '2025-01']
            })
        },
        'bu1': {
            'feb_budget': 100000,
            'feb_expense': 90000,
            'jan_budget': 90000,
            'jan_expense': 85000,
            'feb_data': pd.DataFrame({
                'Budget Finance': [100000],
                'Expense Finance': [90000],
                'Bulan Quality': ['2025-02']
            }),
            'jan_data': pd.DataFrame({
                'Budget Finance': [90000],
                'Expense Finance': [85000],
                'Bulan Quality': ['2025-01']
            })
        }
    }
    return mock_data

# ---------------------------
# Visualization Functions
# ---------------------------

def plot_budget_vs_expense(df, title):
    """
    Plot a bar chart comparing Budget vs Expense from a dataframe.
    Expects dataframe with columns 'Category', 'Budget', 'Expense' or their equivalents.
    """
    if df is None or df.empty:
        st.info("No data available to plot.")
        return

    # Determine which columns to use for Budget and Expense
    if 'Budget' in df.columns and 'Expense' in df.columns:
        budget_col = 'Budget'
        expense_col = 'Expense'
        category_col = 'BU' if 'BU' in df.columns else 'Category'
    elif 'Budget Finance' in df.columns and 'Expense Finance' in df.columns:
        budget_col = 'Budget Finance'
        expense_col = 'Expense Finance'
        # For BU1, no explicit category column, create one for plotting
        category_col = 'Category'
        df = df.copy()
        df[category_col] = 'BU1'
    else:
        st.info("Data columns for Budget and Expense not found.")
        return

    df_melted = df.melt(id_vars=[category_col], value_vars=[budget_col, expense_col], var_name='Type', value_name='Amount')
    fig = px.bar(df_melted, x=category_col, y='Amount', color='Type', barmode='group', title=title)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Main Dashboard Logic
# ---------------------------

def main():
    st.title("BU Performance Dashboard (CSV Data)")

    # Load CSV files
    df_overall = load_csv_data("Overall_BU.csv")
    df_bu1 = load_csv_data("BU1.csv")

    # Process data
    data = process_csv_data(df_overall, df_bu1)

    # If no data loaded, use mock data
    if (df_overall is None) and (df_bu1 is None):
        st.warning("CSV files not found. Using mock data.")
        data = generate_mock_data()

    # Tabs
    tabs = st.tabs(["Overall BU Performance", "BU1", "BU2", "BU3"])

    # Tab 1: Overall BU Performance
    with tabs[0]:
        st.header("Overall BU Performance")
        if data['overall'].get('feb_data') is not None and not data['overall']['feb_data'].empty:
            st.subheader("February 2025 Data")
            st.dataframe(data['overall']['feb_data'])
            plot_budget_vs_expense(data['overall']['feb_data'], "Overall BU Budget vs Expense (Feb 2025)")
        else:
            st.info("No Overall BU data available for February 2025.")

        if data['overall'].get('jan_data') is not None and not data['overall']['jan_data'].empty:
            st.subheader("January 2025 Data")
            st.dataframe(data['overall']['jan_data'])
            plot_budget_vs_expense(data['overall']['jan_data'], "Overall BU Budget vs Expense (Jan 2025)")
        else:
            st.info("No Overall BU data available for January 2025.")

    # Tab 2: BU1
    with tabs[1]:
        st.header("BU1 Performance")
        if data['bu1'].get('feb_data') is not None and not data['bu1']['feb_data'].empty:
            st.subheader("February 2025 Data")
            st.dataframe(data['bu1']['feb_data'])
            plot_budget_vs_expense(data['bu1']['feb_data'], "BU1 Budget vs Expense (Feb 2025)")
        else:
            st.info("No BU1 data available for February 2025.")

        if data['bu1'].get('jan_data') is not None and not data['bu1']['jan_data'].empty:
            st.subheader("January 2025 Data")
            st.dataframe(data['bu1']['jan_data'])
            plot_budget_vs_expense(data['bu1']['jan_data'], "BU1 Budget vs Expense (Jan 2025)")
        else:
            st.info("No BU1 data available for January 2025.")

    # Tab 3: BU2 placeholder
    with tabs[2]:
        st.header("BU2 Performance")
        st.info("No BU2 data available yet.")

    # Tab 4: BU3 placeholder
    with tabs[3]:
        st.header("BU3 Performance")
        st.info("No BU3 data available yet.")

if __name__ == "__main__":
    main()