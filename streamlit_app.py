import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import streamlit.components.v1 as components

@st.cache_resource
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

url = 'http://www.google.com'
driver = get_driver()
driver.get(url)

components.iframe(url)
st.code(driver.page_source)