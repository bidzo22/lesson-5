import sqlite3
import os

# Перевіряємо, чи існує база даних
db_path = 'db.sqlite3'
if not os.path.exists(db_path):
    print(f"❌ Файл бази даних '{db_path}' не знайдено!")
    exit()

print(f"✅ Файл бази даних '{db_path}' знайдено")
print("=" * 50)

# Підключаємося до бази
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Отримуємо всі таблиці
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print(f"📊 Знайдено {len(tables)} таблиць:")
print("-" * 50)

# Виводимо всі таблиці
for table in tables:
    table_name = table[0]
    print(f"  📋 {table_name}")

# Перевіряємо чи є store_order
print("-" * 50)
if any(table[0] == 'store_order' for table in tables):
    print("✅ Таблиця 'store_order' ІСНУЄ!")
    
    # Показуємо структуру таблиці
    cursor.execute("PRAGMA table_info(store_order)")
    columns = cursor.fetchall()
    print("\n📋 Структура таблиці store_order:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # Показуємо кількість записів
    cursor.execute("SELECT COUNT(*) FROM store_order")
    count = cursor.fetchone()[0]
    print(f"\n📊 Кількість записів: {count}")
else:
    print("❌ Таблиця 'store_order' НЕ ІСНУЄ!")

conn.close()