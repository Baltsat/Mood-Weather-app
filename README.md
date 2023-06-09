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

### Визуализация данных
**- display_mood_insights:**
Функция display_mood_insights использует Plotly для создания интерактивных визуализаций, которые дают представление о взаимосвязи между погодными факторами и настроением. Она включает в себя 3D диаграммы рассеяния с визуализацией гиперплоскости и 2D проекции точек данных на гиперплоскость. Вот пример реализации:
```
import plotly.graph_objects as go

def display_mood_insights():
    st.header("Mood Insights")
    calculate_mood_statistics()

    # Fetch weather data and mood labels
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file)
        weather_data = df[["Temperature", "Humidity", "Wind Speed"]]
        mood_labels = df["Mood"]

        # Perform LDA on weather data
        lda = perform_lda(weather_data, mood_labels)

        # Get the significance of weather factors
        factors = weather_data.columns
        significance = np.abs(lda.coef_[0])
        sorted_indices = np.argsort(significance)[::-1]  # Sort in descending order

        # Display the most significant weather factors
        st.subheader("Most Significant Weather Factors on Mood:")
        for i in sorted_indices:
            factor = factors[i]
            factor_significance = significance[i]
            st.write(f"{factor}: {factor_significance:.2f}")

        # Visualize the significance as a bar chart
        significance_data = pd.DataFrame(
            {"Factor": factors[sorted_indices], "Significance": significance[sorted_indices]})
        st.bar_chart(significance_data, x="Factor", y="Significance")

        # Map mood labels to numerical values
        encoded_labels = map_mood_labels(mood_labels)

        # Calculate plane coefficients
        plane_normal, plane_d = calculate_plane_coefficients(lda)
        st.subheader("Your data all in one.")
        
        # Create a 3D scatter plot with hyperplane visualization
        fig = go.Figure(data=[
            go.Scatter3d(
                x=weather_data["Temperature"],
                y=weather_data["Humidity"],
                z=weather_data["Wind Speed"],
                mode="markers",
                marker=dict(
                    size=5,
                    color=encoded_labels,
                    colorscale="Viridis",
                    opacity=0.8
                ),
                name="Weather Data",
                text=mood_labels,
                hovertemplate="%{text}"
            ),
            go.Mesh3d(
                x=[-30, 40, 40, -30],
                y=[20, 20, 100, 100],
                z=[(-plane_normal[0]*(-30) - plane_normal[1]*20 - plane_d) / plane_normal[2],
                (-plane_normal[0]*40 - plane_normal[1]*20 - plane_d) / plane_normal[2],
                (-plane_normal[0]*40 - plane_normal[1]*100 - plane_d) / plane_normal[2],
                (-plane_normal[0]*(-30) - plane_normal[1]*100 - plane_d) / plane_normal[2]],
                i=[0, 1, 2, 0],
                j=[1, 2, 3, 1],
                k=[3, 0, 1, 3],
                opacity=0.3,
                color="rgba(255, 0, 0, 0.3)",
                name="Dividing Hyperplane"
            )
        ])

        fig.update_layout(
            scene=dict(
                xaxis_title="Temperature",
                yaxis_title="Humidity",
                zaxis_title="Wind Speed"
            ),
            margin=dict(l=0, r=0, b=0, t=0)
        )

        st.plotly_chart(fig)

        # Funny insights based on the weather factors
        if factors[sorted_indices[0]] == "Temperature":
            if significance[sorted_indices[0]] > 0.5:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a hot and spicy person! 🔥🌶️</h3>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are as cool as a cucumber! 🥒❄️</h3>", unsafe_allow_html=True)
        elif factors[sorted_indices[0]] == "Humidity":
            if significance[sorted_indices[0]] > 0.5:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a humidifier! 💦😅</h3>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a desert dweller. 🏜️😎</h3>", unsafe_allow_html=True)
        elif factors[sorted_indices[0]] == "Wind Speed":
            if significance[sorted_indices[0]] > 0.5:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a tornado of energy! 🌪️⚡</h3>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are as calm as a gentle breeze! 🍃😌</h3>", unsafe_allow_html=True)

    else:
        st.write("No mood entries available.")
```

В функции display_mood_insights мы сначала рассчитываем LDA и извлекаем значимость погодных факторов. Мы отображаем наиболее значимые погодные факторы и визуализируем их значимость с помощью гистограммы. Затем мы сопоставляем метки настроения с числовыми значениями, вычисляем коэффициенты плоскости и создаем трехмерную диаграмму рассеяния с данными о погоде. Диаграмма рассеяния включает визуализацию гиперплоскости с помощью сетчатого графика. Наконец, мы предоставляем забавные сведения, основанные на наиболее значимом погодном факторе.

Включив функцию display_mood_insights в свое приложение Streamlit, пользователи смогут исследовать взаимосвязь между погодными факторами и настроением в интерактивном и визуально привлекательном виде.


### Создание приложения веб-интерфейса на Streamlit

Приложение Streamlit обычно имеет простую структуру. Давайте рассмотрим основные компоненты приложения Streamlit:

**Импорт зависимостей:**
Начните с импорта необходимых библиотек и модулей, включая Streamlit и другие библиотеки, используемые в вашем приложении, такие как Pandas, NumPy и Plotly.

**Инициализация приложения:**
Используйте модуль st, предоставляемый Streamlit, для инициализации приложения и установите заголовок для вашего приложения. Например, ```st.title('Weather Mood Tracker App').```

**Конфигурация боковой панели:**
Вы можете добавить боковую панель в ваше приложение с помощью модуля st.sidebar от Streamlit. Боковая панель полезна для включения опций, входов или настроек, с которыми пользователи могут взаимодействовать. Вы можете добавить такие виджеты, как слайдеры, выпадающие окна, флажки и т.д., для сбора информации от пользователей.
```
st.sidebar.title('Options')
city = st.sidebar.text_input('Enter City', 'London')
api_key = st.sidebar.text_input('Enter API Key', '')
```

**Основное содержание:**
Основное содержание вашего приложения - это место, где вы отображаете различные разделы и визуализации. Вы можете использовать различные модули Streamlit (st.header, st.subheader, st.write и т.д.) для добавления заголовков, текста и визуализаций.
```
st.header('Weather Mood Tracker')
st.write('Welcome to the Weather Mood Tracker App!')
```

**Ввод данных:**
Предоставьте пользователям возможность вводить данные о погоде или записи о настроении. Для этого можно использовать такие виджеты, как текстовые вводы, слайдеры или выпадающие элементы. Вы также можете включить кнопки для запуска действий, таких как добавление или удаление записей.
```
st.subheader('Add Weather Data')
temperature = st.number_input('Temperature', min_value=-100, max_value=100, value=0)
humidity = st.slider('Humidity', 0, 100, 50)
wind_speed = st.number_input('Wind Speed', min_value=0, max_value=100, value=0)
mood = st.selectbox('Mood', ['Happy', 'Sad', 'Neutral'])

if st.button('Add Entry'):
    add_entry(city, api_key, temperature, humidity, wind_speed, mood)

if st.button('Delete Last Entry'):
    delete_last_entry()
```
    
**Отображение данных:** 
Используйте модули Streamlit и библиотеки визуализации, такие как Plotly, для отображения данных о погоде, статистики настроения и других данных. Вы можете создавать графики, диаграммы и таблицы, чтобы представить информацию в интерактивном и визуально привлекательном виде.
```
st.header('Weather Data Visualization')
display_current_weather(city, api_key)

st.subheader('Previous Entries')
display_previous_entries()
```

**Дополнительно:**
Streamlit предоставляет несколько способов сбора отзывов пользователей и отображения уведомлений. Вы можете использовать такие виджеты, как кнопки, флажки или радиокнопки, чтобы позволить пользователям делать выбор. Streamlit также предлагает возможность отображения сообщений об успехе, ошибках или других уведомлений с помощью st.success, st.error и т.д.


**Запуск приложения:** 
Чтобы запустить приложение Streamlit, используйте команду streamlit run <filename>.py в терминале. Streamlit запустит локальный сервер разработки и откроет приложение в вашем веб-браузере по умолчанию.

**Развертывание приложения:**
Если вы хотите поделиться своим приложением с другими, вы можете развернуть его на различных платформах, таких как Streamlit Sharing, Heroku или других облачных платформах. Процесс развертывания будет зависеть от выбранной вами платформы.

### Заключение
В этой статье мы рассмотрели процесс создания приложения Weather Mood Tracker с помощью Streamlit. Мы начали с получения API-ключа с сайта weatherapi.com, что позволило нам получать данные о погоде в реальном времени для нашего приложения. Затем мы реализовали CRUD-методы для управления записями настроения, включая добавление новых записей и удаление последней записи.

Мы создали функциональность отображения нашего приложения, которая включала показ текущей погоды и отображение предыдущих записей настроения в табличном формате. Это предоставило пользователям удобный способ отслеживать и просматривать свое настроение с течением времени.

Далее мы углубились в анализ данных, где подсчитали статистику настроения и провели линейный дискриминантный анализ (LDA) для погодных факторов, чтобы выявить наиболее значимые факторы, влияющие на настроение. Мы визуализировали результаты с помощью гистограмм, чтобы показать значимость каждого погодного фактора.

Чтобы создать приложение Streamlit, мы организовали различные компоненты в структурированный макет. Мы использовали боковую панель для опций и настроек, а в разделе основного содержания разместили форму ввода данных о погоде, отображение текущей погоды, предыдущие записи, информацию о настроении и визуализации. Это позволило пользователям легко взаимодействовать с приложением и получать ценные сведения о взаимосвязи между погодой и настроением.

Мы использовали возможности Plotly для создания интерактивных 3D диаграмм рассеяния, визуализации гиперплоскостей и 2D проекций данных. Эти визуализации добавили дополнительный уровень понимания и вовлеченности, позволяя пользователям исследовать взаимосвязь между погодными факторами и настроением более захватывающим способом.

Streamlit предоставил интуитивно понятную и эффективную основу для создания нашего приложения с возможностью быстрой итерации и обновления приложения в режиме реального времени. Бесшовная интеграция компонентов анализа данных, визуализации и пользовательского интерфейса идеально подошла для нашего приложения Weather Mood Tracker.

В заключение, наше приложение Weather Mood Tracker демонстрирует потенциал Streamlit для создания интерактивных и глубоких приложений. Объединив данные о погоде, отслеживание настроения, анализ данных и визуализацию, мы разработали инструмент, позволяющий пользователям глубже понять, как погода влияет на их настроение. При дальнейшем совершенствовании и получении отзывов пользователей это приложение может стать ценным ресурсом для людей, стремящихся отслеживать и улучшать свое эмоциональное состояние в зависимости от погодных условий.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.
