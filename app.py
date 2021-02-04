import dash
import dash_bootstrap_components as dbc

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.LITERA, FA])

app.title = 'Romi APP'

server = app.server