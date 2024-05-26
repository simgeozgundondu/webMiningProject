import json
import plotly.graph_objects as go
import pandas as pd
import re

# we load json data
with open('DataVisualization/artwork.json') as f:
    artworks = json.load(f)


# we convert dataframe
df = pd.DataFrame(artworks)

# normalized price
def normalize_price(price_str):

    price_str = price_str.replace(",", "")
    if 'US$' in price_str:
        return float(re.findall(r'[\d.]+', price_str)[0])
    elif '€' in price_str: #convert euro to dolar
        return float(re.findall(r'[\d.]+', price_str)[0]) * 1.1
    elif '£' in price_str:   # convert sterlin to dolar
        return float(re.findall(r'[\d.]+', price_str)[0]) * 1.3
    else:
        return None

# we normalize price
df['normalized_price'] = df['price'].apply(normalize_price)

# we calculate avg price
category_avg_prices = df.groupby('category')['normalized_price'].mean().reset_index()

# we create graph
fig = go.Figure(data=[go.Pie(
    labels=category_avg_prices['category'],
    values=category_avg_prices['normalized_price'],
    textinfo='label+percent',
    hoverinfo='label+value',
    textposition='inside',
    insidetextorientation='radial'
)])

# we write/add avg price
annotations = []
for i, row in category_avg_prices.iterrows():
    annotations.append(dict(
        x=0.0, y= 0.98 - i * 0.1,
        text=f"{row['category']}: ${row['normalized_price']:.2f}",
        showarrow=False,
        xref="paper", yref="paper",
        align="left"
    ))

fig.update_layout(
    title_text='Average Price per Category',
    annotations=annotations
)


# show graph
fig.show()
