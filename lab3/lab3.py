import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Завантаження даних
@st.cache_data
def load_data():
    return pd.read_csv("combined_data.csv")

df = load_data()

# Словник регіонів
region_dict = {
    "1": "Вінничина", "2": "Волинь", "3": "Дніпропетровщина", "4": "Донеччина", "5": "Житомирщина",
    "6": "Закарпаття", "7": "Запоріжжя", "8": "Івано-Франківщина", "9": "Київщина", "10": "Кіровоградщина",
    "11": "Луганщина", "12": "Львівщина", "13": "Миколаївщина", "14": "Одещина", "15": "Полтавщина",
    "16": "Рівненщина", "17": "Сумщина", "18": "Тернопільщина", "19": "Харківщина", "20": "Херсонщина",
    "21": "Хмельницька", "22": "Черкащина", "23": "Чернівецька", "24": "Чернігівщина", "25": "Крим",
    "26": "Київ", "27": "Севастополь"
}

# Ініціалізація стану сесії для фільтрів
if 'ticker' not in st.session_state:
    st.session_state.ticker = "VCI"
if 'region' not in st.session_state:
    st.session_state.region = "1"
if 'week_range' not in st.session_state:
    st.session_state.week_range = (1, 54)
if 'year_range' not in st.session_state:
    st.session_state.year_range = (1981, 2023)
if 'sort_asc' not in st.session_state:
    st.session_state.sort_asc = False
if 'sort_desc' not in st.session_state:
    st.session_state.sort_desc = False

# Функція для скидання фільтрів
def reset_filters():
    st.session_state.ticker = "VCI"
    st.session_state.region = "1"
    st.session_state.week_range = (1, 54)
    st.session_state.year_range = (1981, 2023)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

# Бічна панель (колонка для інтерактивних елементів)
with st.sidebar:
    st.header("Фільтри")

    # Вибір показника (VCI, TCI, VHI)
    ticker = st.selectbox("Оберіть показник:", ["VCI", "TCI", "VHI"], key="ticker")

    # Вибір області
    region = st.selectbox("Оберіть область:", options=region_dict.keys(), format_func=lambda x: region_dict[x], key="region")

    # Вибір тижня
    week_range = st.slider("Оберіть інтервал тижнів:", min_value=1, max_value=54, value=st.session_state.week_range, key="week_slider")

    # Вибір року
    year_range = st.slider("Оберіть діапазон років:", min_value=1981, max_value=2023, value=st.session_state.year_range, key="year_slider")

    # Чекбокси для сортування
    sort_asc = st.checkbox("Сортувати за зростанням", key="sort_asc")
    sort_desc = st.checkbox("Сортувати за спаданням", key="sort_desc")

    # Оновлення значень слайдерів у st.session_state
    st.session_state.week_range = week_range
    st.session_state.year_range = year_range

    # Кнопка скидання фільтрів
    if st.button("Скинути фільтри", on_click=reset_filters):
        # Оновлення стану компонентів, щоб відобразити зміни
        st.rerun()

# Основна область (колонка для графіка та таблиці)
st.header("Результати")

# Фільтрація даних
week_start, week_end = st.session_state.week_range
year_start, year_end = st.session_state.year_range

filtered_df = df[
    (df["area"] == int(st.session_state.region)) &
    (df["Week"].between(week_start, week_end)) &
    (df["Year"].between(year_start, year_end))
]

# Сортування даних
if st.session_state.sort_asc and not st.session_state.sort_desc:
    filtered_df = filtered_df.sort_values(by=st.session_state.ticker, ascending=True)
elif not st.session_state.sort_asc and st.session_state.sort_desc:
    filtered_df = filtered_df.sort_values(by=st.session_state.ticker, ascending=False)
elif st.session_state.sort_asc and st.session_state.sort_desc:
    st.warning("Виберіть лише один тип сортування.")

# Вкладки
tab1, tab2 = st.tabs([" Таблиця", " Графік"])

# Таблиця
with tab1:
    st.subheader("Таблиця відфільтрованих даних")
    st.dataframe(filtered_df[['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']])

# Графік
with tab2:
    if not filtered_df.empty:
        st.subheader(f"Графік для {region_dict[st.session_state.region]} ({year_start}-{year_end} рік, {week_start}-{week_end} тижнів)")

        fig, ax = plt.subplots(figsize=(15, 10))

        # Побудова графіка на основі тижнів, але з урахуванням сортування
        for year in range(year_start, year_end + 1):
            year_data = filtered_df[filtered_df["Year"] == year]
            ax.plot(year_data["Week"], year_data[st.session_state.ticker], label=f"{year}")

        ax.set_xlabel("Тижні")
        ax.set_ylabel(st.session_state.ticker)
        ax.set_title(f"{st.session_state.ticker} для {region_dict[st.session_state.region]} ({year_start}-{year_end} рік)")
        ax.legend(title="Роки", bbox_to_anchor=(1.05, 1), loc='upper left')

        st.pyplot(fig)
    else:
        st.warning("Немає даних для вибраних параметрів.")