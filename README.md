# Mood-Weather-app
Mood Weather app streamlit, weatherapi API.

* Run with

``` 
pip install -r requirements.txt 
streamlit run src/app.py 
```


![screencast](https://github.com/Baltsat/Mood-Weather-app/assets/42536677/67d570f9-5da2-4fb8-a3f7-af7139cf73ac)







## Создание приложения для отслеживания настроения и погоды с помощью Streamlit: Пошаговое руководство
### Введение:
В этом руководстве мы рассмотрим процесс создания приложения для отслеживания погодного настроения с помощью Streamlit, мощной библиотеки Python для создания интерактивных веб-приложений. Наше приложение будет анализировать погодные данные и их влияние на настроение, предоставляя ценные сведения и визуализации. К концу этой статьи у вас будет функциональное приложение, которое поможет вам понять, как погода влияет на ваше настроение. Итак, давайте начнем!
```
python -m venv weather-mood-tracker-env
```
Активируйте виртуальную среду:

* Для Windows:
```weather-mood-tracker-env\Scripts\activate```
* Для macOS/Linux:
```source weather-mood-tracker-env/bin/activate```

Затем установите необходимые библиотеки, выполнив следующую команду:
```pip install streamlit pandas scikit-learn plotly```
Или с помощью файла требований:
``` pip install -r /path/to/requirements.txt```

### Сбор и подготовка данных о погоде
Чтобы проанализировать влияние погоды на настроение, нам нужны данные о погоде. Существует несколько вариантов получения данных о погоде, включая погодные API или общедоступные наборы данных. Выберите вариант, который лучше всего соответствует вашим потребностям, и соберите необходимые данные о погоде. Убедитесь, что данные включают температуру, влажность, скорость ветра и другие необходимые погодные характеристики.

**Шаг 1: Получение ключа API от weatherapi**
Чтобы получить данные о погоде для нашего приложения, нам необходимо зарегистрировать API-ключ от weatherapi. API-ключ предоставит нам доступ к их службе данных о погоде. Получив API-ключ, вы можете надежно сохранить его в качестве переменной окружения в своей среде разработки либо импортировать из другого файла, как это сделано в текущей реализации.

**Шаг 2: Получение данных о погоде**
После получения ключа API мы можем получить данные о погоде с помощью функции fetch_weather_data. Эта функция делает запрос к weatherapi и извлекает информацию о погоде на основе определенного местоположения и даты. Простпейший способ сделать это:
```
import requests

def fetch_weather_data(location, date):
    url = f"https://api.weatherapi.com/v1/history.json?key={API_KEY}&q={location}&dt={date}"
    response = requests.get(url)
    data = response.json()
    return data
```


### Сбор данных о настроении. Методы CRUD для записей
Для управления записями настроения в нашем приложении Weather Mood Tracker мы реализуем методы CRUD (Create, Read, Update, Delete). Эти методы позволяют пользователям добавлять новые записи настроения и удалять последнюю запись.
**Добавление записи настроения**
Функция add_entry добавляет новую запись настроения к данным о погоде. В качестве входных данных она принимает значение настроения и данные о погоде.
```def add_entry(mood, weather_data):
    entry = {
        "Mood": mood,
        "Temperature": weather_data["Temperature"],
        "Humidity": weather_data["Humidity"],
        "Wind Speed": weather_data["Wind Speed"]
    }
    weather_data["Mood Entries"].append(entry)
```
В этой функции мы создаем словарь, представляющий запись настроения, и заполняем его значением настроения и данными о погоде. Затем мы добавляем эту запись в список записей настроения в данных о погоде.

**Удаление последних записей**
Функция delete_last_entry удаляет последнюю запись о настроении из данных о погоде.
```def delete_last_entry(weather_data):
    if weather_data["Mood Entries"]:
        weather_data["Mood Entries"].pop()
```
Эта функция проверяет, есть ли в данных о погоде записи о настроении. Если таковые имеются, она удаляет последнюю запись из списка, используя метод pop.

### Отображение текущей погоды и предыдущих записей
Чтобы предоставить пользователям обзор текущей погоды и историю их записей о настроении, мы реализуем функции для отображения этой информации.
**Отображение текущей погоды**
Функция display_current_weather извлекает информацию о текущей погоде с помощью функции fetch_weather_data и отображает ее пользователю.
```
def display_current_weather(location):
    weather_data = fetch_weather_data(location, date.today())
    st.subheader("Current Weather")
    st.write(f"Location: {location}")
    st.write(f"Temperature: {weather_data['Temperature']}°C")
    st.write(f"Humidity: {weather_data['Humidity']}%")
    st.write(f"Wind Speed: {weather_data['Wind Speed']} km/h")
```
В этой функции мы получаем данные о погоде на текущую дату с помощью функции fetch_weather_data. Затем мы используем функции Streamlit's subheader и write для отображения пользователю местоположения, температуры, влажности и скорости ветра.

**Отображение предыдущих записей**
Функция display_previous_entries представляет пользователю историю записей настроения.
```
def display_previous_entries(weather_data):
    mood_entries = weather_data["Mood Entries"]
    if mood_entries:
        st.subheader("Previous Mood Entries")
        for entry in mood_entries:
            st.write(f"Mood: {entry['Mood']}")
            st.write(f"Temperature: {entry['Temperature']}°C")
            st.write(f"Humidity: {entry['Humidity']}%")
            st.write(f"Wind Speed: {entry['Wind Speed']} km/h")
            st.write("---")
    else:
        st.write("No previous mood entries.")
```
В этой функции мы проверяем, есть ли в данных о погоде записи о настроении. Если таковые имеются, мы перебираем каждую запись и отображаем настроение, температуру, влажность и скорость ветра для пользователя с помощью функции записи Streamlit. Если записей не найдено, мы выводим сообщение об отсутствии предыдущих записей о настроении.


### Эксплораторный анализ данных (EDA)
**- calculate_mood_statistics:**
Функция calculate_mood_statistics рассчитывает различные статистические данные, связанные с настроением, на основе данных о погоде. Она вычисляет среднее настроение, наиболее частое настроение и распределение настроения. Вот пример реализации:
```
def calculate_mood_statistics(weather_data):
    average_mood = weather_data["Mood"].mean()
    most_frequent_mood = weather_data["Mood"].mode()[0]
    mood_distribution = weather_data["Mood"].value_counts(normalize=True)
    return average_mood, most_frequent_mood, mood_distribution
```

**- perform_lda:**
Функция perform_lda применяет линейный дискриминантный анализ (LDA) к данным о погоде и меткам настроения. Это помогает определить значимые погодные факторы, влияющие на настроение. Вот пример реализации:
```
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def perform_lda(weather_data, mood_labels):
    lda = LinearDiscriminantAnalysis()
    lda.fit(weather_data, mood_labels)
    return lda
```

**- map_mood_labels:**
Функция map_mood_labels отображает метки настроения в числовые значения для дальнейшего анализа и визуализации. Она присваивает уникальное числовое значение каждой категории настроения. Вот пример реализации:
```
def map_mood_labels(mood_labels):
    unique_labels = mood_labels.unique()
    mapping = {label: i for i, label in enumerate(unique_labels)}
    encoded_labels = mood_labels.map(mapping)
    return encoded_labels
```

**- calculate_plane_coefficients:**
Функция calculate_plane_coefficients определяет коэффициенты уравнения гиперплоскости на основе анализа LDA. Она извлекает нормальный вектор и постоянный член (d) уравнения плоскости. Вот пример реализации:
```
def calculate_plane_coefficients(lda):
    plane_normal = lda.coef_[0]
    plane_d = lda.intercept_[0]
    return plane_normal, plane_d
```

### Visualizing the Data

### Building the Weather Mood Tracker App

### Deploying the App

### Conclusion

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.
