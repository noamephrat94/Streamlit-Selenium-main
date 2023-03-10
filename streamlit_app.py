import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import streamlit.components.v1 as components
import pandas as pd
import countries
import os
import time
import datetime
from bs4 import BeautifulSoup
import countries


@st.cache_resource
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
# options.add_argument('--headless')

# url = 'http://www.google.com'
# driver = get_driver()
# driver.get(url)
#
# components.iframe(url)
# st.code(driver.page_source)
def create_df():
    columns = ['url', 'title', 'paragraph', 'age']
    df = pd.DataFrame(columns=columns)
    return df


def get_news(driver, search_term):
    # Query to obtain links
    search_term = search_term.replace(" ", "%20")
    df = create_df()
    n_pages = 2
    for countrie in countries.countries:
        time.sleep(5)
        for page in range(1, n_pages):
            st.title(countrie)
            # url = "http://www.google.com/search?q=" + search_term +"&start=" + str((page - 1) * 10)
            url = f'https://www.bing.com/news/search?q={search_term}%20{countrie}&qft=sortbydate%3d%221%22&FORM=HDRSC7'
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # soup = BeautifulSoup(r.text, 'html.parser')
            # st.code(soup)
            search = soup.findAll('div', class_="news-card-body card-with-cluster")
            search = search[0:5]
            # st.code(soup)
            for d in search:
                col1, col2 = st.columns([1, 3])
                # st.code(d)
                with col1:
                    try:
                        img = d.find('div', 'image right').find('a').find('img')['src']
                        st.image(img)
                    except Exception as e:
                        st.write('No Image')
                with col2:
                    url = d.find('a', class_='title')['href']
                    title = d.find('a', class_='title').text
                    paragraph = d.find('div', class_='snippet').text
                    try:
                        age = d.find('div', class_='source set_top').findAll("span")[-1].text
                    except Exception as e:
                        age = None
                    st.subheader(title)
                    st.markdown(paragraph)
                    if age:
                        st.text(age)
                    link = f'[Read Article]({url})'
                    st.markdown(link, unsafe_allow_html=True)
                st.markdown("""---""")
        st.markdown("""---""")
    return df
def create_ds(data, search_term):
    df = pd.DataFrame(data)
    df.to_csv(f'output/google_shops_{search_term}.csv')

def main():
    search_term = st.text_input("Enter search term")
    run = st.button(label="Search News")
    if run:
        driver = get_driver()
        data = get_news(driver, search_term)
        st.dataframe(data)


if __name__ == "__main__":
    main()