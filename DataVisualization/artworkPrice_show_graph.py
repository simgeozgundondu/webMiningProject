import json
import pandas as pd
import plotly.express as px

# we load json data
with open('DataVisualization/artworkPrice.json') as f:
    data = json.load(f)

# we convert dataframe
df = pd.DataFrame(data)

# we create graph
fig = px.pie(df, values='price', names='title', title='Artwork Prices', color_discrete_sequence=px.colors.qualitative.Pastel)

fig.show()
