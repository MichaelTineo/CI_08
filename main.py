import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import requests
import json
import layout

# Definindo o app # dbc.themes.LUX / MINTY
app = Dash(__name__, external_stylesheets=[dbc.icons.BOOTSTRAP, dbc.themes.CERULEAN], suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id="url"),
    layout.nav_bar(),
    layout.content()
])


# Renderizando estrutura da página
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return layout.not_found_page(pathname)
    else:
        response = requests.get(
            f'https://synceurofarma.wdspace.com.br:8080/Commands/index?cmd=IC_VerifySession&SessionID={pathname[1:]}'
        )
        if response.text.find("UserID") == -1:
            return layout.not_found_page(pathname)
        response = pd.json_normalize(json.loads(response.text))
        userID = int(response["UserID"][0])
    return layout.main_page(userID)


@app.callback(
    Output('dropdown_team', 'options'),
    Output('dropdown_team', 'value'),
    Input("dropdown_user", "value")
)
def dropdown_team(userID):
    # A379DA49-5E46-4EAD-A512-012B53602000
    # pd.json_normalize(json.loads(response.text))
    response = requests.get(
        f'https://synceurofarma.wdspace.com.br:8080/Commands/index?cmd=IC_GetTeamList&UserID={userID}'
    )
    teamList = json.loads(response.text)
    teamValue = min(teamList, key=lambda d: d['value'])['value']
    return teamList, teamValue


@app.callback(
    Output('dropdown_calendar', 'options'),
    Output('dropdown_calendar', 'value'),
    Output('dropdown_especialidade', 'options'),
    Input("dropdown_team", "value")
)
def dropdown_team(teamID):
    response = requests.get(
        f'https://synceurofarma.wdspace.com.br:8080/Commands/index?cmd=IC_GetCalendarList&TeamID={teamID}'
    )
    calendarList = json.loads(response.text)
    calendarValue = max(calendarList, key=lambda d: d['value'])['value']

    response = requests.get(
        f'https://synceurofarma.wdspace.com.br:8080/Commands/index?cmd=IC_GetEspecialidadeList&TeamID={teamID}'
    )
    especialidadeList = json.loads(response.text)

    return calendarList, calendarValue, especialidadeList


@app.callback(
    Output('metasPorEspecialidade', 'children'),
    Input("dropdown_user", "value"),
    Input("dropdown_team", "value"),
    Input("dropdown_calendar", "value"),
    Input("dropdown_especialidade", "value")
)
def dropdown_team(userID, teamID, calendarID, especialidadeID):
    if especialidadeID is None:
        response = requests.get(
            f'https://synceurofarma.wdspace.com.br:8080/Commands/index?cmd=IC_SelectMedico&'
            f'UserID={userID}&TeamID={teamID}&CalendarID={calendarID}'
        )
    else:
        response = requests.get(
            f'https://synceurofarma.wdspace.com.br:8080/Commands/index?cmd=IC_SelectMedico&'
            f'UserID={userID}&TeamID={teamID}&CalendarID={calendarID}&EspecialidadeID={especialidadeID}'
        )
    df = pd.json_normalize(json.loads(response.text))

    return [
        dash_table.DataTable(
            df.to_dict('records'),
            [{"name": i, "id": i} for i in df.columns]
        )
    ]


if __name__ == '__main__':
    app.run_server(debug=False)
