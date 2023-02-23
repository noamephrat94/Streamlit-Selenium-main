import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@st.cache_resource
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# options = Options()
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')

driver = get_driver()
driver.get('http://www.google.com')

st.code(driver.page_source)