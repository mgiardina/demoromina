
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pages import contact
from app import server

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(id="input-on-search",type="text", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", id='search-val',n_clicks=0, color="light", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dcc.Link(html.I(id='home-button', n_clicks=0, className='fa fa-home',
                         style={'color': 'white', 'fontSize': '2rem'}), href='/home')),
                    dbc.Col(dbc.NavbarBrand("Dash App Template", className="ml-2")),
                ],
                align="center",
                className="ml-auto flex-nowrap mt-3 mt-md-0",
                no_gutters=True,
            ),
        ),
 
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            dbc.Nav(
                [search_bar],className="ml-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True,
        ),        
        ],
        fluid=True,
    ),    
    color="#2c6693",
    dark=True,
)

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 60,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f4f6f8",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}






submenu_1 = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col("Menu 1"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-1",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Page 1.1", href="/page-1/1"),
            dbc.NavLink("Page 1.2", href="/page-1/2"),
        ],
        id="submenu-1-collapse",
    ),
]

submenu_2 = [
    html.Li(
        dbc.Row(
            [
                dbc.Col("Menu 2"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-2",
    ),
    dbc.Collapse(
        [
            dbc.NavLink("Page 2.1", href="/page-2/1"),
            dbc.NavLink("Page 2.2", href="/page-2/2"),
        ],
        id="submenu-2-collapse",
    ),
]


buttons = [dbc.Button("Contact", color="info", href='/contact',className="mr-1"),
    ]


sidebar = html.Div(
    [
        html.H2("Dash Sidebar", className="display-8"),
        html.Hr(),
        html.P(
            "Example links", className="lead"
        ),
        dbc.Nav(submenu_1 + submenu_2 + buttons, vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)


content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), navbar,sidebar, content])


# this function is used to toggle the is_open property of each Collapse
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""


for i in [1, 2]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1/1"]:
        return html.P("This is the content of page 1.1!")
    elif pathname == "/page-1/2":
        return html.P("This is the content of page 1.2. Yay!")
    elif pathname == "/page-2/1":
        return html.P("Oh cool, this is page 2.1!")
    elif pathname == "/page-2/2":
        return html.P("No way! This is page 2.2!")
    elif pathname == '/contact':
        return contact.layout   
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


server = flask.Flask(__name__)
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    app.run_server(debug=True)
