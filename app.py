from dash import Dash, html, dcc, callback, Output, Input, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from source.utils.scraping import retrieve_goodreads_shelf_data
from source.utils.converters import book_to_cards
from flask_caching import Cache
import random


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache',
    'CACHE_THRESHOLD': 100
})

timeout = 1800  # 30 minutes


app.layout = html.Div([
    dcc.Store(id='signal'),  # signal value to trigger callbacks
    html.H1(children='Goodreads Shelf Randomizer', style={'textAlign': 'center'}),
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
        dcc.Slider(id='slider-number', min=1, max=5, step=1, value=3),
        html.Br(),
        dcc.Loading(
            id='loading-shelf',
            type="default",
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
        dbc.CardGroup(id="results")
    ]),

])


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

    # TODO: Progress bar/background callback to make this more stable
    #   currently this can take minutes to parse.
    shelf_data = fetch_shelf_data_from_goodreads(shelf_url)
    sample_number = slider_number if len(shelf_data) >= slider_number else len(shelf_data)
    shelf_choices = list(map(book_to_cards, random.sample(shelf_data, sample_number)))

    return False, None, f"Retrieved Shelf Data: {len(shelf_data)} Books Retrieved", shelf_url, shelf_choices


if __name__ == '__main__':
    app.run(debug=True)
