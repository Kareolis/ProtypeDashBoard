import streamlit as st
import pandas as pd
import plotly.express as px

# Загрузка данных
data = pd.read_csv("Data/units_timeline1.csv")

# Преобразуем время в datetime
data['time'] = pd.to_datetime(data['time'])

# Уникальные значения времени
unique_times = sorted(data['time'].unique())

# Заголовок приложения
st.title("Визуализация данных объектов")

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

# Отображение карты
st.subheader(f"Объекты на карте (время: {current_time})")
fig_map = px.scatter_mapbox(
    filtered_data,
    lat="latitude",
    lon="longitude",
    color="status",
    hover_name="callsign",
    size="fuel",
    mapbox_style="open-street-map",
    title="Карта объектов"
)
# Уменьшаем масштаб карты
fig_map.update_layout(
    mapbox=dict(
        zoom=4  # Установите значение масштаба, меньшее значение означает меньший масштаб
    )
)

st.plotly_chart(fig_map)


# Выбор объекта
selected_object = st.selectbox(
    "Выберите объект:",
    options=filtered_data["callsign"].unique(),
    key="object_selector"
)

# Детальная информация об объекте
if selected_object:
    unit_data = data[data['callsign'] == selected_object]
    latest_data = unit_data.iloc[-1]

    st.subheader("Детальная информация об объекте")
    st.write(
        f"""
        - **Позывной**: {latest_data['callsign']}
        - **Состояние**: {latest_data['status']}
        - **Топливо**: {latest_data['fuel']}
        - **Боеприпасы**: {latest_data['ammo']}
        - **Здоровье**: {latest_data['health']}
        - **Координаты**: ({latest_data['latitude']}, {latest_data['longitude']})
        """
    )

    # График динамики параметров
    st.subheader(f"Динамика параметров для {selected_object}")
    fig_details = px.line(
        unit_data,
        x="time",
        y=["fuel", "ammo", "health"],
        title=f"Динамика параметров для {selected_object}"
    )
    st.plotly_chart(fig_details)
