import dash
import dash_bootstrap_components as dbc
from dash import html


# App Main
app = dash.Dash(__name__, use_pages = True, external_stylesheets = [dbc.themes.SPACELAB], suppress_callback_exceptions = True)


sidebar = dbc.Nav(
                    [
                        dbc.NavLink(
                            [
                                html.Div(page["name"], className = "ms-2"),
                            ],
                            href = page["path"],
                            active = "exact",
                        )
                        for page in dash.page_registry.values()
                    ],
                    vertical = False,
                    pills = True,
                    className = "bg-light",
)

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                html.Div(
                            className='div-for-text',
                            children=[
                                html.H1("Worlds biggest Data Breaches & Hacks", style={'fontSize': 35, 'textAlign' : 'center'}), 
                                html.P('''A basic Dashboard with Dash and Plotly, showing the worlds biggest data breaches.''', style={'fontSize': 20, 'textAlign' : 'center'})
                            ]
                        )
            )
        ]),

        html.Hr(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        sidebar
                    ])
            ]
        ),

        html.Hr(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dash.page_container
                    ])
            ]
        )
    ], fluid = True)



# Run the app
def start():   

    app.run_server(host = '0.0.0.0', port = 80)
    return 'Done!'

if __name__ == '__main__':

    start()
    # app.run_server(debug = True, port = "8051")




