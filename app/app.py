import streamlit as st
import pandas as pd
from PIL import Image
from image_analizer import image_analizer
from calories import display_data

IMAGES_PATH = "assets/images"
APP_ICON = Image.open(IMAGES_PATH + "/banana_icon.png")

st.set_page_config(page_title = "Calory Database", page_icon= APP_ICON, 
                   initial_sidebar_state="collapsed")

def main():
    menu = ["Scan Images", "Database"]
    option = st.sidebar.selectbox("Menu", menu,)

    if option == "Scan Images":
        image_analizer()
    elif option == "Database":
        display_data()

if __name__ == "__main__":
    main()