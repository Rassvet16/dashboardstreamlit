import pandas as pd
import streamlit as st
import io
import matplotlib.pyplot as plt
st.title("Интерактивный дашборд по проверке оружия")
st.sidebar.header("Выберите параметры")


uploaded_file = st.sidebar.file_uploader("Загрузите файл CSV", type="csv")
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.warning("Загрузите файл CSV")

if 'df' in locals():
    selected_state = st.sidebar.selectbox("Выберите штат", df['state'].unique())

    unique_months = df['month'].apply(lambda x: x[-2:]).drop_duplicates().tolist()

    years = [int(month.split('-')[0]) for month in df['month']]
    selected_year = st.sidebar.selectbox("Выберите год",  options=range(min(years), max(years)+1), index=0)

    # Фильтрация данных
    filtered_data = df[(df['state'] == selected_state) &
                       (pd.to_datetime(df['month']).dt.year == selected_year)]

    # Вывод результатов анализа
    st.subheader("Результаты анализа")
    st.write("Выбранные параметры:")
    st.write("- Штат:", selected_state)

    st.write("- Год:", selected_year)
    st.write("Общее количество проверенного оружия за {}:".format(selected_year),
             filtered_data['totals'].sum())

    filtered_data  = df[pd.to_datetime(df['month']).dt.year == selected_year]

    st.subheader("Распределение проверенного оружия по штатам за {}".format(selected_year))
    top_states = filtered_data.groupby('state')['totals'].sum().nlargest(10)


    fig, ax = plt.subplots(figsize=(10, 8))
    top_states.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

    if st.download_button("Экспортировать результаты в CSV", data=filtered_data.to_csv(index=False), file_name="filter.csv", mime="text/csv"):
        st.success("Успешно!")
