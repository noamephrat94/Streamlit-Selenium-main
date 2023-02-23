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
    df = create_df()
    query = 'comprehensive guide to web scraping in python'
    links = []  # Initiate empty list to capture final results
    # Specify number of pages on google search, each page contains 10 #links
    n_pages = 2
    for page in range(1, n_pages):
        # url = "http://www.google.com/search?q=" + search_term +"&start=" + str((page - 1) * 10)
        url = f'https://www.bing.com/news/search?q={search_term}&FORM=HDRSC7'
        st.write(url)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # soup = BeautifulSoup(r.text, 'html.parser')

        search = soup.findAll('div', class_="news-card-body card-with-cluster")
        # st.code(soup)
        for d in search:
            # img = d.find('div', 'image right').find('a')['href']
            # st.image(img)
            url = d.find('a', class_='title')['href']
            title = d.find('a', class_='title')['href'].text
            paragraph = d.find('div', class_='snippet').text
            age = d.find('div', class_='source set_top').findAll("span")[-1].text
            st.write([url, title, paragraph, age])
    return df
def create_ds(data, search_term):
    df = pd.DataFrame(data)
    df.to_csv(f'output/google_shops_{search_term}.csv')

def main():
    import os
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    st.write(files)
    search_term = st.text_input("Enter search term")
    run = st.button(label="Search Google News")
    if run:
        driver = get_driver()
        data = get_news(driver, search_term)
        st.dataframe(data)


if __name__ == "__main__":
    main()