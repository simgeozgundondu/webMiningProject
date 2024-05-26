import json
import plotly.express as px
import pandas as pd
import re

# we load json data
with open('artwork.json') as f:
    artworks = json.load(f)


# we edit date and convert dataframe
df = pd.DataFrame(artworks)

# we normalize date datas because some data is wrong
def normalize_date(date_str):
    if 'ca.' in date_str:
        return int(re.findall(r'\d{4}', date_str)[0])
    elif '20th Century' in date_str:
        return
    elif 'Mid' in date_str:
        return
    elif '-' in date_str:
        return int(date_str.split('-')[0])
    elif 's' in date_str:
        return int(date_str.replace('s', '0'))
    elif 'mai' in date_str:
        parts = date_str.split()
        return int(parts[2])

    else:
        return int(date_str)

# part of normalize
df['artwork_date'] = df['artwork_date'].apply(normalize_date)

# we decide set of date
start_date = 1910
end_date = 2024

# we filter by date range
filtered_df = df[(df['artwork_date'] >= start_date) & (df['artwork_date'] <= end_date)]

# we calculate number of artworks for each year
yearly_counts = filtered_df['artwork_date'].value_counts().sort_index()

# we create graph
fig = px.bar(yearly_counts,
             x=yearly_counts.index,
             y=yearly_counts.values,
             labels={'x': 'Year', 'y': 'Number of Artworks'},
             title=f'Number of Artworks from {start_date} to {end_date}',
             text=yearly_counts.values,
             color=yearly_counts.values,
             color_continuous_scale='Viridis')

# we edit some frontend part
fig.update_traces(texttemplate='%{text}', textposition='outside', textfont_size=18)
# we customize graph
fig.update_layout(
    xaxis_title="Date of Artwoks",
    yaxis_title="Number of Artworks",
    font=dict(
        family="Arial, sans-serif",
        size=14,
        color="RebeccaPurple"
    ),

)


# show graph
fig.show()
