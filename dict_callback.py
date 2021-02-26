import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


INPUT_FIELDS = ("name", "email", "phone", "address", "dob")

form = html.Div(
    id="form-container",
    children=[
        html.Div(
            children=[
                html.Label(f"Enter your {_input}:"),
                dcc.Input(id=f"input-{_input}", type="text"),
            ]
        )
        for _input in INPUT_FIELDS
    ],
)

app.layout = html.Div(
    children=[
        html.H1(
            children="A simple example demonstrating a callback updating multiple outputs."
        ),
        html.Div(children="This example uses the dict_callback to prepopulate fields"),
        form,
        html.Div(
            html.Button("Prepopulate fields!", id="prepop-button", n_clicks=0),
        ),
        html.Div(
            html.Button("Clear fields", id="clear-button", n_clicks=0),
        ),
    ]
)


@app.dict_callback(
    [Output(f"input-{_input}", "value") for _input in INPUT_FIELDS],
    [Input("prepop-button", "n_clicks"), Input("clear-button", "n_clicks")],
)
def prepopulate(inputs, states):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]["prop_id"]
    # which button was clicked
    if triggered.startswith("prepop"):
        clicked = inputs["prepop-button.n_clicks"]
        if clicked > 0:
            return {
                "input-name.value": "John Smithy-Smith",
                "input-email.value": "smitherino@mail.com",
                "input-phone.value": "555-555-5555",
                "input-address.value": "123 North Rockaway Street",
                "input-dob.value": "12/12/1979",
            }
    elif triggered.startswith("clear"):
        clicked = inputs["clear-button.n_clicks"]
        if clicked > 0:
            return {
                "input-name.value": "",
                "input-email.value": "",
                "input-phone.value": "",
                "input-address.value": "",
                "input-dob.value": "",
            }
    return {}


if __name__ == "__main__":
    app.run_server(debug=True)