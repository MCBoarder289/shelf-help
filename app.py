from dash import Dash, html, dcc, callback, Output, Input, State, ctx, clientside_callback, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from source.utils.scraping import retrieve_goodreads_shelf_data, get_library_availability
from source.utils.converters import book_to_cards
from flask_caching import Cache
import random

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc_css, dbc.icons.FONT_AWESOME], title="Goodreads Shelf Randomizer")
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
            is_open=False,
        )
)


app.layout = dbc.Container(
    [

        dcc.Store(id='signal'),  # signal value to trigger callbacks
        html.H1(children='Goodreads Shelf Randomizer', style={'textAlign': 'center'}),
        color_mode_switch,
        html.Div([
            html.Label('Enter Shelf Url:', id='input-label'),
            dbc.Input(id='input-box', type='text'),
            html.Br(),
            dbc.DropdownMenu(
                label="Examples",
                children=[
                    dbc.DropdownMenuItem("MC - To Read", id="to-read-item"),
                    dbc.DropdownMenuItem("MC - Currently Reading", id="currently-reading-item")
                ]
            ),
            html.Br(),
            html.Label('Select Number of Suggestions:', id='slider-label'),
            dcc.Slider(id='slider-number', className="dbc", min=1, max=5, step=1, value=3),
            html.Br(),
            dcc.Loading(
                id='loading-shelf',
                type="default",
                className="dbc",
                children=[
                    html.Div(id='shelf-url-output')
                ]
            ),
            dbc.Button('Retrieve Shelf', id='retrieve-button', color='primary'),
            dbc.Alert(
                "Hello! I am an auto-dismissing alert!",
                id="alert-auto",
                is_open=False,
                dismissable=False,
                duration=4000,
                color="warning",
            ),
            dbc.CardGroup(id="results", style={"maxHeight": "600px", "overflow": "scroll"})
        ]),
        modal
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

    shelf_data = fetch_shelf_data_from_goodreads(shelf_url)
    sample_number = slider_number if len(shelf_data) >= slider_number else len(shelf_data)
    shelf_choices = list(map(book_to_cards, random.sample(shelf_data, sample_number)))

    return False, None, f"Retrieved Shelf Data: {len(shelf_data)} Books Retrieved", shelf_url, shelf_choices


@callback(
    Output("modal", "is_open"),
    Output("library-details", "children"),
    Output("open-library", "href"),
    Input({"type": "library-button", "index": ALL}, "n_clicks"),
    State("modal", "is_open"),
    State({"type": "library-button", "index": ALL}, "value")
)
def toggle_modal(n_clicks, is_open, library_url):
    if ctx.triggered_id is None or len(n_clicks) == 0:
        return False, None, None
    elif ctx.inputs[''.join(str(ctx.triggered_id).replace("'", '"').split())+".n_clicks"] is not None:
        library_link = ctx.states[''.join(str(ctx.triggered_id).replace("'", '"').split())+".value"]
        library_status = get_library_availability(library_link)
        return not is_open, library_status, library_link
    return is_open, None, None


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
