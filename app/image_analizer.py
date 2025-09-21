import streamlit as st
from PIL import Image
import os
from ultralytics import YOLO
from collections import Counter
import sqlite3 as sql
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / "models" / "best.pt"
DB_PATH = BASE_DIR / "database" / "fruitsAndVegetables.db"


@st.cache_data
def load_data(image_file):
    img = Image.open(image_file)
    return img

def save_file(uploadedFile):
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    with open(os.path.join("temp",uploadedFile.name), "wb") as f:
        f.write(uploadedFile.getbuffer())

def process_image(img):
    model = YOLO(MODEL_PATH)
    results = model.predict(source="./temp/" + img.name, conf=0.25, device=0)
    detected_classes = []

    if len(results[0].boxes) > 0:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])   
            cls_name = results[0].names[cls_id] 
            detected_classes.append(cls_name)

        counts = Counter(detected_classes)
        
        plotted_img = results[0].plot()
        img_with_boxes = Image.fromarray(plotted_img[..., ::-1])

        return counts, img_with_boxes
    else:
        return {}, None
    
def image_analizer():
    st.subheader("Load or Scan your image")
    img_file = st.file_uploader("Upload your Image", type=["png", "jpg", "jpeg"])

    if img_file:
        save_file(img_file)
        counts, processed_img = process_image(img_file)
        if counts:
            st.image(processed_img, caption="Detections", use_container_width=True)
            for fruit, qty in counts.items():
                st.success(f"{qty}: {fruit}")

        else:
            st.text("No fruits/vegetables detected")
        
        meals = ["Breakfast", "Lunch", "Dinner", "Afternoon Snack", "Supper"]
        option =  st.selectbox("Add to:", meals)
        date = st.date_input("Choose a day")

        if st.button("Save"):
            for fruit, qty in counts.items():
                save_meal_database(fruit, option, date, qty)
            st.success(f"Food added to {option}")
            

def save_meal_database(food_name, option, date, qty):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()

    mapping = {
        "Breakfast": "breakfast",
        "Lunch": "lunch",
        "Dinner": "dinner",
        "Afternoon Snack": "snack",
        "Supper": "supper"
    }
    meal_type = mapping[option]

    cursor.execute(
        "SELECT id FROM meals WHERE date = ? AND meal_type = ?",
        (date, meal_type)
    )
    meal = cursor.fetchone()
    if meal:
        meal_id = meal[0]
    else:
        cursor.execute(
            "INSERT INTO meals (date, meal_type) VALUES (?, ?)",
            (date, meal_type)
        )
        meal_id = cursor.lastrowid

    cursor.execute("SELECT id, avg_weight FROM food WHERE name = ?", (food_name,))
    food = cursor.fetchone()
    if not food:
        st.error(f"{food_name} is not in the Food table")
        conn.close()
        return
    food_id, avg_weight = food

    grams = (avg_weight or 100) * qty

    cursor.execute(
        "SELECT id, grams, quantity FROM meal_items WHERE meal_id = ? AND food_id = ?",
        (meal_id, food_id)
    )
    existing_item = cursor.fetchone()

    if existing_item:
        item_id, old_grams, old_qty = existing_item
        new_grams = old_grams + grams
        new_qty = old_qty + qty
        cursor.execute(
            "UPDATE meal_items SET grams = ?, quantity = ? WHERE id = ?",
            (new_grams, new_qty, item_id)
        )
    else:
        cursor.execute(
            "INSERT INTO meal_items (meal_id, food_id, grams, quantity) VALUES (?, ?, ?, ?)",
            (meal_id, food_id, grams, qty)
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    image_analizer()
