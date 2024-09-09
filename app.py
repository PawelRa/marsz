import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Analiza półmaratonu wrocławskiego 2024")

df = pd.read_csv("halfmarathon_wroclaw_2024__final.csv", sep=";")

#Liczba zawodników
c0, c1, c2 = st.columns(3)
with c0:
    st.metric("Liczba zawodników", len(df))

#Liczba mężczyzn
with c1:
    st.metric("Liczba mężczyzn", len(df[df["Płeć"]=="M"]))

#Liczba kobiet
with c2:
    st.metric("Liczba kobiet", len(df[df["Płeć"]=="K"]))

#10 losowych wierszy
#st. write("## 10 losowych wierszy")
st.header("10 losowych wierszy")
st.dataframe(
    df.sample(10),
    use_container_width=True,
    hide_index=True
)

#TOP 5 zawodników
st.header("TOP 5 zawodników")
top_columns = ["Miejsce", "Numer startowy", "Nazwisko", "Miasto", "Kraj", "Czas"]
st.dataframe(
    df.sort_values("Miejsce")[top_columns].head(5),
    hide_index=True,
    use_container_width=True,
)

# Barplot krajów
st.header("Pochodzenie zawodników")
gdf = df.groupby("Kraj", as_index=False).count().rename(columns={"Miejsce": "Liczba zawodników"})
st.bar_chart(gdf, x="Kraj", y="Liczba zawodników")

# Histogram czasu na mecie
st.header("Histogram czasu na mecie")
df["Czas"] = pd.to_datetime(df["Czas"], format='%H:%M:%S', errors="coerce").dt.time

# Tworzenie histogramu przy użyciu seaborn
plt.figure(figsize=(10,6))
plot = sns.histplot(df["Czas"].apply(lambda x: x.hour * 60 + x.minute + x.second / 60), kde=True)

st.pyplot(plot.figure)

# Macierz korelacji
st.header("Macierz korelacji")
correlation_matrix = df.corr(numeric_only=True)
plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
st.pyplot(plt.gcf())