import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_plotly_events import plotly_events
from streamlit_theme import st_theme

# Configure the page to use full width
st.set_page_config(layout="wide")

# Generate random data
np.random.seed(42)
data = pd.DataFrame({
    'p95 Latency (ms)': np.random.rand(50),
    'Accuracy (%)': np.random.rand(50),
    'label': [f"Point {i}" for i in range(50)]
})

# Detect Streamlit theme mode. May not be initialized yet during some runs.
theme_data = st_theme()
if theme_data is not None:
    theme_mode = theme_data['base']
else:
    # Theme data is not available
    theme_mode = 'n/a'

# Choose colors dynamically based on theme
if theme_mode == "dark":
    axis_line_color = "white"
    grid_color = "#444444"
    label_color = "white"
else:
    axis_line_color = "black"
    grid_color = "#cccccc"
    label_color = "black"

# Layout: Split page into two columns with custom width proportions
col1, col2 = st.columns([2, 2.5])  # Adjust the proportions (e.g., 2:3 for left:right column width ratio)

# Left column: Text box
with col1:    
    # st.markdown(
    #     """
    #     <style>
    #     [data-testid="stHorizontalBlock"] > div:first-child {
    #         background-color: lightgrey;
    #         padding: 10px;
    #         border-radius: 5px;
    #         height: 100%;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    st.subheader("Deploy LLMs with Ken")
    st.empty().text("Ken allows you to deploy and query LLMs without having to guesstimate which LLM best suits your application needs.")
    
    st.empty().text("1. Click on a configuration on the right based on the accuracy and latency requirements of your application.")
    
    
    st.code("heherer", language="python")

    selected_text = st.empty()
    selected_text.text("Select a gear plan on the left to get its hash.")

    st.empty().text("2. Create an endpoint with Ken:")
    st.empty().text(" A. Install ken-llm:")
    st.code("pip install ", language="python")
    st.empty().text("or build from source:")

    st.empty().text(" B. Paste the configuration hash as shown in the examples.")

    st.empty().text("TODO: What about hardware, what about qps? Include cost??")


# Right column: Interactive scatter plot
with col2:
    st.subheader("Serving configurations")

    # Create scatter plot (no title)
    fig = px.scatter(
        data, 
        x='p95 Latency (ms)', 
        y='Accuracy (%)', 
        # hover_data=['label']
    )

    # Disable default template so it doesn't override colors
    fig.update_layout(template=None)

    # Transparent background, minimal margins
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=40, t=30, b=80),
        hovermode='closest',
        hoverdistance=1,
        title=None
    )

    # Default Plotly-blue marker color
    fig.update_traces(
        marker=dict(color="#636EFA", size=10),
        selector=dict(mode='markers')
    )

    # Update X axis
    fig.update_xaxes(
        # showline draws the axis line; mirror=True draws it on both sides
        showline=True,  
        mirror=False,            
        linecolor=axis_line_color,
        linewidth=1,
        tickcolor=axis_line_color,
        tickfont=dict(color=label_color),
        titlefont=dict(color=label_color),
        title_standoff=20,  # Add spacing between axis title and ticks
        # Use same color for all grid lines
        showgrid=True,
        gridcolor=grid_color,
        # Make zero-line match grid lines
        zeroline=True,
        zerolinecolor=grid_color,
        zerolinewidth=1
    )

    # Update Y axis
    fig.update_yaxes(
        showline=True,
        mirror=False,
        linecolor=axis_line_color,
        linewidth=1,
        tickcolor=axis_line_color,
        tickfont=dict(color=label_color),
        titlefont=dict(color=label_color),
        title_standoff=20,  # Add spacing between axis title and ticks
        showgrid=True,
        gridcolor=grid_color,
        zeroline=True,
        zerolinecolor=grid_color,
        zerolinewidth=1
    )

    # Display figure and capture click events
    selected_points = plotly_events(
        fig,
        click_event=True,
        hover_event=False,
        override_width="100%",
        override_height=400
    )

    # Handle click data to show text on the left
    if selected_points:
        point_index = selected_points[0]['pointIndex']
        selected_text.text(f"You selected: {data.iloc[point_index]['label']}")
    else:
        selected_text.text("Select a point to see its label.")
