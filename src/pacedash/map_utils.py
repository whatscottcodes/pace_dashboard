import plotly.graph_objs as go
from .helpers_configs import color_palette, sql_return_df


def ppts_address_map(mapbox_access_token):
    """
    Creates a map of participants, colored based on enrollment status
    
    Args:
        mapbox_access_token: public Mapbox Access Token
            See https://plot.ly/python/scattermapbox/ for more information

     Returns:
         dict: contianging plotly figure data and layout information
    """

    enrolled_address_query = """
        SELECT (p.first || ' ' || p.last) as name, (a.address || ', ' || a.city)
        as full_address, a.lat, a.lon
        FROM addresses a
        JOIN ppts p on a.member_id=p.member_id
        JOIN enrollment e on p.member_id=e.member_id
        WHERE e.disenrollment_date IS NULL
        GROUP BY a.member_id
        """

    disenrolled_address_query = """
        SELECT (p.first || ' ' || p.last) as name, (a.address || ', ' || a.city)
        as full_address, a.lat, a.lon
        FROM addresses a
        JOIN ppts p on a.member_id=p.member_id
        JOIN enrollment e on p.member_id=e.member_id
        WHERE e.disenrollment_date NOT NULL
        GROUP BY a.member_id
        """
    enrolled_df = sql_return_df(enrolled_address_query, None, None)
    disenrolled_df = sql_return_df(disenrolled_address_query, None, None)

    fig_data = [
        go.Scattermapbox(
            lat=disenrolled_df.lat,
            lon=disenrolled_df.lon,
            mode="markers",
            name="Disenrolled",
            marker=dict(color=color_palette[0], size=10),
            line=dict(width=0),
            text=disenrolled_df.name + "<br>" + disenrolled_df.full_address,
            hoverinfo="text",
        ),
        go.Scattermapbox(
            lat=enrolled_df.lat,
            lon=enrolled_df.lon,
            mode="markers",
            name="Enrolled",
            marker=dict(color=color_palette[2], size=10),
            line=dict(width=0),
            text=enrolled_df.name + "<br>" + enrolled_df.full_address,
            hoverinfo="text",
        ),
    ]

    fig_layout = go.Layout(
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"pad": 5, "l": 50, "r": 55, "t": 35, "b": 35},
        hovermode="closest",
        showlegend=True,
        legend=dict(orientation="h", y=-0.015, traceorder="reversed"),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(lat=41.700, lon=-71.4128),
            pitch=0,
            zoom=8.75,
            style="streets",
        ),
        annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=1.035,
                x=0,
                text=f"<b>Map of Participants</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ],
    )
    return dict(data=fig_data, layout=fig_layout)
