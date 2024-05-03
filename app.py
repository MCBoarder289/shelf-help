import random

import dash_bootstrap_components as dbc
import dash_player
from dash import Dash, html, dcc, callback, Output, Input, State, ctx, clientside_callback, ALL
from dash.exceptions import PreventUpdate
from flask_caching import Cache
from furl import furl

from source.parsers.gr import retrieve_goodreads_shelf_data, TOTAL_BOOKS_MAX
from source.parsers.libby import LIBBY_LIBRARIES, search_libby
from source.parsers.library import SUPPORTED_LIBRARIES, parser_factory
from source.utils.converters import book_to_cards
from source.utils.models import Book

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
timeout_mins = timeout // 60

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch(id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

book_or_libby = dbc.Stack(
    children=[
        dbc.Label(id="medium-label", children="Book / Libby:"),
        html.Span(
            [
                dbc.Label(className="fa fa-book", html_for="medium-switch"),
                dbc.Switch(id="medium-switch", value=False, className="d-inline-block ms-1"),
                dbc.Label(className="fa fa-tablet-screen-button", html_for="color-mode-switch")
            ]
        )
    ]
)

tab_nav = dbc.Nav(dbc.NavItem(dbc.NavLink("Back to Top", active=True, href="#")))

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
                dbc.Row(
                    dcc.Markdown(
                        '''
                        ### iOS Install
                        To install in iOS, simply "Add to Home Screen".
                        Like this video:''',
                        className="dbc"
                    ),
                    align="center"
                ),
                dbc.Row(
                    dash_player.DashPlayer(
                        url="https://vimeo.com/939721340?share=copy",
                        loop=True,
                        muted=True,
                        playsinline=True,
                        playing=True,
                        controls=False,
                        width="360px",
                        height="640px"
                    ),
                    align="center"
                ),
                tab_nav
            ]
        ),
    ]
)

how_to_tab = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Markdown(
                    """
                    ## Using Shelf Help
                    Shelf Help was designed to help you make a quick decision on what book should be next in your `to-read` shelf.
                    Two examples of my personal shelves (`to-read` and `currently-reading`) can be selected from the dropdown.
                    
                    ### Step 1: Insert a Goodreads shelf URL
                    Simply copy the `Share` link from goodreads and paste it into the `input box`.
                    
                    Images below show you how to do this:
                    """,
                    className="dbc"
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            html.Img(id="gr-img1",
                                     src="https://drive.google.com/thumbnail?id=1ScHB-yypcEf2gbH7vvuK1qMeLI3BasAX&sz=w1000",
                                     style={'maxWidth': '100%', 'height': 'auto'},
                                     className="dbc")
                        ),
                        dbc.Col(
                            html.Img(id="gr-img2",
                                     src="https://drive.google.com/thumbnail?id=1s2Zpgs6cWdWwK2js3jPqsdET9TWBlY0I&sz=w1000",
                                     style={'maxWidth': '100%', 'height': 'auto'},
                                     className="dbc")
                        ),
                    ],
                    id="gr-imgs",
                    align="center",
                    justify="between"
                ),
                dcc.Markdown(
                    f"""
                    If you directly want to create the url, the following formats are supported currently:
                    * `https://www.goodreads.com/review/list/<numbers go here>?shelf=to-read` 
                    * `https://www.goodreads.com/review/list/<numbers here>-<user-name>?shelf=to-read`
                    * `https://www.goodreads.com/user_shelves/<numbers here>`

                    > **Note:** The `?shelf=to-read` parameter can also be whatever you named a shelf.
                    
                    ### Step 2: Select Number of Suggestions
                    You can select 1-5 suggestions with the provided slider (the default is 3).
                    
                    ### Step 3: Click "Retrieve Shelf"
                    This app will then get all of your shelf data and pick a random subset for you.
                    
                    If the number of books returned is lower than you expected, it's because we only pull the latest {TOTAL_BOOKS_MAX} books from your Goodreads shelf. 
                    
                    > **Note:** The initial pull will take a little time, but once the data is retrieved, it is saved for {timeout_mins} minutes.
                    
                    > **Tip:** If you want a new list of suggestions, just keep pressing the `Retrieve Shelf` Button!
                    
                    ### Step 4: Check Goodreads or Library
                    Once you have some books to look through, you can click on either the `Goodreads Link` or `Check Library` buttons.
                    
                    This allows you to either:
                    * Check the Goodreads reviews for the selected book
                    * See if it is available, either as a physical copy or on Libby (depending on your toggle selection)
                    
                    **Use the `Library Selector` to search your library of choice.**
                    
                    The pop-up showing the Library status allows you to navigate to the website and check it out for yourself.
                    
                    > **Note:** If the book is unavailable in the Library, still use that button and manually search their website if you wish.
                    
                    ### Step 4: (Optional) Bookmark this site
                    
                    If you bookmark the site after you've run a search, it will save that search as the input for next time, so you don't have to copy the url again!                    
                    """,
                    className="dbc"
                ),
                tab_nav
            ]
        )
    ]
)

contributing_tab = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Markdown(
                    f"""
                    ## Contributing to Shelf Help
                    Shelf Help is Open Source, so feel free to check out our [Github](https://github.com/MCBoarder289/shelf-help) and contribute.
                    
                    Feel free to:
                    * Make a branch/pull-request with some changes you'd like to see
                    * Post any issues or requests (other library support, bugs, etc.)
                    
                    Thanks for your interest in helping make this better!
                    """
                ),
                tab_nav
            ]
        )
    ]
)

collapse = [
    dbc.Button(
        [dbc.Label(className="fa fa-info-circle"), " Info"],
        id="info-button",
        size="md",
        className="mb-3",
        color="info",
        n_clicks=0,
    ),
    dbc.Collapse(
        [
            dbc.Tabs(
                [
                    dbc.Tab(how_to_tab, label="How to Use"),
                    dbc.Tab(ios_install_tab, label="iOS Install"),
                    dbc.Tab(contributing_tab, label="Contributing")
                ]
            )
        ],
        id="collapse",
        is_open=False,
    ),
]

library_selector = dbc.Stack(
    [
        html.Label("Library:", className="dbc"),
        dcc.Dropdown(
            options=SUPPORTED_LIBRARIES,
            value="Nashville",
            clearable=False,
            multi=False,
            className="dbc",
            id="library-selector"
        )
    ],
    direction="vertical",
)

app.layout = dbc.Container(
    style={"paddingLeft": "calc(var(--bs-gutter-x)* 1.5)", "paddingRight": "calc(var(--bs-gutter-x)* 1.5)"},
    children=[
        dcc.Location(id='url-location', refresh=False),
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        dbc.Stack(
                            [
                                html.Img(id="app-icon",
                                         src="https://drive.google.com/thumbnail?id=1nL4BOE7WqG7tPHQLfOq5tBcbazXN06dt",
                                         style={'width': '5.5vw', 'borderRadius': '20%',
                                                'maxWidth': '100%', 'height': 'auto'}, className="dbc"),
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
            children=[
                dbc.Col(
                    children=color_mode_switch,
                ),
                dbc.Col(
                    children=book_or_libby,
                    align="center",
                ),
                dbc.Col(
                    children=library_selector,
                    align="center",
                ),
            ],
            id="color-mode-row",
            align="center",
            justify="between"
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
    Input("url-location", "href"),

)
def populate_examples(to_read_btn, currently_reading_btn, url_query):
    if ctx.triggered_id == 'to-read-item':
        return "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=to-read"
    elif ctx.triggered_id == 'currently-reading-item':
        return "https://www.goodreads.com/review/list/158747789-michael-chapman?shelf=currently-reading"
    elif url_query:
        return furl(url_query).args.get("gr_id", "").strip()


@callback(
    Output("alert-auto", "is_open"),
    Output("alert-auto", "children"),
    Output("shelf-url-output", "children"),
    Output('results', 'children'),
    Output("url-location", "search"),
    Input('retrieve-button', 'n_clicks'),
    State('input-box', 'value'),
    State('slider-number', 'value'),
    State("library-selector", "value"),
)
def get_shelf_data(n_clicks, shelf_url, slider_number, library):
    if n_clicks is None:
        raise PreventUpdate
    if shelf_url is None:
        return True, "Invalid Entry: Must not be blank and url starts with http:// or https://", None, None, None
    if not shelf_url.startswith("http://") and not shelf_url.startswith("https://"):
        return True, "Invalid Entry: Must start with http:// or https://", None, None, None

    # TODO: Make the pattern matching better, not just "Starts With"
    shelf_data = fetch_shelf_data_from_goodreads(url=shelf_url.strip())
    sample_number = slider_number if len(shelf_data) >= slider_number else len(shelf_data)
    shelf_choices = list(map(book_to_cards, random.sample(shelf_data, sample_number)))

    return False, None, f"Retrieved Shelf Data: {len(shelf_data)} Books Retrieved", shelf_choices, f"?gr_id={shelf_url}"


@callback(
    Output("modal", "is_open"),
    Output("library-details", "children"),
    Output("open-library", "href"),
    Output("library-loading-output", "children"),
    Input({"type": "library-button", "index": ALL}, "n_clicks"),
    State("modal", "is_open"),
    State({"type": "library-store", "index": ALL}, "data"),
    State("library-selector", "value"),
    State("medium-switch", "value"),
)
def toggle_modal(n_clicks, is_open, library_store, library, is_libby):
    if ctx.triggered_id is None or len(n_clicks) == 0:
        return False, None, None, None
    triggered_key_prefix = ''.join(str(ctx.triggered_id).replace("'", '"').split())
    if ctx.inputs[triggered_key_prefix + ".n_clicks"] is not None:
        book_data: Book = Book(**ctx.states[triggered_key_prefix.replace("button", "store") + ".data"])

        if not is_libby:
            library_parser = parser_factory(library)
            library_status, library_link = library_parser.get_library_availability(
                library_parser.get_library_links(
                    isbn=book_data.isbn,
                    title=book_data.searchable_title,
                    author=book_data.author
                )
            )
        else:
            library_status, library_link = search_libby(
                library_id=library,
                title=book_data.searchable_title,
                author=book_data.author,
            )
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


@app.callback(
    Output("library-selector", "options"),
    Output("library-selector", "value"),
    Input("medium-switch", "value"),
    State("library-selector", "value"),
    prevent_initial_call=True
)
def library_selector_dropdown_switch(is_libby, selected_library):
    if not is_libby:
        return SUPPORTED_LIBRARIES, [d['label'] for d in LIBBY_LIBRARIES if d['value'] == selected_library][0]
    else:
        return LIBBY_LIBRARIES, [d['value'] for d in LIBBY_LIBRARIES if d['label'] == selected_library][0]


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
