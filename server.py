import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import mysql.connector as mysql

query_all = (
  "SELECT `latitude`, `longitude`, `impact_type` FROM `collisions`"
)

db = mysql.connect(
    host="localhost",
    user="user",
    password="password",
    database="traffic"
)

cursor = db.cursor()
cursor.execute(query_all)
points = cursor.fetchall()
# print(points)

mapbox_token = "pk.eyJ1IjoiZGFua2F0IiwiYSI6ImNqdWdmYmZwdzBrb3IzeW5xcjdlZHdjbXQifQ.BaqHnmIJrZzFl3e7M81ksQ"

app = dash.Dash(__name__)

data = [
    go.Scattermapbox(
        lat=[point[0] for point in points],
        lon=[point[1] for point in points],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=[point[2] for point in points],
    )
]

layout = go.Layout(
    autosize=True,
    height=1000,
    hovermode='closest',
    title="Collision Locations Visualization",
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=43.7,
            lon=-79.4
        ),
        pitch=0,
        zoom=11
    ),
)

fig = dict(data=data, layout=layout)

app.layout = html.Div(children=[
    dcc.Graph(
        id='collisions-toronto',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)