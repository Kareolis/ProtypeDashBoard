import streamlit as st
import pandas as pd
import plotly.express as px

# Установим конфигурацию страницы для уменьшения белых полос
st.set_page_config(
    layout="wide"  # Используем широкий режим для страницы
)

# Загрузка данных
data = pd.read_csv("Data/units_timeline1.csv")

# Преобразуем время в datetime
data['time'] = pd.to_datetime(data['time'])

# Уникальные значения времени
unique_times = sorted(data['time'].unique())

# Заголовок приложения
st.title("Визуализация данных объектов")

# Разделение экрана на 2 колонки с другими пропорциями
col1, col2 = st.columns([2, 1])  # col1 для карты и таймлайна, col2 для остальной информации

# В колонке 1 - Таймлайн и Карта
with col1:
    # Слайдер для выбора времени
    selected_time = st.slider(
        "Выберите время:",
        min_value=0,
        max_value=len(unique_times) - 1,
        value=0,
        format="%d",
        step=1,
        key="time_slider"
    )

    # Фильтрация данных по времени
    current_time = unique_times[selected_time]
    filtered_data = data[data['time'] == current_time]

    color_discrete_map = {
        'Работает': 'blue',
        'Выведен из строя': 'green',
        'Уничтожен': 'red',
        'Погиб': 'black'

    }



    # Отображение карты
    st.subheader(f"Объекты на карте (время: {current_time})")
    fig_map = px.scatter_mapbox(
        filtered_data,
        lat="latitude",
        lon="longitude",
        color="status",
        color_discrete_map={
            'Работает': 'blue',
            'Выведен из строя': 'green',
            'Уничтожен': 'red',
            'Погиб': 'black'
        },
        hover_name="callsign",
        hover_data = "type",
        # size=200,
        size="type_value",
        mapbox_style="open-street-map",
        title="Карта объектов",
        width = 9000,
        height= 700
    )

    # Уменьшаем масштаб карты
    fig_map.update_layout(
        mapbox=dict(
            zoom=4  # Установите значение масштаба, меньшее значение означает меньший масштаб
        )
    )

    st.plotly_chart(fig_map)

# В колонке 2 - Информация о выбранном объекте и графики
with col2:
    # Выбор объекта
    selected_object = st.selectbox(
        "Выберите объект:",
        options=filtered_data["callsign"].unique(),
        key="object_selector",
        placeholder="Select contact method...",
        index=None
    )

    # Детальная информация об объекте
    if selected_object:
        unit_data = data[data['callsign'] == selected_object]
        latest_data = unit_data.iloc[-1]

        st.subheader("Последняя полученная информация об обекте")
        st.write(
            f"""
            - **Тип**: {latest_data['type']}

            - **Позывной**: {latest_data['callsign']}
            - **Состояние**: {latest_data['status']}
            - **Топливо**: {latest_data['fuel']}
            - **Боеприпасы**: {latest_data['ammo']}
            - **Здоровье**: {latest_data['health']}
            - **Повреждение**: {latest_data['damage']}
            - **Координаты**: ({latest_data['latitude']}, {latest_data['longitude']})
            """
        )
        # - ** Дивизион **: {latest_data['division']}

        # График динамики параметров
        st.subheader(f"Динамика параметров для {selected_object}")
        fig_details = px.line(
            unit_data,
            x="time",
            y=["fuel", "ammo", "health","temperature"],
            title=f"Динамика параметров для {selected_object}"
        )
        st.plotly_chart(fig_details)
