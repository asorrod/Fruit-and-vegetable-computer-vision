import sqlite3 as sql

def create_table_f():
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS food (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            food_class INTEGER UNIQUE,
            kcal_per_100g REAL NOT NULL,
            avg_weight REAL,
            avg_kcal REAL
        )"""
    )
    conn.commit()
    conn.close()

def create_table_m():
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            meal_type TEXT NOT NULL
        )"""
    )
    conn.commit()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS meal_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            grams REAL NOT NULL,
            quantity Integer,
            FOREIGN KEY (meal_id) REFERENCES meals(id),
            FOREIGN KEY (food_id) REFERENCES food(id)
        )"""
    )
    conn.commit()
    cursor.execute(
    """CREATE VIEW IF NOT EXISTS meal_with_totals AS
       SELECT m.id,
              m.date,
              m.meal_type,
              COALESCE(SUM((mi.grams / 100.0) * f.kcal_per_100g), 0) AS total_kcal
       FROM meals m
       LEFT JOIN meal_items mi ON mi.meal_id = m.id
       LEFT JOIN food f ON f.id = mi.food_id
       GROUP BY m.id"""
    )
    conn.commit()
    conn.close()

def insert_rows_f(fVkcal):
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.executemany(
        """INSERT OR IGNORE INTO food
        (name, food_class, kcal_per_100g, avg_weight, avg_kcal) VALUES (?,?,?,?,?)""", (fVkcal)
    )
    conn.commit()
    conn.close()

def delete_row(foodName):
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM food WHERE name like ? """, (f"%{foodName}%",)
    )
    conn.commit()
    conn.close()

def delete_table():
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.execute(
        """DROP TABLE meals"""
    )

def read_row():
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT  * FROM food"""
    )

    data = cursor.fetchall()
    conn.close()
    print(data)

def search_by_class(foodClass):
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT  * FROM food WHERE food_class= ?""", (foodClass, )
    )

    data = cursor.fetchall()
    conn.close()
    print(data)

def search(foodName):
    conn = sql.connect("fruitsAndVegetables.db")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT  * FROM food WHERE name like ?""", (f"%{foodName}%", )
    )

    data = cursor.fetchall()
    conn.close()
    print(data)




if __name__ == "__main__":

    fVkcal = [
        ("apple", 0, 52, 182, round(182/100 * 52, 1)),          
        ("banana", 1, 89, 118, round(118/100 * 89, 1)),         
        ("broccoli", 2, 34, 91, round(91/100 * 34, 1)),         
        ("carrot", 3, 41, 61, round(61/100 * 41, 1)),           
        ("orange/orange fruit", 4, 47, 131, round(131/100 * 47, 1)), 
        ("strawberry", 5, 32, 12, round(12/100 * 32, 1)),       
        ("tomato", 6, 18, 123, round(123/100 * 18, 1)),         
        ("grape", 7, 69, 80, round(80/100 * 69, 1)),            
        ("lemon", 8, 29, 58, round(58/100 * 29, 1)),            
        ("pineapple", 9, 50, 165, round(165/100 * 50, 1)),      
        ("cucumber/cuke", 10, 16, 100, round(100/100 * 16, 1)), 
        ("lettuce", 11, 15, 36, round(36/100 * 15, 1))          
    ]

    create_table_f()
    insert_rows_f(fVkcal)
    create_table_m()


    

