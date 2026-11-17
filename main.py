import sqlite3
import flet as ft

def main(page: ft.Page):
    page.title = "نظام محاسبة المتجر"
    page.rtl = True  # تفعيل اللغة العربية من اليمين لليسار
    page.theme_mode = ft.ThemeMode.LIGHT

    # 1. إعداد قاعدة البيانات
    conn = sqlite3.connect("store.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )
    """)
    conn.commit()

    # 2. عناصر الواجهة
    name_input = ft.TextField(label="اسم المنتج")
    price_input = ft.TextField(label="السعر", keyboard_type=ft.KeyboardType.NUMBER)
    products_list = ft.Column()

    def load_products():
        products_list.controls.clear()
        cursor.execute("SELECT name, price FROM products")
        for row in cursor.fetchall():
            products_list.controls.append(
                ft.Text(f"• {row[0]} - السعر: {row[1]}", size=18)
            )
        page.update()

    def add_product(e):
        if name_input.value and price_input.value:
            cursor.execute(
                "INSERT INTO products (name, price) VALUES (?, ?)",
                (name_input.value, float(price_input.value))
            )
            conn.commit()
            name_input.value = ""
            price_input.value = ""
            load_products()

    add_btn = ft.ElevatedButton("إضافة المنتج للمخزن", on_click=add_product)

    # 3. إضافة العناصر للشاشة
    page.add(
        ft.Text("إدارة منتجات المتجر", size=24, weight=ft.FontWeight.BOLD),
        name_input,
        price_input,
        add_btn,
        ft.Divider(),
        ft.Text("قائمة المنتجات المسجلة:", size=20),
        products_list
    )
    load_products()

ft.app(target=main)
