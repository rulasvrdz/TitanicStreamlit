import pandas as pd
import streamlit as st
import plotly.express as px

st.title("EDA Titanic")
st.markdown("**Datos**")


@st.cache
def get_data():
    URL = 'https://storage.googleapis.com/kagglesdsdata/competitions/3136/26502/train.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1633692991&Signature=CUsoKupWKy2Pe0xZ53XkeQ2BIwQxbrFhTHIxBC95vX%2FFSmG7VqLLZvKAm1M%2BjwFXohTVgFHwq5ETDgiyxjWRbtg88UsTCuCCRJZl%2F51WzumXe3pQNPzqTPpO6%2BKeIpMjaK6Eu%2FibeBTXJZ6Ekk45GZ7SfQRo5jjslmF6Pl6emJqZeWcjDytWUuOOiWSf3sYdmNC2M43vxcydZBXhUdWXly50PPxTz7xRiqZMQuUU7ZpWOOiAMFQM%2BnkBJOxcsVnvL81kmUc0BPibJiJB%2BtaAXclxGl%2FGoNYMW1A3rvBtCmt7yfCXCrJ1%2BLEF5tbJPNcNheAOiLl5g878k2TTjlon7w%3D%3D&response-content-disposition=attachment%3B+filename%3Dtrain.csv'
    return pd.read_csv(URL)

df = get_data()
st.dataframe(df.head(25))

st.subheader("Select a column to see")
default_cols = ["Name", "Survived", "Pclass"]
cols = st.multiselect("Columns", df.columns.tolist(), default=default_cols)
st.dataframe(df[cols].head(50))

st.subheader("Age analisis for ticket class")
st.text("Select a an option")
Pclass = st.radio("Ticket class", df.Pclass.unique())
classMask = df['Pclass']==Pclass
ClassDf = df[classMask]
@st.cache
def get_availability(Pclass):
    return df.query(""" Pclass==@Pclass""").Age.describe(\
        percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

st.table(get_availability(Pclass))

st.subheader("Age analisis for sex")
st.text("Select a an option")
Sex = st.radio("Sex", df.Sex.unique())
sexMask = df['Sex']==Sex
sexDf = df[sexMask]
@st.cache
def get_availability(Sex):
    return df.query(""" Sex==@Sex""").Age.describe(\
        percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

st.table(get_availability(Sex))

st.subheader("Ticket Fare")
st.write("Select a range for pricing within the sidebar")
values = st.sidebar.slider("Price range", float(df.Fare.min()), float(df.Fare.clip(upper=250.).max()), (0., 250.))
hist = px.histogram(df.query(f"Fare.between{values}"), x="Fare", nbins=10, title="Price Distribution")
hist.update_xaxes(title="price")
hist.update_yaxes(title="# of Apartments/rooms/hotels")
st.plotly_chart(hist)

st.subheader("Age distribution")
st.write("Select a range for age within the sidebar")
valuesA = st.sidebar.slider("Age range", float(df.Age.clip(lower=0.).min()), float(df.Age.max()), (0., 80.))
hist = px.histogram(df.query(f"Age.between{valuesA}"), x="Age", nbins=20, title="Age Distribution")
hist.update_xaxes(title="Age")
hist.update_yaxes(title="Passengers")
st.plotly_chart(hist)
