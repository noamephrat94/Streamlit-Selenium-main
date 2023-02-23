import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import streamlit.components.v1 as components
import pandas as pd
import os

@st.cache_resource
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

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
    df = create_df()
    for country in countries.countries:
        st.title(country)
        url = f'https://www.google.com/search?q={search_term}%20{country}&tbm=nws'
        driver.get(url)
        driver.maximize_window()
        # scroll_page(driver)
        time.sleep(3)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        nav = soup.findAll("div", role="navigation")[1]
        pages = nav.findAll("td")
        url = ''
        for p in range(2, 3):
            if url:
                driver.get(url)
                time.sleep(3)
                html_source = driver.page_source
                soup = BeautifulSoup(html_source, 'html.parser')
            data = soup.findAll('div', class_='SoaBEf')
            data = data[0:5]
            for d in data:
                url = d.find('a')['href']
                title = d.findAll('span', dir="ltr")[1].text
                paragraph = d.findAll('span', dir="ltr")[2].text
                age = d.findAll('span')[4].text
                print(url, "\n", title, "\n", paragraph, "\n", age, "\n")
                df.loc[len(df)] = [url, title, paragraph, age]
                st.subheader(title)
                st.text(paragraph)
                st.text(age)
                link = f'[Read Article]({url})'
                st.markdown(link, unsafe_allow_html=True)
                st.markdown("""---""")
            url = "https://www.google.com/" + pages[p].find('a')['href']
    df.to_excel(f'output/{search_term}_{datetime.datetime.now().strftime("%m%d%Y-%H:%M:%S")}.')
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