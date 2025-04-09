import pandas as pd
import random
from datetime import datetime, timedelta

# Параметры генерации
TIME_STEP_MINUTES = 30  # Шаг времени в минутах (можно изменить на 30 или любой другой)
NUM_CHANGES = 100  # Количество изменений

# Пути к файлам
INPUT_FILE = "Data/units_initial1.csv"  # Входной файл с начальными данными
OUTPUT_FILE = "Data/units_timeline1.csv"  # Выходной файл с изменениями

# Загрузка исходных данных
data = pd.read_csv(INPUT_FILE)

# Преобразование времени в datetime для удобства
initial_time = datetime.strptime("2025-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")  # Стартовое время

# Функция для генерации изменений одного объекта
def generate_changes(unit, current_time):
    # Логичные изменения для типа объекта
    if unit['type'] in ['Танк', 'БТР', 'Гаубица']:
        max_distance = 0.01  # Танки, БТР и гаубицы перемещаются медленно
        fuel_consumption = 10  # Расход топлива
    elif unit['type'] in ['Дрон']:
        max_distance = 0.05  # Дроны могут перемещаться быстрее
        fuel_consumption = 2  # Дроны потребляют больше топлива
    elif unit['type'] in ['Пехота']:
        max_distance = 0.005  # Пехота перемещается медленно
        fuel_consumption = 0.2  # Пехота потребляет мало ресурса (еда)
    else:
        max_distance = 0.01
        fuel_consumption = 1

    # Обновление координат
    unit['latitude'] += random.uniform(-max_distance, max_distance)
    unit['longitude'] += random.uniform(-max_distance, max_distance)

    # Обновление топлива и боекомплекта
    unit['fuel'] = max(0, unit['fuel'] - fuel_consumption)
    # unit['fuel'] -= 10

    unit['ammo'] = max(0, unit['ammo'] - random.uniform(0, 3))

    # Обновление здоровья (возможное повреждение)
    if random.random() < 0.1:  # 10% вероятность повреждения
        unit['health'] = max(0, unit['health'] - random.uniform(5, 20))
        unit['damage'] = random.choice([
            "Ранение ноги", "Ранение головы", "Пробоина", "Прямое попадание", "Нет"
        ])

    # Изменение статуса с вероятностью
    if unit['health'] <= 0:
        unit['status'] = "Погиб"
    elif unit['fuel'] <= 0 and unit['status'] == "Работает":
        unit['status'] = "Выведен из строя"

    # Добавление видимости, температуры и погодных условий
    unit['visibility'] = random.choice(["Туман", "Ночь", "Преграда", "Ясно"])
    unit['temperature'] = round(random.uniform(-20, 40), 1)  # Температура в пределах -20 до 40
    unit['weather'] = random.choice(["Шторм", "Снег", "Дождь", "Облачно", "Ясно"])

    # Увеличение времени
    unit['time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return unit

# Генерация изменений
output_data = []
current_time = initial_time
for _ in range(NUM_CHANGES):
    for _, unit in data.iterrows():
        unit_copy = unit.copy()  # Создаём копию объекта
        updated_unit = generate_changes(unit_copy, current_time)
        output_data.append(updated_unit)
    current_time += timedelta(minutes=TIME_STEP_MINUTES)

# Создание DataFrame для вывода
output_df = pd.DataFrame(output_data)

# Сохранение в CSV
output_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

print(f"Генерация завершена! Изменения сохранены в файл {OUTPUT_FILE}")
