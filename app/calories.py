import streamlit as st
import sqlite3 as sql
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "fruitsAndVegetables.db"


def get_food_date():
    
    day = st.date_input("Choose a day")

    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT meal_type, total_kcal 
        FROM meal_with_totals 
        WHERE date = ?
    """, (day,))
    kcal_data = dict(cursor.fetchall())  # {meal_type: total_kcal}

    cursor.execute("""
        SELECT 
        m.meal_type,
        mi.id,
        f.name AS food,
        mi.grams AS grams,
        mi.quantity AS quantity,
        ROUND((mi.grams / 100.0) * f.kcal_per_100g, 2) AS kcal
        FROM meal_items mi
        JOIN meals m ON mi.meal_id = m.id
        JOIN food f ON mi.food_id = f.id
        WHERE m.date = ?
    """, (day,))
    items = cursor.fetchall()

    conn.close()

    return kcal_data, items

def delete_item_from_db(item_id):
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meal_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def display_data():

    kcal_data, items = get_food_date()
    meals = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Afternoon Snack"),
        ("supper", "Supper")
    ]

    for meal_type, label in meals:
        total_kcal = kcal_data.get(meal_type, 0)

        with st.expander(f"{label}: {total_kcal:.2f} kcal", expanded=False):

            meal_rows = []
            for row in items: 
                if row[0] == meal_type:
                    meal_rows.append(row)

            header_cols = st.columns([3, 2, 2, 2, 1])
            header_cols[0].markdown("**Food**")
            header_cols[1].markdown("**Grams**")
            header_cols[2].markdown("**Quantity**")
            header_cols[3].markdown("**Kcal**")

            for row in meal_rows:
                meal_type, item_id, food, grams, quantity, kcal = row
                cols = st.columns([3, 2, 2, 2, 1])
                cols[0].write(food)
                cols[1].write(grams)
                cols[2].write(quantity)
                cols[3].write(kcal)

                if cols[4].button("❌", key=f"del_{item_id}"):
                    delete_item_from_db(item_id)
                    st.rerun()
    
    day_kcal = sum(kcal_data.values()) 
    st.success(f"Total calories: {day_kcal:.2f} kcal")

if __name__ == "__main__":
    display_data()