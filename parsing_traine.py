import requests
from bs4 import BeautifulSoup
from pprint import pprint

weather_with_real_param_list = []
resourse = requests.get('https://sinoptik.ua/')
city = "Кременчуг"
# city сделать инпутом
hours = []
weather = ['temp', 'preasure', 'humidity', 'weather', 'wind']
parameters_of_weather = []

url_for_city = requests.get('https://sinoptik.ua/погода-{}/10-дней'.format(city)).text
soup = BeautifulSoup(url_for_city, 'lxml')

# перебираем всю информацию по часам
for classes in range(8):
    search_right_teg = soup.find('div', class_='rSide').find_all('td', class_='p{}'.format(classes + 1))

# Добавляем в список температуру, давление и влажность, в список hourse добавляем часы
    for index, tegs in enumerate(search_right_teg):
        if index in (2, 4, 5):
            parameters_of_weather.append(tegs.text)
        elif index == 0:
            hours.append(tegs.text)
        else:
            continue
# Добавляем в список ветер и облачность
    parameters_of_weather.append(soup.find('div', class_='weatherIco n400')['title'])
    parameters_of_weather.append(soup.find('div', class_="Tooltip wind wind-SE")['data-tooltip'])

# Соединяем список погоды с ее параметрами в словарь и добавляем его в список
    weather_with_real_param = dict(zip(weather, parameters_of_weather))
    weather_with_real_param_list.append((weather_with_real_param))
    parameters_of_weather.clear()

# Соединяем список часов с полным списком параметров
weather_per_hours = dict(zip(hours, weather_with_real_param_list))

pprint(weather_per_hours)


