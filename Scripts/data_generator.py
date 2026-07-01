# =========================
# 0. IMPORTAR LIBRERIAS
# =========================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import date

fake = Faker('es_ES')
np.random.seed(42)

# =========================
# 1. TABLA PRODUCTOS
# =========================

products = [
    {"product_id": 1, "product_name": "Cemento", "price_per_100kg": 7000},
    {"product_id": 2, "product_name": "Ladrillos", "price_per_100kg": 5000},
    {"product_id": 3, "product_name": "Arena", "price_per_100kg": 3000},
    {"product_id": 4, "product_name": "Fierros", "price_per_100kg": 12000},
    {"product_id": 5, "product_name": "Madera", "price_per_100kg": 9000},
    {"product_id": 6, "product_name": "Yeso", "price_per_100kg": 4000},
    {"product_id": 7, "product_name": "Alambres", "price_per_100kg": 8000},
    {"product_id": 8, "product_name": "Grava", "price_per_100kg": 3500}
]

df_products = pd.DataFrame(products)
df_products["category"] = "Materiales de construcción"
df_products["unit"] = "100kg"

# =========================
# 2. CLIENTES
# =========================

names_correct = [fake.first_name() for _ in range(250)]
names_errors = [
    "Klaudio", "Maria", "Frnanda", "Marsela", "J pablo",
    "walter", "Ana Lorena", "Hanns"
]

last_names_correct = [fake.last_name() for _ in range(280)]
last_names_errors = ["prado", "Liyo", "fernandez", "Pasheco", "Gnzález", "Sánches"]

customers = []

for i in range(300):

    # Nombre
    if random.random() < 0.15:
        first_name = random.choice(names_errors)
    else:
        first_name = random.choice(names_correct)

    # Apellido
    if random.random() < 0.15:
        last_name = random.choice(last_names_errors)
    else:
        last_name = random.choice(last_names_correct)

    full_name = f"{first_name} {last_name}"

    customers.append({
        "customer_id": i + 1,
        "customer_name": full_name
    })

df_customers = pd.DataFrame(customers)

# AGREGAR DUPLICADOS DE CLIENTES
duplicates_customers = df_customers.sample(frac=0.1, random_state=42)
df_customers = pd.concat([df_customers, duplicates_customers], ignore_index=True)

# =========================
# 3. SUCURSALES (CON ERRORES)
# =========================

branches = [
    "Santiago", "Stgo", "snatiago", "santiago",
    "Puerto Montt", "PMontt", "Prt montt", "puerto mont",
    "Concepción", "conce", "consepcion",
    "Valparaíso", "Valpo", "valparaiso", "Vlpo",
    "Calama", "Clama", "calama", "calma",
    "Rancagua", "rancagua", "rcgua", "rancajua"
]

# =========================
# 4. TABLA VENTAS
# =========================

sales = []

for i in range(1000):

    product = random.choice(products)
    quantity = np.random.randint(1, 20)

    total = quantity * product["price_per_100kg"]

    sale_date = fake.date_between(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31)
    )

    customer = random.choice(customers)

    sale = {
        # posible duplicado de ID
        "sale_id": i if random.random() < 0.03 else i + 1,
        "product_id": product["product_id"],
        "quantity_100kg": quantity,
        "total_sale": total,
        "branch": random.choice(branches),
        "customer_id": customer["customer_id"],
        "customer_name": customer["customer_name"],
        "sale_date": sale_date
    }

    sales.append(sale)

df_sales = pd.DataFrame(sales)

# AGREGAR FILAS DUPLICADAS
duplicates_sales = df_sales.sample(frac=0.1, random_state=42)
df_sales = pd.concat([df_sales, duplicates_sales], ignore_index=True)

# =========================
# 5. AJUSTES FINALES
# =========================

df_sales["sale_date"] = pd.to_datetime(df_sales["sale_date"])

# =========================
# 6. EXPORTAR CSV
# =========================

df_products.to_csv("products.csv", index=False)
df_sales.to_csv("sales.csv", index=False)

print("Archivos generados correctamente:")
print("- products.csv")
print("- sales.csv")