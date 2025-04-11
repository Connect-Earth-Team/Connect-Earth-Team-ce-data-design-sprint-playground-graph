import pandas as pd
import plotly.express as px
import streamlit as st

from utils import inputs as input_module

# Set page config
st.set_page_config(
    page_title="Energy Usage Comparison",
    layout="centered",
    page_icon="🌍",
    initial_sidebar_state="collapsed",
)

# Load the data
# @st.cache_data <- removed because it was causing a bug in the calculation when inputs changed
def load_data(inputs):
    # Using the data provided but with new column names
    data_raw = pd.read_csv("data/elec_consumption.csv", index_col=0).reset_index(names='Month')
    data_modified = input_module.calculate_impact_of_modifiers(modifiers=inputs, data_raw=data_raw)


    return data_modified

def get_column_pairs():
    """Map display names to actual column name pairs"""
    return {
        "Electricity Bills (£)": ("elec_spend_gbp", "elec_spend_modified_gbp"),
        "Electricity Emissions (kg CO₂e)": ("elec_emissions_kg_co2e", "elec_emissions_modified_kg_co2e"),
        "Electricity Consumption (kWh)": ("elec_consumption_kwh", "elec_consumption_modified"),
    }

def prepare_data_for_plotting(df, metric_display_name):
    """Prepare data for plotting by restructuring it for Plotly"""
    # Get the column pairs for the selected metric
    column_pairs = get_column_pairs()
    base_col, modified_col = column_pairs[metric_display_name]
    
    # Create a new dataframe with the required structure
    plot_data = pd.DataFrame({
        'Month': df['Month'].tolist() + df['Month'].tolist(),
        'Value': df[base_col].tolist() + df[modified_col].tolist(),
        'View': ['original'] * len(df) + ['modified'] * len(df)
    })
    
    return plot_data

def plot_chart(data, metric):
    """Create a Plotly bar chart with the given data and metric"""
    # Set colors based on metric type
    base_color = '#e74c3c' if '£' in metric else ('#2ecc71' if 'kWh' in metric else '#3498db')

    # Define color_discrete_map with original as a lighter (transparent) shade of the base color
    color_discrete_map = {
        'modified': base_color,  # Keep the base color as is
        'original': f'rgba({int(base_color[1:3], 16)}, {int(base_color[3:5], 16)}, {int(base_color[5:7], 16)}, 0.4)'  # Make original 40% opacity (lighter)
    }
    
    fig = px.bar(
        data,
        x='Month',
        y='Value',
        color='View',
        barmode='overlay',
        title=f"{metric} - Comparison View",
        color_discrete_map=color_discrete_map,
        category_orders={'View': ['modified', 'original']}
    )

    fig.update_layout(
        yaxis=dict(
            title=metric.split('(')[1].strip(')') if '(' in metric else metric,
            range=[0, data['Value'].max() * 1.1]
        ),
        xaxis=dict(
            title="Month",
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            categoryorder='array',
            categoryarray=[
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
        ),
        margin=dict(t=40, b=40),
        height=500,
        legend_title="View",
        legend=dict(
            itemclick='toggleothers',  # Optional: allow clicking on legend to hide other traces
            traceorder='reversed',  # Set the order based on how they appear in category_orders
            orientation='v',  # Optionally change the orientation if you prefer horizontal
            itemsizing='constant',
            x=1.05,  # Position the legend, adjust as needed
            y=1.05,  # Adjust vertical position
            tracegroupgap=5
        )
    )

    return fig

def main():
    st.title("Energy Usage Comparison")
    
    inputs = input_module.choose_inputs()

    # Load data
    df = load_data(inputs)
    
    # Get column mapping
    column_pairs = get_column_pairs()
    
    # Metric selection
    metric_options = list(column_pairs.keys())
    selected_metric = st.selectbox("Select Metric", metric_options)
    
    # View selection
    # view_options = ["Both", "Original Only", "Modified Only"]
    # selected_view = st.sidebar.radio("View", view_options)
    selected_view = "Both"
    
    # Prepare data based on selections
    plot_data = prepare_data_for_plotting(df, selected_metric)
    
    # Filter data based on view selection
    if selected_view == "Original Only":
        plot_data = plot_data[plot_data['View'] == 'original']
    elif selected_view == "Modified Only":
        plot_data = plot_data[plot_data['View'] == 'modified']
    
    # Create tabs for visualization and data
    tab1, tab2 = st.tabs(["Chart", "Data"])
    
    with tab1:
        # Plot the chart
        fig = plot_chart(plot_data, selected_metric)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display statistics
        st.subheader("Statistics")
        col1, col2 = st.columns(2)
        
        # Get column names for the selected metric
        base_col, modified_col = column_pairs[selected_metric]
        
        # Calculate statistics for original data
        base_data = df[base_col]
        
        with col1:
            st.markdown("**Original Data**")
            st.write(f"Average: {base_data.mean():.2f}")
            st.write(f"Total: {base_data.sum():.2f}")
            st.write(f"Min: {base_data.min():.2f}")
            st.write(f"Max: {base_data.max():.2f}")
        
        # Calculate statistics for modified data
        modified_data = df[modified_col]
        
        with col2:
            st.markdown("**Modified Data**")
            st.write(f"Average: {modified_data.mean():.2f}")
            st.write(f"Total: {modified_data.sum():.2f}")
            st.write(f"Min: {modified_data.min():.2f}")
            st.write(f"Max: {modified_data.max():.2f}")
    
    with tab2:
        # Display data table
        st.subheader("Raw Data")
        
        # Display only relevant columns
        base_col, modified_col = column_pairs[selected_metric]
        display_cols = ['Month', base_col, modified_col]
        st.dataframe(df[display_cols], use_container_width=True)

if __name__ == "__main__":
    main()