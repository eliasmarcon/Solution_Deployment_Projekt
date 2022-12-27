import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import html

# app Main
app = dash.Dash(__name__, use_pages = True, external_stylesheets = [dbc.themes.LUX],
                suppress_callback_exceptions = True)

# load bootstrap template
load_figure_template("LUX")

# enable assets/customs.css
app.css.config.serve_locally = True

# define navigation bar
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

# define layout
app.layout = dbc.Container(
    [
        # define dashboard header
        dbc.Row([
            dbc.Col(
                html.Div(
                            className='div-for-text',
                            children=[
                                html.H1('Worlds biggest Data Breaches & Hacks', style={'fontSize': 35, 'textAlign' : 'center'}), 
                                html.P('A basic dashboard with Dash and Plotly.', style={'fontSize': 20, 'textAlign' : 'center'})
                            ]
                        )
            )
        ]),

        html.Hr(),

        # define content layout
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

    app.run_server(host = '0.0.0.0', port = 80, debug=True)
    return 'Done!'

if __name__ == '__main__':

    start()




