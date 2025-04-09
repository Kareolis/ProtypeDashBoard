import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Загрузка данных
data = pd.read_csv("Data/units_timeline1.csv")

# Преобразуем время в datetime
data['time'] = pd.to_datetime(data['time'])

# Уникальные значения времени
unique_times = sorted(data['time'].unique())

# Создаем Dash-приложение
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='map-graph',
            config={
                'scrollZoom': True,  # Включение возможности масштабирования
                'displayModeBar': True,  # Включение панели инструментов
                'modeBarButtonsToAdd': ['zoomIn', 'zoomOut', 'resetScale']
                # Добавляем кнопки увеличения, уменьшения и сброса масштаба
            }
        ),
        dcc.Slider(
            id='time-slider',
            min=0,
            max=len(unique_times) - 1,
            value=0,
            marks={i: str(unique_times[i]) for i in range(len(unique_times))},
            step=None
        )
    ], style={'width': '70%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        html.H4("Детальная информация об объекте"),
        html.Div(id='details-info', style={'margin-bottom': '20px'}),
        dcc.Graph(id='details-graph')
    ], style={'width': '30%', 'display': 'inline-block'})
])


@app.callback(
    Output('map-graph', 'figure'),
    Input('time-slider', 'value')
)
def update_map(selected_time_index):
    # Фильтруем данные по выбранному времени
    selected_time = unique_times[selected_time_index]
    filtered_data = data[data['time'] == selected_time]

    # Создаем карту
    fig = px.scatter_mapbox(
        filtered_data,
        lat="latitude",
        lon="longitude",
        color="status",
        hover_name="callsign",
        size="fuel",
        mapbox_style="open-street-map",
        title=f"Объекты на карте (время: {selected_time})"
    )
    return fig


@app.callback(
    [Output('details-graph', 'figure'), Output('details-info', 'children')],
    Input('map-graph', 'clickData')
)
def update_details(clickData):
    if clickData is None:
        return px.bar(title="Выберите объект на карте"), "Выберите объект на карте, чтобы увидеть его подробности."

    # Получаем данные об объекте
    unit_id = clickData['points'][0]['hovertext']  # callsign передается в hover_name
    unit_data = data[data['callsign'] == unit_id]

    # Формируем текстовую информацию
    latest_data = unit_data.iloc[-1]  # Последняя запись для объекта
    details_text = html.Div([
        html.P(f"Позывной: {latest_data['callsign']}", style={'margin': '5px 0'}),
        html.P(f"Состояние: {latest_data['status']}", style={'margin': '5px 0'}),
        html.P(f"Топливо: {latest_data['fuel']}", style={'margin': '5px 0'}),
        html.P(f"Боеприпасы: {latest_data['ammo']}", style={'margin': '5px 0'}),
        html.P(f"Здоровье: {latest_data['health']}", style={'margin': '5px 0'}),
        html.P(f"Координаты: ({latest_data['latitude']}, {latest_data['longitude']})", style={'margin': '5px 0'})
    ])

    # Строим график
    fig = px.line(unit_data, x="time", y=["fuel", "ammo", "health"],
                  title=f"Динамика параметров для {unit_id}")
    return fig, details_text


if __name__ == '__main__':
    app.run_server(debug=True)
