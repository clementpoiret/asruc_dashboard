# Import required libraries
import copy
import datetime as dt
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

import utils.etl as etl
# Multi-dropdown options
from controls import (COLNAMES, DPZV, POPULATION, PRETTY_COLNAMES,
                      TIME_FRAME_NAMES, TIME_FRAME_VALUES, TZFC)

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(__name__,
                meta_tags=[{
                    "name": "viewport",
                    "content": "width=device-width"
                }])
app.title = "ASRUC Dashboard"
server = app.server

# Create controls
timeframe_options = [{
    "label": str(TIME_FRAME_NAMES[timeframe]),
    "value": str(timeframe)
} for timeframe in TIME_FRAME_NAMES]

population_options = [{
    "label": str(POPULATION[population]),
    "value": str(population)
} for population in POPULATION]

dpzv_options = [{"label": str(DPZV[dpzv]), "value": str(dpzv)} for dpzv in DPZV]

# Load data
rpe, seances = etl.get_datasets("./data", ["RPE", "Seances"])
postes = pd.read_excel(DATA_PATH.joinpath("postes.xlsx")).iloc[:, [1, -1]]

rpe.Date = pd.to_datetime(rpe.Date)
rpe = rpe.merge(postes,
                on="Nom",
                left_index=False,
                right_index=False,
                how="left")
seances.Date = pd.to_datetime(seances.Date)
seances = seances.merge(postes,
                        on="Nom",
                        left_index=False,
                        right_index=False,
                        how="left")

# Create global chart template
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#182B3A",
    paper_bgcolor="#182B3A",
    font=dict(color="#FFFFFF"),
    legend=dict(font=dict(size=10, color="#FFFFFF"), orientation="h"),
    title="Performance Overview",
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("u-rouen.png"),
                            id="logo",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div([
                            html.H3(
                                "ASRUC",
                                style={"margin-bottom": "0px"},
                            ),
                            html.H5("Rugby", style={"margin-top": "0px"}),
                        ])
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Nous Contacter", id="contact-button"),
                            href="mailto:poiret.clement@outlook.fr",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown("""
                        *Dashboard interactif pour l'analyse des entraînements
                        de l'équipe féminine de l'ASRUC (Association Sportive
                        Rouen Université Club) Rugby. L'application est développée
                        en tant que preuve de concept, et est complètement
                        automatisée.*

                        Version : 1.0.0-2 (2020-02-06)
                        ____
                        """),
                        html.Br(),
                        html.H6(
                            "Modifiez les paramètres d'analyse :",
                            className="control_label",
                        ),
                        html.P("Temps d'analyse:", className="timeframe_label"),
                        dcc.Dropdown(
                            id="timeframe_selector",
                            options=timeframe_options,
                            value=list(TIME_FRAME_VALUES.keys())[0],
                            multi=False,
                            className="dcc_control",
                        ),
                        html.P("Population:", className="population_label"),
                        dcc.Dropdown(
                            id="population_selector",
                            options=population_options,
                            value=list(POPULATION.keys())[0],
                            multi=False,
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(id="mental_text"),
                                        html.P("Fatigue Mentale")
                                    ],
                                    id="mental",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="rpe_text"),
                                        html.P("RPE (Physique)")
                                    ],
                                    id="rpe",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="fcmoy_text"),
                                        html.P("FC Moyenne")
                                    ],
                                    id="fcmoy",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="fcmax_text"),
                                        html.P("FC Max")
                                    ],
                                    id="fcmax",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="charge_graph", 
                                       config={
                                           'staticPlot': True,
                                       })],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="dpzv_selector",
                            options=dpzv_options,
                            multi=False,
                            value=list(DPZV.keys())[0],
                            className="dcc_control",
                        ),
                        dcc.Graph(id="dt_graph", config={
                                           'staticPlot': True,
                                       })
                    ],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="fc_graph", config={
                                           'staticPlot': True,
                                       })],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="pie_dt_graph", config={
                                           'staticPlot': True,
                                       })],
                    className="pretty_container five columns",
                ),
                html.Div(
                    [dcc.Graph(id="sprints_graph", config={
                                           'staticPlot': True,
                                       })],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6("Données Brutes"),
                        dash_table.DataTable(
                            id="table",
                            columns=[{
                                "name": i,
                                "id": i
                            } for i in PRETTY_COLNAMES],
                            page_current=0,
                            page_size=10,
                            page_action="custom",
                            style_header={
                                "border": "1px solid #12202b",
                                "textAlign": "center",
                                "backgroundColor": "#142430",
                                "fontWeight": "bold"
                            },
                            style_cell={
                                "border": "1px solid #142430",
                                "textAlign": "center",
                                "backgroundColor": "#182B3A",
                                "color": "white"
                            },
                            style_table={'overflowX': 'scroll'},
                        ),
                        html.
                        P("Avec DPZV la Distance par Zone de Vitesse, et TZFC le Temps par Zone de Fréquence Cardiaque (FC)"
                         )
                    ],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="power_graph", config={
                                           'staticPlot': True,
                                       })],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    },
)


# Helper functions
def filter_dataset(dataset, timeframe, population):
    upper = dataset.Date.max()
    lower = upper - dt.timedelta(days=timeframe)

    mask = (dataset.Date <= upper) & (dataset.Date >= lower)

    if population:
        mask = mask & (dataset.Position == population)

    return dataset[mask]


# Selectors -> charge text
@app.callback(
    [
        Output("mental_text", "children"),
        Output("rpe_text", "children"),
        Output("fcmoy_text", "children"),
        Output("fcmax_text", "children"),
    ],
    [
        Input("timeframe_selector", "value"),
        Input("population_selector", "value"),
    ],
)
def update_mentalfc_text(timeframe_selector, population_selector):
    timeframe = TIME_FRAME_VALUES[timeframe_selector]

    if population_selector == "ALL":
        population = None
    else:
        population = population_selector

    rpe_filtered = filter_dataset(rpe, timeframe, population)
    seances_filtered = filter_dataset(seances, timeframe, population)

    return round(rpe_filtered.RpeMenAp.mean(), 2), round(
        rpe_filtered.RpePhyAp.mean(), 2), round(
            seances_filtered.Fcmoy[seances_filtered.Fcmoy > 0].mean(),
            2), round(seances_filtered.Fcmax[seances_filtered.Fcmax > 0].mean(),
                      2)


# Selectors -> charge graph
@app.callback(
    Output("charge_graph", "figure"),
    [
        Input("timeframe_selector", "value"),
        Input("population_selector", "value")
    ],
)
def make_charge_figure(timeframe_selector, population_selector):

    layout_charge = copy.deepcopy(layout)

    timeframe = TIME_FRAME_VALUES[timeframe_selector]

    if not timeframe:
        timeframe = 31

    if population_selector == "ALL":
        population = None
    else:
        population = population_selector

    rpe_filtered = filter_dataset(rpe, timeframe, population)
    rpe_graph = rpe_filtered.groupby(["Date"]).mean()
    index = rpe_graph.index
    physical = rpe_graph.RpePhyAp
    mental = rpe_graph.RpeMenAp

    if index is None:
        annotation = dict(
            text="Pas de données disponibles",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_charge["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="RPE (Physique)",
                x=index,
                y=physical,
                line=dict(shape="spline", smoothing=2, width=1,
                          color="#5e35b1"),
                marker=dict(symbol="diamond-open"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Fatigue Mentale",
                x=index,
                y=mental,
                line=dict(shape="spline", smoothing=2, width=1,
                          color="#43a047"),
                marker=dict(symbol="diamond-open"),
            ),
        ]

        layout_charge[
            "title"] = "Charges Physiques et Mentales sur {} Jours".format(
                timeframe)
        layout_charge["margin"] = dict(l=40, r=0, t=40, b=40)
        layout_charge["xaxis"] = {"title": "Séance", "fixedrange": True}
        layout_charge["yaxis"] = {
            "title": "Fatigue entre 1 et 10",
            "fixedrange": True
        }

    figure = dict(data=data, layout=layout_charge)
    return figure


# Selectors -> dt graph
@app.callback(
    Output("dt_graph", "figure"),
    [
        Input("timeframe_selector", "value"),
        Input("population_selector", "value"),
        Input("dpzv_selector", "value"),
    ],
)
def make_dt_figure(timeframe_selector, population_selector, dpzv_selector):

    layout_dt = copy.deepcopy(layout)

    timeframe = TIME_FRAME_VALUES[timeframe_selector]

    if population_selector == "ALL":
        population = None
    else:
        population = population_selector

    seances_filtered = filter_dataset(seances, timeframe, population)
    seances_graph = seances_filtered.groupby(["Nom"]).sum()
    index = seances_graph.index
    y = seances_graph[dpzv_selector]

    if index is None:
        annotation = dict(
            text="Pas de données disponibles",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_dt["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="bar",
                name="Distance par Zones de Vitesse",
                x=index,
                y=y,
                marker=dict(color="#43a047"),
            ),
        ]

        if not timeframe:
            text_timeframe = "le Dernier Entraînement"
        else:
            text_timeframe = "{} Jours".format(timeframe)

        layout_dt["title"] = "Distances Parcourues ({}) sur {}".format(
            DPZV[dpzv_selector], text_timeframe)

        layout_dt["margin"] = dict(l=45, r=0, t=40, b=60)
        layout_dt["xaxis"] = {"title": "Joueuses", "fixedrange": True}
        layout_dt["yaxis"] = {"title": "Distance (m)", "fixedrange": True}

    figure = dict(data=data, layout=layout_dt)

    return figure


# Main graph -> fc graph
@app.callback(
    Output("fc_graph", "figure"),
    [
        Input("timeframe_selector", "value"),
        Input("population_selector", "value")
    ],
)
def make_fc_figure(timeframe_selector, population_selector):

    layout_fc = copy.deepcopy(layout)

    timeframe = TIME_FRAME_VALUES[timeframe_selector]

    if population_selector == "ALL":
        population = None
    else:
        population = population_selector

    seances_filtered = filter_dataset(seances, timeframe, population)
    seance_graph = seances_filtered[seances_filtered.Fcmax > 0].groupby(
        ["Nom"]).mean()
    x = seance_graph.RrBfMoy
    y = seance_graph.RrHfMoy
    text = seance_graph.index
    size = seance_graph.Fcmax

    if x is None:
        annotation = dict(
            text="Pas de données disponibles",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_fc["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="markers",
                name="Variabilité Cardiaque",
                x=x,
                y=y,
                text=text,
                marker={
                    "size": size,
                    "color": size,
                    "sizemode": "area",
                    "sizeref": 2. * max(size) / (40.**2),
                    "sizemin": 4
                },
            ),
        ]

        if not timeframe:
            text_timeframe = "le Dernier Entraînement"
        else:
            text_timeframe = "{} Jours".format(timeframe)

        layout_fc["title"] = "Variabilité Cardiaque sur {}".format(
            text_timeframe)
        layout_fc["margin"] = dict(l=40, r=0, t=40, b=40)
        layout_fc["xaxis"] = {
            "title": "Variabilité Cardiaque Basse Fréquence",
            "fixedrange": True
        }
        layout_fc["yaxis"] = {
            "title": "Variabilité Cardiaque Haute Fréquence",
            "fixedrange": True
        }

    figure = dict(data=data, layout=layout_fc)
    return figure


# Selectors, main graph -> sprint graph
@app.callback(
    Output("sprints_graph", "figure"),
    [
        Input("timeframe_selector", "value"),
        Input("population_selector", "value")
    ],
)
def make_sprint_figure(timeframe_selector, population_selector):

    layout_sprint = copy.deepcopy(layout)

    timeframe = TIME_FRAME_VALUES[timeframe_selector]

    if not timeframe:
        timeframe = 31

    if population_selector == "ALL":
        population = None
    else:
        population = population_selector

    seances_filtered = filter_dataset(seances, timeframe, population)
    seances_graph = seances_filtered.groupby(["Nom", "Date"
                                             ]).sum().groupby(["Date"]).mean()
    y = seances_graph.Sprints
    index = seances_graph.index

    if index is None:
        annotation = dict(
            text="Pas de données disponibles",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_sprint["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Sprints",
                x=index,
                y=y,
                line=dict(shape="spline", smoothing=2, width=1,
                          color="#43a047"),
                marker=dict(symbol="diamond-open"),
            ),
        ]

        if not timeframe:
            text_timeframe = "le Dernier Entraînement"
        else:
            text_timeframe = "{} Jours".format(timeframe)

        layout_sprint["title"] = "Sprints sur {}".format(text_timeframe)

        layout_sprint["margin"] = dict(l=40, r=0, t=40, b=60)
        layout_sprint["xaxis"] = {"title": "Jours", "fixedrange": True}
        layout_sprint["yaxis"] = {"title": "Sprints", "fixedrange": True}

    figure = dict(data=data, layout=layout_sprint)
    return figure


# Selectors, main graph -> pie graph
@app.callback(
    Output("pie_dt_graph", "figure"),
    [
        Input("timeframe_selector", "value"),
        Input("population_selector", "value")
    ],
)
def make_pie_figure(timeframe_selector, population_selector):

    layout_pie = copy.deepcopy(layout)

    timeframe = TIME_FRAME_VALUES[timeframe_selector]

    if population_selector == "ALL":
        population = None
    else:
        population = population_selector

    seances_filtered = filter_dataset(seances, timeframe, population)

    dpzv_values = [seances_filtered[dpzv].mean() for dpzv in DPZV.keys()]
    dpzv_text = [
        "Distance Passée dans l'Interval {}".format(dpzv)
        for dpzv in DPZV.values()
    ]

    data = [
        dict(
            type="pie",
            labels=list(DPZV.values()),
            values=dpzv_values,
            name="Distances par Zones de Vitesse",
            text=dpzv_text,
            hoverinfo="text+value",
            textinfo="label+name",
            hole=0.5,
            marker=dict(
                colors=["#43a047", "#00acc1", "#1e88e5", "#5e35b1", "#d81b60"]),
        ),
    ]
    layout_pie["title"] = "Distances par Zones de Vitesse"
    layout_pie["legend"] = dict(font=dict(color="#CCCCCC", size="10"),
                                orientation="h",
                                bgcolor="rgba(0,0,0,0)")

    figure = dict(data=data, layout=layout_pie)
    return figure


# Selectors, main -> table
@app.callback(
    Output("table", "data"),
    [Input("table", "page_current"),
     Input("table", "page_size")],
)
def make_table(page_current, page_size):
    table = seances[COLNAMES]
    table.columns = PRETTY_COLNAMES

    return table.iloc[page_current * page_size:(page_current + 1) *
                      page_size].to_dict("records")


# Selectors, main graph -> power graph
@app.callback(
    Output("power_graph", "figure"),
    [
        Input("timeframe_selector", "value"),
        Input("population_selector", "value")
    ],
)
def make_power_figure(timeframe_selector, population_selector):

    layout_power = copy.deepcopy(layout)

    timeframe = TIME_FRAME_VALUES[timeframe_selector]

    if not timeframe:
        timeframe = 7

    if population_selector == "ALL":
        population = None
    else:
        population = population_selector

    seances_filtered = filter_dataset(seances, timeframe, population)
    seances_graph = seances_filtered[seances_filtered.Power < 200].groupby(
        ["Nom", "Date"]).sum().groupby(["Date"]).mean()
    y = seances_graph.Power
    index = seances_graph.index

    if index is None:
        annotation = dict(
            text="Pas de données disponibles",
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_power["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Puissance",
                x=index,
                y=y,
                line=dict(shape="spline", smoothing=2, width=1,
                          color="#5e35b1"),
                marker=dict(symbol="diamond-open"),
            ),
        ]

        if not timeframe:
            text_timeframe = "le Dernier Entraînement"
        else:
            text_timeframe = "{} Jours".format(timeframe)

        layout_power["title"] = "Puissance Développée sur {}".format(
            text_timeframe)

        layout_power["margin"] = dict(l=40, r=0, t=40, b=60)
        layout_power["xaxis"] = {"title": "Jours", "fixedrange": True}
        layout_power["yaxis"] = {"title": "Puissance", "fixedrange": True}

    figure = dict(data=data, layout=layout_power)
    return figure


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
