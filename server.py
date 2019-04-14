import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import mysql.connector as mysql

query_all_collisions = (
    "SELECT `latitude`, `longitude`, `impact_type`, `date` FROM `collisions`"
)

db = mysql.connect(
    host="localhost",
    user="user",
    password="password",
    database="traffic"
)

cursor = db.cursor()

app = dash.Dash(__name__)


def collisions_map():
    cursor.execute(query_all_collisions)
    points = cursor.fetchall()
    # print(points)

    mapbox_token = "pk.eyJ1IjoiZGFua2F0IiwiYSI6ImNqdWdmYmZwdzBrb3IzeW5xcjdlZHdjbXQifQ.BaqHnmIJrZzFl3e7M81ksQ"

    data = [
        go.Scattermapbox(
            lat=[point[0] for point in points],
            lon=[point[1] for point in points],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=[point[2] + ", " + point[3] for point in points],
        )
    ]

    layout = go.Layout(
        autosize=True,
        height=800,
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

    return dcc.Graph(
        id='collisions-toronto',
        figure=fig
    )


def collisions_per_month():
    cursor.execute(query_all_collisions)
    points = cursor.fetchall()
    monthMap = dict()
    for point in points:
        date = point[3]
        month = date.split("-")[1]
        if month not in monthMap:
            monthMap[month] = 1
        else:
            monthMap[month] += 1

    months = sorted([m for m, _ in monthMap.items()])
    counts = [count for _, count in monthMap.items()]
    data = [
        {
            'x': months,
            'y': counts,
            'type': 'bar',
            "name": "collision"
        }
    ]

    layout = {
        "xaxis": {"title": "Month"},
        "yaxis": {"title": "Number of Fatal Collisions"},
        "title": "Number of Fatal Collisions Per Month"
    }

    fig = dict(data=data, layout=layout)

    return dcc.Graph(
        id='collisions-toronto-per-month',
        figure=fig
    )


app.layout = html.Div(children=[
    collisions_map(),
    collisions_per_month()
])

if __name__ == '__main__':
    app.run_server(debug=True)
