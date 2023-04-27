from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import json


def content():
    return html.Div(id="page-content", children=[])


def not_found_page(pathname):
    notFoundPage = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(
                    [
                        html.H1("404: Not found", className="text-danger"),
                        html.Hr(),
                        html.P(f"The path {pathname} was not recognised...")
                    ],
                    className="p-3 bg-light rounded-3",
                )
            ])
        ])
    ])

    return notFoundPage


def nav_bar():
    navbar = dbc.Navbar([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Img(src="/assets/nuxen-removebg-preview.png", height="50px")
                ]),
                dbc.Col([
                    dbc.NavbarBrand("Nuxen", className="ms-2")
                ],
                    align="center"
                )
            ],
                justify="start",
                className="g-0"
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Collapse(
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink(html.I(className="bi bi-linkedin"),
                                                    href="https://www.linkedin.com/company/nuxen-brasil/mycompany/",
                                                    external_link=True)),
                            dbc.NavItem(
                                dbc.NavLink(html.I(className="bi bi-instagram"), href="https://instagram.com/nuxenbr/",
                                            external_link=True)),
                            dbc.NavItem(
                                dbc.NavLink(html.I(className="bi bi-globe"), href="https://eurofarma.wdspace.com.br/",
                                            external_link=True))
                        ]),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True
                    )
                ])
            ],
                justify="end"
            )
        ],
            fluid=True
        )
    ],
        color="light",
        dark=False
    )

    return navbar


def main_page(userID):
    response = requests.get(
        f'https://synceurofarma.wdspace.com.br:8080/Commands/index?cmd=IC_UserLevels&UserID={userID}'
    )
    userList = json.loads(response.text)

    mainPage = dbc.Container([
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4('Setor:'),
                    dcc.Dropdown(
                        id='dropdown_user',
                        options=userList,
                        value=userID,
                        clearable=False
                    ),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H4('Equipe:'),
                    dcc.Dropdown(
                        id='dropdown_team',
                        clearable=False
                    ),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H4('Ciclo:'),
                    dcc.Dropdown(
                        id='dropdown_calendar',
                        clearable=False
                    ),
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H4('Especialidade:'),
                    dcc.Dropdown(
                        id='dropdown_especialidade'
                    ),
                ])
            )
        ]),
        html.Br(),
        dbc.Row([
            html.Div(id='metasPorEspecialidade')
        ])
    ],
        fluid=True
    )

    return mainPage
