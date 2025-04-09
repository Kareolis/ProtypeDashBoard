from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

# Создаем приложение Dash
app = Dash(__name__)

# Загрузка данных из CSV
units_timeline = pd.read_csv('E:/PCH/StartNaukaData/units_timeline.csv')
terrain_data = pd.read_csv('E:/PCH/StartNaukaData/terrain.csv')

# Определение минимального и максимального значений для таймлайна
min_timeline = int(units_timeline['timeline'].min())
max_timeline = int(units_timeline['timeline'].max())


# Функция для создания карты
def create_map(data):
    fig = go.Figure()

    # Наши объекты
    our_units = data[data['type'] == 'Our']
    fig.add_trace(go.Scattergeo(
        lat=our_units['latitude'], lon=our_units['longitude'],
        mode='markers+text',
        text=our_units['id'],
        textposition="top center",
        marker=dict(size=15, color='red'),
        name='Our Units'
    ))

    # Объекты противника
    enemy_units = data[data['type'] == 'Enemy']
    fig.add_trace(go.Scattergeo(
        lat=enemy_units['latitude'], lon=enemy_units['longitude'],
        mode='markers+text',
        text=enemy_units['id'],
        textposition="top center",
        marker=dict(size=15, color='blue'),
        name='Enemy Units'
    ))

    # Нейтральные объекты
    neutral_units = data[data['type'] == 'Neutral']
    fig.add_trace(go.Scattergeo(
        lat=neutral_units['latitude'], lon=neutral_units['longitude'],
        mode='markers',
        marker=dict(size=10, color='green'),
        name='Neutral Units'
    ))

    # Объекты местности
    terrain_groups = terrain_data.groupby('type')
    for terrain_type, group in terrain_groups:
        if terrain_type == 'River':
            fig.add_trace(go.Scattergeo(
                lat=group['latitude'], lon=group['longitude'],
                mode='lines',
                line=dict(color='cyan', width=3),
                name='River'
            ))
        elif terrain_type == 'Mountain':
            fig.add_trace(go.Scattergeo(
                lat=group['latitude'], lon=group['longitude'],
                mode='markers',
                marker=dict(color='brown', size=20, symbol='triangle-up'),
                name='Mountain'
            ))
        elif terrain_type == 'Trench':
            fig.add_trace(go.Scattergeo(
                lat=group['latitude'], lon=group['longitude'],
                mode='lines',
                line=dict(color='darkgray', width=3, dash='dash'),
                name='Trench'
            ))

    # Настройки карты
    fig.update_layout(
        title="Map",
        geo=dict(
            scope='world',
            projection_type='equirectangular',
            showland=False,
            landcolor="rgb(217, 217, 217)",
            subunitwidth=1,
            subunitcolor="rgb(255, 255, 255)"
        )
    )
    return fig


# Макет приложения
app.layout = html.Div([

    html.Div(children='''Концепт реализации проекта'''),

    html.Div([
        dcc.Graph(id='map', style={'height': '70vh'}),
    ], style={'width': '70%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='details', style={'height': '30vh'}),
    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),

    # Таймлайн
    dcc.Slider(
        id='time-slider',
        min=min_timeline,
        max=max_timeline,
        step=1,
        marks={i: f'T{i}' for i in range(min_timeline, max_timeline + 1)},
        value=min_timeline
    ),

])


# Колбэки для обновления
@app.callback(
    Output('map', 'figure'),
    Output('details', 'figure'),
    Input('map', 'clickData'),
    Input('time-slider', 'value')
)
def update_dashboard(click_data, time_value):
    # Фильтрация данных для текущего момента времени
    current_data = units_timeline[units_timeline['timeline'] == time_value]
    map_fig = create_map(current_data)

    # Если кликнули на объект
    if click_data:
        clicked_id = click_data['points'][0]['text']
        obj = current_data[current_data['id'] == clicked_id]
        if not obj.empty:
            details_fig = go.Figure()
            details_fig.add_trace(go.Bar(
                x=['Fuel', 'Ammo', 'Health'],
                y=[obj['fuel'].values[0], obj['ammo'].values[0], obj['health'].values[0]],
                marker=dict(color=['blue', 'orange', 'green'])
            ))
            details_fig.update_layout(
                title=f"Details for {clicked_id}",
                xaxis_title="Attribute",
                yaxis_title="Value",
                template="simple_white"
            )
            return map_fig, details_fig

    # Пустой график по умолчанию
    empty_fig = go.Figure().update_layout(template="plotly_dark")
    return map_fig, empty_fig


# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
