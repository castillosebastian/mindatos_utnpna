#!/usr/bin/env python3

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import KBinsDiscretizer
import warnings
warnings.filterwarnings('ignore')

def cargarDatos(ruta_archivo: str) -> pd.DataFrame:
    print("Cargando dataset...")
    df = pd.read_csv(ruta_archivo)
    print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df

def analizarCalidadDatos(df: pd.DataFrame) -> dict:
    print("\n=== ANÁLISIS DE CALIDAD DE DATOS ===")
    
    calidad = {}
    total_registros = len(df)
    
    valores_faltantes = df.isnull().sum()
    porcentaje_faltantes = (valores_faltantes / total_registros * 100).round(2)
    
    print(f"Total de registros: {total_registros}")
    print("Valores faltantes por columna:")
    for col in df.columns:
        faltantes = valores_faltantes[col]
        porcentaje = porcentaje_faltantes[col]
        print(f"  {col}: {faltantes} ({porcentaje}%)")
    
    duplicados = df.duplicated().sum()
    porcentaje_duplicados = (duplicados / total_registros * 100).round(2)
    print(f"\nRegistros duplicados: {duplicados} ({porcentaje_duplicados}%)")
    
    calidad['valores_faltantes'] = valores_faltantes.to_dict()
    calidad['duplicados'] = duplicados
    
    return calidad

def eliminarColumnasInutilizables(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== ELIMINACIÓN DE COLUMNAS INUTILIZABLES ===")
    
    porcentaje_faltantes = (df.isnull().sum() / len(df) * 100)
    columnas_eliminar = porcentaje_faltantes[porcentaje_faltantes > 90].index.tolist()
    
    if columnas_eliminar:
        print(f"Eliminando columnas con >90% de valores faltantes: {columnas_eliminar}")
        df = df.drop(columns=columnas_eliminar)
    else:
        print("No se encontraron columnas con >90% de valores faltantes")
    
    return df

def tratarValoresFaltantes(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== TRATAMIENTO DE VALORES FALTANTES ===")
    
    registros_iniciales = len(df)
    columnas_criticas = ['Precio Kg', 'Cantidad de Kg']
    columnas_existentes = [col for col in columnas_criticas if col in df.columns]
    
    if columnas_existentes:
        df_limpio = df.dropna(subset=columnas_existentes)
        registros_eliminados = registros_iniciales - len(df_limpio)
        print(f"Registros eliminados por valores faltantes: {registros_eliminados}")
        print(f"Registros restantes: {len(df_limpio)}")
        return df_limpio
    
    return df

def eliminarDuplicados(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== ELIMINACIÓN DE DUPLICADOS ===")
    
    registros_iniciales = len(df)
    df_sin_duplicados = df.drop_duplicates()
    duplicados_eliminados = registros_iniciales - len(df_sin_duplicados)
    
    print(f"Duplicados eliminados: {duplicados_eliminados}")
    print(f"Registros restantes: {len(df_sin_duplicados)}")
    
    return df_sin_duplicados

def detectarOutliers(serie: pd.Series) -> tuple:
    Q1 = serie.quantile(0.25)
    Q3 = serie.quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = (serie < limite_inferior) | (serie > limite_superior)
    return outliers, limite_inferior, limite_superior

def tratarOutliers(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== TRATAMIENTO DE OUTLIERS ===")
    
    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    print(f"Columnas numéricas identificadas: {columnas_numericas}")
    
    df_sin_outliers = df.copy()
    
    for columna in columnas_numericas:
        if columna in df.columns:
            registros_antes = len(df_sin_outliers)
            outliers, lim_inf, lim_sup = detectarOutliers(df_sin_outliers[columna])
            num_outliers = outliers.sum()
            
            if num_outliers > 0:
                print(f"\n{columna}:")
                print(f"  Outliers detectados: {num_outliers} ({num_outliers/len(df_sin_outliers)*100:.2f}%)")
                print(f"  Límites: [{lim_inf:.2f}, {lim_sup:.2f}]")
                
                if num_outliers / len(df_sin_outliers) < 0.15:
                    df_sin_outliers = df_sin_outliers[~outliers]
                    registros_despues = len(df_sin_outliers)
                    print(f"  Registros eliminados: {registros_antes - registros_despues}")
                else:
                    print(f"  Outliers no eliminados (>15% de los datos)")
    
    print(f"\nRegistros totales después del tratamiento de outliers: {len(df_sin_outliers)}")
    return df_sin_outliers

def discretizarVariablesContinuas(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== DISCRETIZACIÓN DE VARIABLES CONTINUAS ===")
    
    df_discretizado = df.copy()
    
    columnas_discretizar = {
        'Cabezas Comercializadas': 'CabezasDisc',
        'Precio Kg': 'PrecioKgDisc', 
        'Cantidad de Kg': 'CantidadKgDisc'
    }
    
    for col_original, col_nueva in columnas_discretizar.items():
        if col_original in df.columns:
            print(f"\nDiscretizando {col_original}...")
            
            # Limpiar valores NaN antes de discretizar
            datos_limpios = df_discretizado[col_original].dropna()
            
            if len(datos_limpios) == 0:
                print(f"  No hay datos válidos para discretizar en {col_original}")
                continue
            
            # Crear máscara para valores válidos
            mask_validos = df_discretizado[col_original].notna()
            
            # Discretizar solo los valores válidos
            discretizer = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')
            valores_discretizados = discretizer.fit_transform(datos_limpios.values.reshape(-1, 1)).flatten()
            
            # Crear etiquetas
            bin_edges = discretizer.bin_edges_[0]
            etiquetas = []
            for i in range(len(bin_edges)-1):
                etiqueta = f"{col_nueva}_{i+1}_({bin_edges[i]:.1f}-{bin_edges[i+1]:.1f})"
                etiquetas.append(etiqueta)
            
            # Crear nueva columna con valores discretizados
            df_discretizado[col_nueva] = np.nan
            df_discretizado.loc[mask_validos, col_nueva] = valores_discretizados.astype(int)
            
            # Mapear a etiquetas
            for i, etiqueta in enumerate(etiquetas):
                df_discretizado.loc[df_discretizado[col_nueva] == i, col_nueva] = etiqueta
            
            print(f"  Rangos creados: {len(etiquetas)}")
            for i, etiqueta in enumerate(etiquetas):
                count = (df_discretizado[col_nueva] == etiqueta).sum()
                print(f"    {etiqueta}: {count} registros")
            
            # Contar valores faltantes
            nan_count = df_discretizado[col_nueva].isna().sum()
            if nan_count > 0:
                print(f"    Valores faltantes: {nan_count} registros")
    
    return df_discretizado

def crearVariablesDerivadas(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== CREACIÓN DE VARIABLES DERIVADAS ===")
    
    df_derivado = df.copy()
    
    # Convertir columnas numéricas a float
    if 'Precio Kg' in df.columns:
        df_derivado['Precio Kg'] = pd.to_numeric(df_derivado['Precio Kg'], errors='coerce')
        print("Columna 'Precio Kg' convertida a numérica")
    
    if 'Cantidad de Kg' in df.columns:
        df_derivado['Cantidad de Kg'] = pd.to_numeric(df_derivado['Cantidad de Kg'], errors='coerce')
        print("Columna 'Cantidad de Kg' convertida a numérica")
    
    if 'Cabezas Comercializadas' in df.columns:
        df_derivado['Cabezas Comercializadas'] = pd.to_numeric(df_derivado['Cabezas Comercializadas'], errors='coerce')
        print("Columna 'Cabezas Comercializadas' convertida a numérica")
    
    # Crear variable Total Vendido
    if 'Precio Kg' in df.columns and 'Cantidad de Kg' in df.columns:
        df_derivado['Total Vendido'] = df_derivado['Precio Kg'] * df_derivado['Cantidad de Kg']
        print("Variable creada: Total Vendido")
    
    # Crear variables temporales
    if 'Fecha Comprobante' in df.columns:
        try:
            df_derivado['Fecha Comprobante'] = pd.to_datetime(df_derivado['Fecha Comprobante'], dayfirst=True)
            df_derivado['Mes'] = df_derivado['Fecha Comprobante'].dt.month
            df_derivado['Trimestre'] = df_derivado['Fecha Comprobante'].dt.quarter
            df_derivado['Semestre'] = ((df_derivado['Mes'] - 1) // 6) + 1
            print("Variables temporales creadas: Mes, Trimestre, Semestre")
        except:
            print("No se pudieron crear variables temporales")
    
    return df_derivado

def normalizarValoresCategoricos(df: pd.DataFrame) -> pd.DataFrame:
    print("\n=== NORMALIZACIÓN DE VALORES CATEGÓRICOS ===")
    
    df_normalizado = df.copy()
    columnas_categoricas = df_normalizado.select_dtypes(include=['object']).columns
    
    for columna in columnas_categoricas:
        if columna != 'Fecha Comprobante':
            df_normalizado[columna] = df_normalizado[columna].astype(str).str.strip().str.upper()
            print(f"Normalizada columna: {columna}")
    
    return df_normalizado

def generarResumenTransformaciones(df_original: pd.DataFrame, df_final: pd.DataFrame) -> dict:
    print("\n=== RESUMEN DE TRANSFORMACIONES ===")
    
    resumen = {
        'registros_originales': len(df_original),
        'registros_finales': len(df_final),
        'registros_eliminados': len(df_original) - len(df_final),
        'porcentaje_retenido': round((len(df_final) / len(df_original) * 100), 2),
        'columnas_originales': len(df_original.columns),
        'columnas_finales': len(df_final.columns),
        'columnas_agregadas': len(df_final.columns) - len(df_original.columns)
    }
    
    print(f"Registros originales: {resumen['registros_originales']}")
    print(f"Registros finales: {resumen['registros_finales']}")
    print(f"Registros eliminados: {resumen['registros_eliminados']}")
    print(f"Porcentaje retenido: {resumen['porcentaje_retenido']}%")
    print(f"Columnas originales: {resumen['columnas_originales']}")
    print(f"Columnas finales: {resumen['columnas_finales']}")
    print(f"Columnas agregadas: {resumen['columnas_agregadas']}")
    
    return resumen

def guardarDatosTransformados(df: pd.DataFrame, ruta_salida: str):
    print(f"\nGuardando dataset transformado en: {ruta_salida}")
    df.to_csv(ruta_salida, index=False)
    print("Dataset guardado exitosamente")

def guardarReporteTransformaciones(resumen: dict, ruta_reporte: str):
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE TRANSFORMACIONES DE DATOS\n")
        f.write("Dataset: SIO-Carnes - Operaciones de Compra-Venta de Ganado Vacuno\n")
        f.write("="*60 + "\n\n")
        
        f.write("RESUMEN EJECUTIVO\n")
        f.write("-"*20 + "\n")
        f.write(f"Registros procesados: {resumen['registros_originales']}\n")
        f.write(f"Registros finales: {resumen['registros_finales']}\n")
        f.write(f"Tasa de retención: {resumen['porcentaje_retenido']}%\n")
        f.write(f"Columnas agregadas: {resumen['columnas_agregadas']}\n\n")
        
        f.write("TRANSFORMACIONES APLICADAS\n")
        f.write("-"*30 + "\n")
        f.write("1. Eliminación de columnas con >90% valores faltantes\n")
        f.write("2. Tratamiento de valores faltantes en columnas críticas\n")
        f.write("3. Eliminación de registros duplicados\n")
        f.write("4. Detección y eliminación de outliers (método IQR)\n")
        f.write("5. Discretización de variables continuas\n")
        f.write("6. Creación de variables derivadas\n")
        f.write("7. Normalización de valores categóricos\n\n")
        
        f.write("RESULTADO\n")
        f.write("-"*10 + "\n")
        f.write("Dataset limpio y preparado para análisis de reglas de asociación.\n")
        f.write("Variables discretizadas disponibles para análisis categórico.\n")
        f.write("Outliers tratados para mejorar calidad de patrones.\n")
    
    print(f"Reporte guardado en: {ruta_reporte}")

def main():
    ruta_datos = 'data/completo-ago20-ago21.csv'
    ruta_salida = 'data/datos_transformados.csv'
    ruta_reporte = 'analisis/transformaciones.txt'
    
    df_original = cargarDatos(ruta_datos)
    calidad_inicial = analizarCalidadDatos(df_original)
    
    df_transformado = df_original.copy()
    df_transformado = eliminarColumnasInutilizables(df_transformado)
    df_transformado = tratarValoresFaltantes(df_transformado)
    df_transformado = eliminarDuplicados(df_transformado)
    df_transformado = crearVariablesDerivadas(df_transformado)  # Mover antes para convertir tipos
    df_transformado = tratarOutliers(df_transformado)
    df_transformado = discretizarVariablesContinuas(df_transformado)
    df_transformado = normalizarValoresCategoricos(df_transformado)
    
    resumen = generarResumenTransformaciones(df_original, df_transformado)
    
    guardarDatosTransformados(df_transformado, ruta_salida)
    guardarReporteTransformaciones(resumen, ruta_reporte)
    
    print("\n" + "="*60)
    print("TRANSFORMACIONES COMPLETADAS EXITOSAMENTE")
    print("="*60)

if __name__ == "__main__":
    main()
