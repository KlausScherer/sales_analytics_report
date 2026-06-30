import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter

# =========================================================================
# CONFIGURACIÓN GENERAL
# =========================================================================
ruta = r"C:/Users/klaus/Documents/Perfil Profesional/GitHub/Proyecto_1/Libro_consolidado.xlsx"

sns.set(style="whitegrid")

# =========================================================================
# CARGA Y PREPARACIÓN DE DATOS
# =========================================================================
sales = pd.read_excel(ruta, sheet_name="sales")
products = pd.read_excel(ruta, sheet_name="products")

sales.columns = sales.columns.str.strip().str.lower()
products.columns = products.columns.str.strip().str.lower()

# Formatear Fechas y Meses ordenados cronológicamente
sales['sale_date'] = pd.to_datetime(sales['sale_date'], errors='coerce')
sales['mes_num'] = sales['sale_date'].dt.month

meses_dict = {
    1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio',
    7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'
}
sales['mes'] = sales['mes_num'].map(meses_dict)

# Combinar ventas y productos
df = sales.merge(products, on="product_id")

# Asegurar orden cronológico para los gráficos de meses
meses_ordenados = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                   'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
df['mes'] = pd.Categorical(df['mes'], categories=meses_ordenados, ordered=True)

# =========================================================================
# FORMATOS PERSONALIZADOS ($X.XXX / $X.XXX.XXX)
# =========================================================================
def formato_pesos_chilenos(x):
    """Formatea un número con signo $ y puntos como separadores de miles."""
    if pd.isna(x):
        return "$0"
    return f"${int(round(x)):,}".replace(",", ".")

def formato_pesos_formatter(x, pos):
    return formato_pesos_chilenos(x)

formatter = FuncFormatter(formato_pesos_formatter)

# =========================================================================
# FUNCIÓN AUXILIAR PARA DIBUJAR TABLAS PRO EN MATPLOTLIB
# =========================================================================
def tabla_pro(ax, df_tabla, titulo):
    ax.axis('off')
    ax.set_title(titulo, fontsize=12, fontweight='bold', loc='center', pad=10)

    tabla = ax.table(
        cellText=df_tabla.values,
        colLabels=df_tabla.columns,
        loc='center',
        cellLoc='center'
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 1.6)
    
    # Colorear la cabecera para un look corporativo
    for (row, col), cell in tabla.get_celld().items():
        if row == 0:
            cell.set_text_props(fontweight='bold', color='white')
            cell.set_facecolor('#1F497D')

# =========================================================================
# GENERACIÓN DEL INFORME PDF
# =========================================================================
with PdfPages("Informe_P1.pdf") as pdf:

    # ---------------------------------------------------------------------
    # PAG 1: PORTADA
    # ---------------------------------------------------------------------
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis('off')

    plt.text(0.5, 0.7, "Informe de Ventas", ha='center', fontsize=26, fontweight='bold', color='#1F497D')
    plt.text(0.5, 0.6, "Análisis General", ha='center', fontsize=16, fontstyle='italic', color='#595959')
    plt.text(0.5, 0.05, f"Fecha: {pd.Timestamp.today().date().strftime('%d/%m/%Y')}", ha='center', fontsize=11)

    pdf.savefig()
    plt.close()

    # ---------------------------------------------------------------------
    # PAG 2: RESUMEN GENERAL (HOJA 1)
    # ---------------------------------------------------------------------
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis('off')

    # KPIs Generales del Resumen
    ventas_totales = df['total_sale'].sum()
    cantidad_ventas = df.shape[0]
    ticket_promedio = df['total_sale'].mean()
    clientes_unicos = df['customer_id'].nunique()
    productos_unicos = df['product_id'].nunique()

    plt.text(0.5, 0.90, "Resumen General", ha='center', fontsize=20, fontweight='bold', color='#1F497D')
    
    plt.text(0.5, 0.80, f"Ventas Totales: {formato_pesos_chilenos(ventas_totales)}", ha='center', fontsize=14, fontweight='bold')
    plt.text(0.5, 0.75, f"Cantidad de Ventas: {cantidad_ventas:,}".replace(",", "."), ha='center', fontsize=12)
    plt.text(0.5, 0.70, f"Ticket Promedio: {formato_pesos_chilenos(ticket_promedio)}", ha='center', fontsize=12)
    plt.text(0.5, 0.65, f"Clientes únicos: {clientes_unicos}", ha='center', fontsize=12)
    plt.text(0.5, 0.60, f"Productos únicos: {productos_unicos}", ha='center', fontsize=12)

    # Gráfico de Ventas en el tiempo (Meses con etiquetas verticales)
    ventas_mes = df.groupby('mes', sort=False)['total_sale'].sum().reset_index()
    
    ax = fig.add_axes([0.15, 0.15, 0.75, 0.35])
    sns.lineplot(data=ventas_mes, x='mes', y='total_sale', ax=ax, marker='o', color='#1F497D', linewidth=2.5)
    ax.set_title("Ventas en el tiempo", fontsize=13, fontweight='bold', pad=10)
    ax.set_ylabel("Ventas Totales ($)")
    ax.set_xlabel("Meses")
    ax.yaxis.set_major_formatter(formatter)
    
    # Rotar etiquetas del eje X a posición vertical
    ax.set_xticklabels(ventas_mes['mes'], rotation='vertical')

    pdf.savefig()
    plt.close()

    # ---------------------------------------------------------------------
    # PAG 3: RESUMEN GENERAL (HOJA 2 - TABLAS DE TOP CLIENTES Y PRODUCTOS)
    # ---------------------------------------------------------------------
    fig, axs = plt.subplots(2, 1, figsize=(8.27, 11.69))

    # Top 5 Clientes con formato monetario corregido
    top_clientes = (
        df.groupby('customer_name')['total_sale']
        .sum().nlargest(5).reset_index()
        .rename(columns={'customer_name': 'Nombre del cliente', 'total_sale': 'Venta total'})
    )
    top_clientes['Venta total'] = top_clientes['Venta total'].apply(formato_pesos_chilenos)

    # Todos los Productos disponibles con su valor monetario
    total_productos = (
        df.groupby('product_name')['total_sale']
        .sum().sort_values(ascending=False).reset_index()
        .rename(columns={'product_name': 'Nombre del producto', 'total_sale': 'Venta total'})
    )
    total_productos['Venta total'] = total_productos['Venta total'].apply(formato_pesos_chilenos)

    tabla_pro(axs[0], top_clientes, "Top Clientes")
    tabla_pro(axs[1], total_productos, "Ventas Totales por Productos")

    pdf.savefig()
    plt.close()

    # ---------------------------------------------------------------------
    # PAG 4+: ANÁLISIS POR SUCURSAL
    # ---------------------------------------------------------------------
    for sucursal in sorted(df['branch'].unique()):
        data_suc = df[df['branch'] == sucursal]

        # Cálculos de KPI de la sucursal
        v_tot_suc = data_suc['total_sale'].sum()
        cant_v_suc = data_suc.shape[0]
        ticket_prom_suc = data_suc['total_sale'].mean()

        # Obtener el Cliente con la mayor venta total en esta sucursal
        top_cliente_suc = (
            data_suc.groupby('customer_name')['total_sale']
            .sum().nlargest(1).reset_index()
        )
        if not top_cliente_suc.empty:
            nom_cliente_top = top_cliente_suc.iloc[0]['customer_name']
            monto_cliente_top = formato_pesos_chilenos(top_cliente_suc.iloc[0]['total_sale'])
        else:
            nom_cliente_top = "N/A"
            monto_cliente_top = "$0"

        fig = plt.figure(figsize=(8.27, 11.69))
        plt.axis('off')

        # Título Centrado Arriba
        plt.text(0.5, 0.92, f"Análisis Sucursal: {sucursal}", ha='center', fontsize=18, fontweight='bold', color='#1F497D')
        
        # Datos e Indicadores de la Sucursal
        plt.text(0.5, 0.82, f"Ventas Totales: {formato_pesos_chilenos(v_tot_suc)}", ha='center', fontsize=13, fontweight='bold')
        plt.text(0.5, 0.77, f"Cantidad de Ventas: {cant_v_suc:,}".replace(",", "."), ha='center', fontsize=11)
        plt.text(0.5, 0.72, f"Ticket Promedio: {formato_pesos_chilenos(ticket_prom_suc)}", ha='center', fontsize=11)
        plt.text(0.5, 0.65, f"Cliente con Mayor Venta: {nom_cliente_top} ({monto_cliente_top})", ha='center', fontsize=11, color='#2E75B6', fontweight='bold')

        # Gráfico con las ventas por mes específico de esta sucursal
        ventas_mes_suc = data_suc.groupby('mes', sort=False)['total_sale'].sum().reset_index()
        
        ax_suc = fig.add_axes([0.15, 0.15, 0.75, 0.35])
        sns.lineplot(data=ventas_mes_suc, x='mes', y='total_sale', ax=ax_suc, marker='o', color='#2E75B6', linewidth=2)
        ax_suc.set_title(f"Evolución de Ventas - {sucursal}", fontsize=12, fontweight='bold', pad=10)
        ax_suc.set_ylabel("Ventas ($)")
        ax_suc.set_xlabel("Meses")
        ax_suc.yaxis.set_major_formatter(formatter)
        ax_suc.set_xticklabels(ventas_mes_suc['mes'], rotation='vertical')

        pdf.savefig()
        plt.close()

    # ---------------------------------------------------------------------
    # PAG FINAL: GRÁFICOS DE PORCENTAJES (DISTRIBUCIÓN)
    # ---------------------------------------------------------------------
    # Título separador inicial para la sección de proporciones
    fig = plt.figure(figsize=(8.27, 11.69))
    plt.axis('off')
    plt.text(0.5, 0.5, "Análisis del porcentaje del total", ha='center', fontsize=22, fontweight='bold', color='#1F497D')
    pdf.savefig()
    plt.close()

    # Configuración de paletas suaves para los gráficos de torta
    colors_pie = sns.color_palette('Blues_r', 8)

    # 1. Gráfico Torta - SUCURSAL
    suc = df.groupby('branch')['total_sale'].sum()
    fig = plt.figure(figsize=(8, 8))
    plt.pie(suc, labels=suc.index, autopct='%1.1f%%', pctdistance=0.8, colors=colors_pie, startangle=90, 
            textprops={'fontsize': 11})
    plt.title("% Ventas por Sucursal", fontsize=14, fontweight='bold', pad=20)
    pdf.savefig()
    plt.close()

    # 2. Gráfico Torta - PRODUCTO (MODIFICACIÓN: Muestra TODOS los productos disponibles)
    prod = df.groupby('product_name')['total_sale'].sum().sort_values(ascending=False)
    fig = plt.figure(figsize=(8, 8))
    plt.pie(prod, labels=prod.index, autopct='%1.1f%%', pctdistance=0.8, colors=sns.color_palette('Blues_r', len(prod)), startangle=140, 
            textprops={'fontsize': 11})
    plt.title("% Ventas por Producto", fontsize=14, fontweight='bold', pad=20)
    pdf.savefig()
    plt.close()

    # 3. Gráfico Torta - MES
    mes_pie = df.groupby('mes')['total_sale'].sum()
    fig = plt.figure(figsize=(8, 8))
    plt.pie(mes_pie, labels=mes_pie.index, autopct='%1.1f%%', pctdistance=0.8, colors=sns.color_palette('light:b', 12), 
            startangle=90, textprops={'fontsize': 10})
    plt.title("% Ventas por Mes", fontsize=14, fontweight='bold', pad=20)
    pdf.savefig()
    plt.close()

print("✅ Informe generado PERFECTO en base al diseño requerido.")