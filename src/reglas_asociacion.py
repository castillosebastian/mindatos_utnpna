#!/usr/bin/env python3

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
import warnings
warnings.filterwarnings('ignore')

def cargarDatosTransformados(ruta_archivo: str) -> pd.DataFrame:
    """
    Carga el dataset transformado desde archivo CSV
    """
    print("Cargando datos transformados...")
    df = pd.read_csv(ruta_archivo)
    print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df

def prepararDatosTransaccionales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara los datos en formato transaccional para reglas de asociación
    """
    print("\n=== PREPARACIÓN DE DATOS TRANSACCIONALES ===")
    
    # Seleccionar columnas relevantes para análisis de asociación
    columnas_analisis = [
        'Zona Destino', 'Raza', 'Categoria', 
        'CabezasDisc', 'PrecioKgDisc', 'CantidadKgDisc'
    ]
    
    # Filtrar columnas existentes
    columnas_existentes = [col for col in columnas_analisis if col in df.columns]
    print(f"Columnas para análisis: {columnas_existentes}")
    
    # Crear subset de datos
    df_subset = df[columnas_existentes].copy()
    
    # Eliminar filas con valores faltantes
    df_limpio = df_subset.dropna()
    registros_eliminados = len(df_subset) - len(df_limpio)
    
    print(f"Registros con valores faltantes eliminados: {registros_eliminados}")
    print(f"Registros finales para análisis: {len(df_limpio)}")
    
    return df_limpio

def crearMatrizTransaccional(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte los datos categóricos a formato de matriz transaccional binaria
    """
    print("\n=== CREACIÓN DE MATRIZ TRANSACCIONAL ===")
    
    # Crear lista de transacciones
    transacciones = []
    for _, fila in df.iterrows():
        transaccion = []
        for columna in df.columns:
            valor = str(fila[columna])
            if pd.notna(valor) and valor != 'nan':
                transaccion.append(f"{columna}_{valor}")
        transacciones.append(transaccion)
    
    print(f"Total de transacciones creadas: {len(transacciones)}")
    
    # Usar TransactionEncoder para crear matriz binaria
    te = TransactionEncoder()
    te_ary = te.fit(transacciones).transform(transacciones)
    df_transaccional = pd.DataFrame(te_ary, columns=te.columns_)
    
    print(f"Dimensiones de matriz transaccional: {df_transaccional.shape}")
    print(f"Total de items únicos: {len(df_transaccional.columns)}")
    
    return df_transaccional

def analizarFrecuenciaItems(df_transaccional: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza la frecuencia de items individuales
    """
    print("\n=== ANÁLISIS DE FRECUENCIA DE ITEMS ===")
    
    frecuencias = df_transaccional.sum().sort_values(ascending=False)
    porcentajes = (frecuencias / len(df_transaccional) * 100).round(2)
    
    print("Top 20 items más frecuentes:")
    for i, (item, freq) in enumerate(frecuencias.head(20).items()):
        porcentaje = porcentajes[item]
        print(f"  {i+1:2d}. {item}: {freq} ({porcentaje}%)")
    
    # Crear DataFrame con estadísticas
    stats_items = pd.DataFrame({
        'Item': frecuencias.index,
        'Frecuencia': frecuencias.values,
        'Soporte': porcentajes.values / 100
    })
    
    return stats_items

def ejecutarApriori(df_transaccional: pd.DataFrame, min_support: float = 0.01) -> pd.DataFrame:
    """
    Ejecuta algoritmo Apriori para encontrar itemsets frecuentes
    """
    print(f"\n=== ALGORITMO APRIORI (Soporte mínimo: {min_support}) ===")
    
    # Ejecutar Apriori
    itemsets_frecuentes = apriori(df_transaccional, 
                                 min_support=min_support, 
                                 use_colnames=True)
    
    if len(itemsets_frecuentes) == 0:
        print("No se encontraron itemsets frecuentes con el soporte mínimo especificado")
        return pd.DataFrame()
    
    # Ordenar por soporte
    itemsets_frecuentes = itemsets_frecuentes.sort_values('support', ascending=False)
    
    print(f"Itemsets frecuentes encontrados: {len(itemsets_frecuentes)}")
    
    # Mostrar top 10
    print("\nTop 10 itemsets frecuentes:")
    for i, (idx, row) in enumerate(itemsets_frecuentes.head(10).iterrows()):
        itemset = list(row['itemsets'])
        soporte = row['support']
        print(f"  {i+1:2d}. {itemset} (soporte: {soporte:.4f})")
    
    return itemsets_frecuentes

def generarReglasAsociacion(itemsets_frecuentes: pd.DataFrame, 
                           min_confidence: float = 0.1,
                           min_lift: float = 1.0) -> pd.DataFrame:
    """
    Genera reglas de asociación a partir de itemsets frecuentes
    """
    print(f"\n=== GENERACIÓN DE REGLAS DE ASOCIACIÓN ===")
    print(f"Confianza mínima: {min_confidence}")
    print(f"Lift mínimo: {min_lift}")
    
    if len(itemsets_frecuentes) == 0:
        print("No hay itemsets frecuentes para generar reglas")
        return pd.DataFrame()
    
    # Generar reglas
    reglas = association_rules(itemsets_frecuentes, 
                              metric="confidence", 
                              min_threshold=min_confidence)
    
    if len(reglas) == 0:
        print("No se generaron reglas con los parámetros especificados")
        return pd.DataFrame()
    
    # Filtrar por lift
    reglas_filtradas = reglas[reglas['lift'] >= min_lift]
    
    print(f"Reglas generadas: {len(reglas)}")
    print(f"Reglas después de filtrar por lift: {len(reglas_filtradas)}")
    
    return reglas_filtradas

def analizarReglasInteresantes(reglas: pd.DataFrame, top_n: int = 10) -> dict:
    """
    Analiza y selecciona las reglas más interesantes según diferentes criterios
    """
    print(f"\n=== ANÁLISIS DE REGLAS INTERESANTES ===")
    
    if len(reglas) == 0:
        return {}
    
    analisis = {}
    
    # Top reglas por confianza
    reglas_confianza = reglas.sort_values('confidence', ascending=False).head(top_n)
    analisis['top_confianza'] = reglas_confianza
    
    # Top reglas por lift
    reglas_lift = reglas.sort_values('lift', ascending=False).head(top_n)
    analisis['top_lift'] = reglas_lift
    
    # Top reglas por soporte
    reglas_soporte = reglas.sort_values('support', ascending=False).head(top_n)
    analisis['top_soporte'] = reglas_soporte
    
    # Reglas balanceadas (combinación de métricas)
    reglas['score_combinado'] = (reglas['confidence'] * 0.4 + 
                                reglas['lift'] * 0.4 + 
                                reglas['support'] * 0.2)
    reglas_balanceadas = reglas.sort_values('score_combinado', ascending=False).head(top_n)
    analisis['top_balanceadas'] = reglas_balanceadas
    
    return analisis

def mostrarReglasDetalladas(analisis: dict):
    """
    Muestra las reglas interesantes con formato detallado
    """
    print("\n" + "="*80)
    print("REGLAS DE ASOCIACIÓN MÁS INTERESANTES")
    print("="*80)
    
    categorias = [
        ('top_confianza', 'TOP 5 REGLAS POR CONFIANZA'),
        ('top_lift', 'TOP 5 REGLAS POR LIFT'),
        ('top_soporte', 'TOP 5 REGLAS POR SOPORTE'),
        ('top_balanceadas', 'TOP 5 REGLAS BALANCEADAS')
    ]
    
    for categoria, titulo in categorias:
        if categoria in analisis and len(analisis[categoria]) > 0:
            print(f"\n{titulo}")
            print("-" * len(titulo))
            
            for i, (idx, regla) in enumerate(analisis[categoria].head(5).iterrows()):
                antecedent = list(regla['antecedents'])
                consequent = list(regla['consequents'])
                
                print(f"\n{i+1}. {antecedent} => {consequent}")
                print(f"   Soporte: {regla['support']:.4f}")
                print(f"   Confianza: {regla['confidence']:.4f}")
                print(f"   Lift: {regla['lift']:.4f}")
                if 'score_combinado' in regla:
                    print(f"   Score Combinado: {regla['score_combinado']:.4f}")

def ejecutarFpGrowth(df_transaccional: pd.DataFrame, min_support: float = 0.01) -> pd.DataFrame:
    """
    Ejecuta algoritmo FP-Growth como alternativa a Apriori
    """
    print(f"\n=== ALGORITMO FP-GROWTH (Soporte mínimo: {min_support}) ===")
    
    try:
        # Ejecutar FP-Growth
        itemsets_fp = fpgrowth(df_transaccional, 
                              min_support=min_support, 
                              use_colnames=True)
        
        if len(itemsets_fp) == 0:
            print("No se encontraron itemsets frecuentes con FP-Growth")
            return pd.DataFrame()
        
        # Ordenar por soporte
        itemsets_fp = itemsets_fp.sort_values('support', ascending=False)
        
        print(f"Itemsets frecuentes encontrados con FP-Growth: {len(itemsets_fp)}")
        
        return itemsets_fp
        
    except Exception as e:
        print(f"Error ejecutando FP-Growth: {e}")
        return pd.DataFrame()

def compararAlgoritmos(itemsets_apriori: pd.DataFrame, itemsets_fp: pd.DataFrame):
    """
    Compara resultados entre Apriori y FP-Growth
    """
    print("\n=== COMPARACIÓN DE ALGORITMOS ===")
    
    if len(itemsets_apriori) > 0 and len(itemsets_fp) > 0:
        print(f"Itemsets Apriori: {len(itemsets_apriori)}")
        print(f"Itemsets FP-Growth: {len(itemsets_fp)}")
        
        # Verificar si son iguales
        if len(itemsets_apriori) == len(itemsets_fp):
            print("Ambos algoritmos encontraron el mismo número de itemsets")
        else:
            print("Los algoritmos encontraron diferente número de itemsets")
    else:
        print("No se pueden comparar - uno o ambos algoritmos no generaron resultados")

def guardarReporteReglas(analisis: dict, stats_items: pd.DataFrame, 
                        itemsets_frecuentes: pd.DataFrame, reglas: pd.DataFrame,
                        ruta_reporte: str):
    """
    Guarda el reporte completo de reglas de asociación
    """
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS DE REGLAS DE ASOCIACIÓN\n")
        f.write("Dataset: SIO-Carnes - Operaciones de Compra-Venta de Ganado Vacuno\n")
        f.write("="*70 + "\n\n")
        
        # Resumen ejecutivo
        f.write("RESUMEN EJECUTIVO\n")
        f.write("-"*20 + "\n")
        f.write(f"Total de itemsets frecuentes: {len(itemsets_frecuentes)}\n")
        f.write(f"Total de reglas generadas: {len(reglas)}\n")
        f.write(f"Items únicos analizados: {len(stats_items)}\n\n")
        
        # Top items frecuentes
        f.write("TOP 10 ITEMS MÁS FRECUENTES\n")
        f.write("-"*30 + "\n")
        for i, (idx, item) in enumerate(stats_items.head(10).iterrows()):
            f.write(f"{i+1:2d}. {item['Item']}: {item['Frecuencia']} (soporte: {item['Soporte']:.4f})\n")
        f.write("\n")
        
        # Reglas interesantes por categoría
        categorias = [
            ('top_confianza', 'REGLAS CON MAYOR CONFIANZA'),
            ('top_lift', 'REGLAS CON MAYOR LIFT'),
            ('top_soporte', 'REGLAS CON MAYOR SOPORTE'),
            ('top_balanceadas', 'REGLAS MEJOR BALANCEADAS')
        ]
        
        for categoria, titulo in categorias:
            if categoria in analisis and len(analisis[categoria]) > 0:
                f.write(f"{titulo}\n")
                f.write("-" * len(titulo) + "\n")
                
                for i, (idx, regla) in enumerate(analisis[categoria].head(5).iterrows()):
                    antecedent = list(regla['antecedents'])
                    consequent = list(regla['consequents'])
                    
                    f.write(f"\n{i+1}. {antecedent} => {consequent}\n")
                    f.write(f"   Soporte: {regla['support']:.4f}\n")
                    f.write(f"   Confianza: {regla['confidence']:.4f}\n")
                    f.write(f"   Lift: {regla['lift']:.4f}\n")
                    
                    # Interpretación de la regla
                    if regla['confidence'] > 0.7:
                        f.write("   Interpretación: Regla de alta confianza\n")
                    elif regla['lift'] > 2.0:
                        f.write("   Interpretación: Fuerte asociación positiva\n")
                    elif regla['support'] > 0.1:
                        f.write("   Interpretación: Patrón frecuente\n")
                
                f.write("\n")
        
        # Interpretación de negocio
        f.write("INTERPRETACIÓN PARA EL NEGOCIO GANADERO\n")
        f.write("-"*40 + "\n")
        f.write("Las reglas de asociación revelan patrones importantes en el mercado:\n")
        f.write("- Asociaciones entre zonas geográficas y razas específicas\n")
        f.write("- Patrones de precios según categorías de ganado\n")
        f.write("- Relaciones entre cantidad comercializada y características\n")
        f.write("- Tendencias regionales en tipos de ganado preferidos\n\n")
        
        f.write("RECOMENDACIONES\n")
        f.write("-"*15 + "\n")
        f.write("1. Usar reglas de alta confianza para predicciones de mercado\n")
        f.write("2. Identificar nichos de mercado mediante reglas de alto lift\n")
        f.write("3. Optimizar logística basada en patrones geográficos\n")
        f.write("4. Ajustar estrategias comerciales por región y raza\n\n")
        
        f.write("MÉTRICAS UTILIZADAS\n")
        f.write("-"*18 + "\n")
        f.write("- Soporte: Frecuencia relativa del itemset en el dataset\n")
        f.write("- Confianza: Probabilidad condicional de la regla\n")
        f.write("- Lift: Medida de dependencia entre antecedente y consecuente\n")
        f.write("- Score Combinado: Métrica balanceada (40% confianza + 40% lift + 20% soporte)\n")
    
    print(f"Reporte guardado en: {ruta_reporte}")

def main():
    """
    Función principal que ejecuta el análisis completo de reglas de asociación
    """
    # Rutas de archivos
    ruta_datos = 'data/datos_transformados.csv'
    ruta_reporte = 'analisis/reglas_asociacion.txt'
    
    # Cargar datos transformados
    df = cargarDatosTransformados(ruta_datos)
    
    # Preparar datos transaccionales
    df_transaccional_prep = prepararDatosTransaccionales(df)
    
    # Crear matriz transaccional binaria
    df_matriz = crearMatrizTransaccional(df_transaccional_prep)
    
    # Analizar frecuencia de items
    stats_items = analizarFrecuenciaItems(df_matriz)
    
    # Ejecutar Apriori con diferentes valores de soporte
    soportes = [0.05, 0.03, 0.01]
    itemsets_mejor = pd.DataFrame()
    soporte_usado = 0.01
    
    for soporte in soportes:
        itemsets = ejecutarApriori(df_matriz, soporte)
        if len(itemsets) > 0:
            itemsets_mejor = itemsets
            soporte_usado = soporte
            break
    
    if len(itemsets_mejor) == 0:
        print("No se pudieron generar itemsets frecuentes")
        return
    
    # Ejecutar FP-Growth para comparación
    itemsets_fp = ejecutarFpGrowth(df_matriz, soporte_usado)
    compararAlgoritmos(itemsets_mejor, itemsets_fp)
    
    # Generar reglas de asociación
    reglas = generarReglasAsociacion(itemsets_mejor, min_confidence=0.1, min_lift=1.0)
    
    if len(reglas) == 0:
        print("No se pudieron generar reglas de asociación")
        return
    
    # Analizar reglas interesantes
    analisis = analizarReglasInteresantes(reglas)
    
    # Mostrar resultados detallados
    mostrarReglasDetalladas(analisis)
    
    # Guardar reporte
    guardarReporteReglas(analisis, stats_items, itemsets_mejor, reglas, ruta_reporte)
    
    print("\n" + "="*80)
    print("ANÁLISIS DE REGLAS DE ASOCIACIÓN COMPLETADO EXITOSAMENTE")
    print("="*80)

if __name__ == "__main__":
    main()
