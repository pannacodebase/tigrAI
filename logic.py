import pandas as pd
import plotly.express as px

def generate_plot():
    # Sample logic for generating a plot
    df = pd.DataFrame({
        "x": [1, 2, 3, 4],
        "y": [10, 11, 12, 13]
    })
    fig = px.line(df, x='x', y='y', title='Generated Line Chart')
    return fig
