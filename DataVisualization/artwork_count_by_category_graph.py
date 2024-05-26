import json
import plotly.express as px

# we load json file
with open('artworkCount.json') as f:
    data = json.load(f)

# we create list for number of categories and artworks
categories = [item['category'] for item in data]
total_artworks = [item['total_artworks'] for item in data]

# we create graph
fig = px.bar(
    x=categories,
    y=total_artworks,
    labels={'x': 'Category', 'y': 'Total Artworks'},
    title='Number of Artworks by Category',
    color=total_artworks,
    color_continuous_scale='Viridis'
)

# we customize graph
fig.update_layout(
    title={
        'text': "Number of Artworks by Category",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Category",
    yaxis_title="Total Artworks",
    font=dict(
        family="Arial, sans-serif",
        size=14,
        color="RebeccaPurple"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=2,
        tickangle=45
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linecolor='black',
        linewidth=2
    )
)

# we set bar width
fig.update_traces(marker=dict(line=dict(color='black', width=1.5)))

# we show graph
fig.show()
