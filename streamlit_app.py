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

data_mt_bench = pd.read_json('data/mt_bench.json')


# data_option_1 = pd.DataFrame({
#     'p95 Latency (ms)': [515.2667999267578, 515.9493446350098, 541.0978794097899, 547.9301929473876, 549.250555038452, 552.0882129669188, 585.1516246795653, 600.8272171020508, 913.4064197540279, 945.2121257781982, 950.4408836364746, 950.4849910736084, 977.4526119232177, 1429.4769763946533, 1431.3950538635254, 1520.143985748291, 1696.936273574829, 1724.5442867279053, 46.429538726806626, 96.96412086486816, 200.61945915222168, 2783.5001945495605, 97.82152175903319, 98.40869903564453, 268.88322830200195, 456.26745223999023, 895.2450752258301, 1434.027910232544, 1698.83394241333, 2845.336675643921, 514.8739337921143, 547.2744464874266, 943.9239501953125, 1798.0921268463135, 1800.3742694854736, 187.2, 80.99, 55.02, 3041, 50.4, 94.0, 1878.9772, 70.12],
#     'Score': [5.439775910364146, 6.793785310734464, 6.824858757062147, 6.929775280898877, 7.401129943502825, 7.511299435028248, 7.528248587570621, 7.573446327683616, 7.677966101694915, 7.748587570621469, 7.796610169491525, 7.8192090395480225, 7.861581920903955, 7.8841807909604515, 7.898305084745763, 7.943342776203966, 7.9491525423728815, 7.954674220963173, 4.728291316526611, 6.677871148459384, 6.697478991596639, 7.985994397759104, 6.773109243697479, 6.80672268907563, 7.372549019607843, 7.490196078431373, 7.649859943977591, 7.8655462184873945, 7.9411764705882355, 7.985994397759104, 5.249299719887955, 6.809523809523809, 7.49859943977591, 7.635854341736695, 7.890756302521009, 7.17, 6.205, 5.5594, 8.0198, 5.184, 6.4557, 7.998, 5.971],
#     'label': [f"Option 1 - Point {i}" for i in range(50)]
# })

# data_option_2 = pd.DataFrame({
#     'p95 Latency (ms)': np.random.rand(50) * 2,
#     'Accuracy (%)': np.random.rand(50) * 2,
#     'label': [f"Option 2 - Point {i}" for i in range(50)]
# })

# data_option_3 = pd.DataFrame({
#     'p95 Latency (ms)': np.random.rand(50) * 3,
#     'Accuracy (%)': np.random.rand(50) * 3,
#     'label': [f"Option 3 - Point {i}" for i in range(50)]
# })

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
    st.subheader("Deploy LLMs with Ken")
    st.empty().text("Ken allows you to deploy and query LLMs without having to guesstimate which LLM best suits your application needs. To fit your precise needs, Ken offers a high-resolution cost-accuracy trade-off.")

# Dropdown menu to choose data (preserved outside column context)
with col1:
    options = ["MT-Bench", "HellaSwag", "MMLU"]
    selected_option = st.selectbox("Choose a benchmark:", options)

    # Advanced options
    with st.expander("Declare workload and hardware"):
        st.write('''
            The chart above shows some numbers I picked for you.
            I rolled actual dice for these, so they're *guaranteed* to
            be random.
        ''')

# Map selected option to corresponding data
if True or selected_option == "MT-Bench":
    current_data = data_mt_bench
elif selected_option == "HellaSwag":
    current_data = data_option_2
else:
    current_data = data_option_3

with col1:
    data_point_display = st.empty()
    st.markdown(
        """2. **Create an endpoint** with Ken:\\
            -- **Install ken-llm:** ```pip install ken-llm``` or [build from source](https://stackoverflow.com/).\\
            --  **Configure:** Copy the hash above and paste it as shown [in the examples](https://stackoverflow.com/). 
            """
    )

# Right column: Interactive scatter plot
with col2:
    st.subheader("Serving configurations")

    # Create scatter plot (no title)
    fig = px.scatter(
        current_data, 
        x='p95 Time To First Token (ms)', 
        y='MT-Bench Score', 
        hover_data=['Gear Plan']
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

    # Update traces for hover styling and formatting
    fig.update_traces(
        marker=dict(color="#636EFA", size=12),
        selector=dict(mode='markers'),
        hoverlabel=dict(
            bgcolor="rgba(240, 240, 240, 0.5)",
            font=dict(color="#333333", size=14),  # Dark text with slightly larger font
            bordercolor="#cccccc",  # Subtle border color
            # padding=10  # More padding inside the hover box
        ),
        hovertemplate=(
            "<span style='font-size:16px'><b>MT-Bench Score:</b> %{y:.1f}</span><br>"
            "<span style='font-size:16px'><b>p95 TTFT:</b>  %{x:.1f} ms</span>"
        )
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

        accuracy = current_data.iloc[point_index]['MT-Bench Score']
        latency = current_data.iloc[point_index]['p95 Time To First Token (ms)']
        label = current_data.iloc[point_index]['Gear Plan']

        data_point_display.markdown(
            f"""1. The configuration's hash lets you declare this configuration to Ken.

            Chosen configuration:
            MT-Bench Score:    {accuracy:.2f}
            p95 TTFT:          {latency:.2f} ms
            Cofiguration:      {label}""",
            unsafe_allow_html=True
        )

    else:
        data_point_display.markdown(
            f"""1. **Click** on a configuration on the right based on the accuracy and latency requirements of your application:
            
            Select a configuration on the right.""",
            unsafe_allow_html=True
        )
