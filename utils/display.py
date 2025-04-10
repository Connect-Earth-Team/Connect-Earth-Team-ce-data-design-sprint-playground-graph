import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    df = pd.read_csv("data/elec_consumption.csv", index_col=0)
    df = df.dropna(how='all')
    df = df.T
    df.index.name = 'Month'
    df.reset_index(inplace=True)
    return df

def melt_data(df, metric, views):
    cols = [f"{metric} ({view})" for view in views]
    df_melted = df[['Month'] + cols].melt(id_vars='Month', var_name='Type', value_name='Value')
    df_melted['View'] = df_melted['Type'].str.extract(r'\((.*?)\)')
    df_melted['Metric'] = metric
    return df_melted

def plot_chart(data, metric):
    color = 'red' if '£' in metric else 'green'
    line_dash_map = {'estimated': 'dash', 'actual': 'solid'}
    fig = px.line(
        data,
        x='Month',
        y='Value',
        color='View',
        line_dash='View',
        line_dash_map=line_dash_map,
        markers=True,
        title=f"{metric} - Comparison View",
        color_discrete_map={'actual': color, 'estimated': color}
    )
    fig.update_layout(
        yaxis=dict(title=metric, range=[0, data['Value'].max() * 1.1]),
        xaxis=dict(title="Month", showline=True, linewidth=1, linecolor='black', mirror=True, ticks='outside'),
        margin=dict(t=40, b=40),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

def calculate_total(df, metric, views):
    return {view: df[f"{metric} ({view})"].sum() for view in views}

def main():
    st.write("## Electricity Usage: Cost & CO2 Savings")
    df = load_data()

    metric = st.selectbox("Select Metric", ['£ elec', 'kg CO2e'])

    col1, col2 = st.columns(2)
    views = []
    with col1:
        if st.checkbox("Show Estimated", value=False):
            views.append('estimated')
    with col2:
        if st.checkbox("Show Actual", value=True):
            views.append('actual')

    if views:
        chart_data = melt_data(df, metric, views)
        plot_chart(chart_data, metric)

        totals = calculate_total(df, metric, views)
        with st.expander("📊 Annual Totals", expanded=True):
            for view, total in totals.items():
                unit = '£' if '£' in metric else 'kg CO₂e'
                st.markdown(f"**{view.capitalize()} Total {metric}:** {total:.2f} {unit}")
    else:
        st.warning("Please select at least one view to display the chart.")

if __name__ == "__main__":
    main()
