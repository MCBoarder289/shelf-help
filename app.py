from dash import Dash, html, dcc, callback, Output, Input, State, ctx, clientside_callback, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from source.utils.models import MAX_PAGES
from source.utils.scraping import retrieve_goodreads_shelf_data, get_library_availability
from source.utils.converters import book_to_cards
from flask_caching import Cache
import random

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc_css, dbc.icons.FONT_AWESOME], title="Shelf Help")
app._favicon = "assets/images/favicon.ico"
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
<title>Shelf Help</title>
<link rel="manifest" href="./assets/manifest.json" />
{%metas%}
{%favicon%}
{%css%}
</head>
<script type="module">
   import 'https://cdn.jsdelivr.net/npm/@pwabuilder/pwaupdate';
   const el = document.createElement('pwa-update');
   document.body.appendChild(el);
</script>
<body>
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', ()=> {
      navigator
      .serviceWorker
      .register('./assets/sw01.js')
      .then(()=>console.log("Ready."))
      .catch(()=>console.log("Err..."));
    });
  }
</script>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''

server = app.server
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache',
    'CACHE_THRESHOLD': 100
})

timeout = 1800  # 30 minutes

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch(id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)


modal = html.Div(
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Library Status")),
                dbc.ModalBody("This is the content of the modal", id="library-details"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Open Library Search", id="open-library", className="ms-auto", target="_blank"
                    )
                ),
            ],
            id="modal",
            centered=True,
            is_open=False,
        )
)

ios_install_tab = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P('To install in iOS, simply "Add to Home Screen"', className="card-text"),
                html.P("Like this video:", className="card-text"),
                html.Img(src="https://drive.google.com/thumbnail?id=1i727hdYfgqoliWkxTxHyaT7b5jE3QISY", style={"max-width": "50%", "max-height": "50%"})
            ]
        ),
    ]
)

how_to_tab = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P('TODO: Add instructions here"', className="card-text"),
                html.P(
                    f"If the number of books returned is lower than you expected, it's because there are up to {MAX_PAGES} pages that we select. We still randomly select from all of them.",
                    className="card-text"),
                html.P('If the book is unavailable in the Library, still use that button and manually search.',
                       className="card-text"),
            ]
        )
    ]
)

collapse = [
    dbc.Button(
        [dbc.Label(className="fa fa-info-circle"), " Info"],
        id="info-button",
        size="sm",
        className="mb-3",
        color="info",
        n_clicks=0,
    ),
    dbc.Collapse(
        [
            dbc.Tabs(
                [
                    dbc.Tab(ios_install_tab, label="iOS Install"),
                    dbc.Tab(how_to_tab, label="How to use")
                ]
            )
        ],
        id="collapse",
        is_open=False,
    ),
]

app.layout = dbc.Container(
    style={"padding-left": "calc(var(--bs-gutter-x)* 1.5)", "padding-right": "calc(var(--bs-gutter-x)* 1.5)"},
    children=[
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        dbc.Stack(
                            [
                                dcc.Store(id='signal'),  # signal value to trigger callbacks
                                html.Img(id="app-icon", src="https://drive.google.com/thumbnail?id=1nL4BOE7WqG7tPHQLfOq5tBcbazXN06dt",
                                         style={'width': '5.5vw', 'border-radius': '20%',
                                                'max-width': '100%', 'height': 'auto'}, className="dbc"),
                                html.H1(children='Shelf Help', style={'textAlign': 'center'}, className="dbc")
                            ],
                            direction="horizontal",
                            gap=3
                        )

                    ],
                    align="center"
                ),
            ],

            id="title-row",
            align="center"
        ),
        dbc.Row(
            dbc.Col(
                children=color_mode_switch,
            ),
            id="color-mode-row",
            align="center"
        ),
        dbc.Row(
            dbc.Col(
                children=collapse,
                align="center"
            ),
            id="help-row",
            align="center"
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Label('Enter Shelf Url:', id='input-label'),
                        dbc.InputGroup(
                            [
                                dbc.DropdownMenu(
                                    label="Examples",
                                    children=[
                                        dbc.DropdownMenuItem("MC - To Read", id="to-read-item"),
                                        dbc.DropdownMenuItem("MC - Currently Reading", id="currently-reading-item")
                                    ]
                                ),
                                dbc.Input(id='input-box', type='text', ),
                            ]
                        ),
                        html.Br(),
                        html.Label('Select Number of Suggestions:', id='slider-label'),
                        dcc.Slider(id='slider-number', className="dbc", min=1, max=5, step=1, value=3),
                        html.Br(),
                        dbc.Button('Retrieve Shelf', id='retrieve-button', color='primary'),
                    ],
                ),
            ],
            id="input-row"
        ),
        dbc.Row(
            children=[
                dcc.Loading(
                    id='loading-shelf',
                    type="default",
                    className="dbc",
                    children=[
                        html.Div(id='shelf-url-output'),
                        html.Br()
                    ]
                ),
                dcc.Loading(
                    id="library-loading",
                    type="default",
                    className="dbc",
                    children=[
                        html.Div(id="library-loading-output")
                    ]
                ),
            ],
            id="loading-row"
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.Div(
                            [
                                html.Br(),
                                dbc.Alert(
                                    "Hello! I am an auto-dismissing alert!",
                                    id="alert-auto",
                                    is_open=False,
                                    dismissable=False,
                                    duration=4000,
                                    color="warning",
                                ),
                                dbc.CardGroup(id="results", style={"maxHeight": "600px", "overflow": "scroll"})
                            ]
                        ),
                        modal
                    ]

                ),

            ],
            id="alerts-row"
        ),
    ]
)


@cache.memoize(timeout=timeout)
def fetch_shelf_data_from_goodreads(url):
    return retrieve_goodreads_shelf_data(shelf_url=url)


@callback(
    Output("input-box", "value"),
    Input('to-read-item', 'n_clicks'),
    Input('currently-reading-item', 'n_clicks'),

)
def populate_examples(to_read_btn, currently_reading_btn):
    if ctx.triggered_id == 'to-read-item':
        return "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read"
    elif ctx.triggered_id == 'currently-reading-item':
        return "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=currently-reading"


@callback(
    Output("alert-auto", "is_open"),
    Output("alert-auto", "children"),
    Output("shelf-url-output", "children"),
    Output('signal', 'data'),
    Output('results', 'children'),
    Input('retrieve-button', 'n_clicks'),
    State('input-box', 'value'),
    State('slider-number', 'value')
)
def get_shelf_data(n_clicks, shelf_url, slider_number):
    if n_clicks is None:
        raise PreventUpdate
    if shelf_url is None:
        return True, "Invalid Entry: Must not be blank and url starts with http:// or https://", None, None, None
    if not shelf_url.startswith("http://") and not shelf_url.startswith("https://"):
        return True, "Invalid Entry: Must start with http:// or https://", None, shelf_url, None

    # TODO: Make the pattern matching better, not just "Starts With"
    shelf_data = fetch_shelf_data_from_goodreads(shelf_url)
    sample_number = slider_number if len(shelf_data) >= slider_number else len(shelf_data)
    shelf_choices = list(map(book_to_cards, random.sample(shelf_data, sample_number)))

    return False, None, f"Retrieved Shelf Data: {len(shelf_data)} Books Retrieved", shelf_url, shelf_choices


@callback(
    Output("modal", "is_open"),
    Output("library-details", "children"),
    Output("open-library", "href"),
    Output("library-loading-output", "children"),
    Input({"type": "library-button", "index": ALL}, "n_clicks"),
    State("modal", "is_open"),
    State({"type": "library-store", "index": ALL}, "data")
)
def toggle_modal(n_clicks, is_open, library_url):
    if ctx.triggered_id is None or len(n_clicks) == 0:
        return False, None, None, None
    triggered_key_prefix = ''.join(str(ctx.triggered_id).replace("'", '"').split())
    if ctx.inputs[triggered_key_prefix + ".n_clicks"] is not None:
        library_links = ctx.states[triggered_key_prefix.replace("button", "store") + ".data"]
        library_status, library_link = get_library_availability(library_links)
        return not is_open, library_status, library_link, None
    return is_open, None, None, None


@app.callback(
    Output("collapse", "is_open"),
    Input("info-button", "n_clicks"),
    State("collapse", "is_open"),
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

if __name__ == '__main__':
    app.run(debug=True)
