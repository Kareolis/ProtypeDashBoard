import pandas as pd
import random
# Генерирует стартовые данные данные которые по умолчанию до сражения и тому подобное
# надо разделить на генерацию людей и техники
# добавить типов и тому подобное также надо
# добавить генератор статичных обьектов карты и нейтральных обьектов
# добавить генерацию в какомнибудь определенном секторе

# Функция для генерации случайных данных

def generate_unit_data(num_units=100):
    types = ['Танк', 'Гаубица', 'Пехота', 'БТР', 'Дрон']
    damages = ['Нет']
    tasks = ['Разведка', 'Оборона', 'Атака', 'Поддержка', 'Патрулирование']
    # statuses = ['Работает', 'Выведен из строя', 'Уничтожен', 'Погиб']
    statuses = ['Работает']
    visibility = ['Ясно', 'Преграда', 'Ночь', 'Туман']
    weather_conditions = ['Ясно', 'Дождь', 'Снег', 'Шторм', 'Облачно']
    division = ['гсадн','реактбатр', 'РС','РДР','РХБЗ','БМП','ДШБ','РР','ПТУР','ОР','РЭБ']
    data = []
    for i in range(1, num_units + 1):
        unit = {
            'id': f'unit_{i}',
            'division': random.choice(division),
            # 'callsign': f'Альфа-{random.randint(1, 99)}',
            'callsign': f'Альфа-{i}',
            'type': random.choice(types),
            'type_value':0,
            'serial_number': random.randint(1000, 9999),
            'status': random.choice(statuses),

            'task': random.choice(tasks),

            'time': random.randint(1, 100),
            'latitude': round(random.uniform(40.0, 50.0), 6),
            'longitude': round(random.uniform(20.0, 30.0), 6),

            'fuel': random.randint(0, 100),
            'ammo': random.randint(0, 100),
            'health': random.randint(0, 100),
            'damage': random.choice(damages),
            'ammo_load': random.randint(0, 100),

            'visibility': random.choice(visibility),
            'temperature': round(random.uniform(-20, 40), 1),
            'weather': random.choice(weather_conditions)
        }
        if unit['type_value'] == 'Танк':
            unit['type_value'] = 100
        else:
            unit['type_value'] = 10

        data.append(unit)



    return pd.DataFrame(data)


# Генерация данных
unit_data = generate_unit_data()

# for i in unit_data:
#     print(i)
    # i['type_value'] = 100
    # if unit['type'] == 'Танк':
    #     unit['type_value'] = 10
    #
    # if unit['type'] == 'Дрон':
    #     unit['type_value'] = 1

# Сохранение в CSV
output_path = 'Data/units_initial1.csv'
unit_data.to_csv(output_path, index=False)
output_path
