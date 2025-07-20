Necesito realiar un análisis de mineria de datos, cumpliendo con los siguientes requisitos:

- El objetivo del trabajo práctico es aplicar los conocimientos teóricos de minería de datos, principalmente la exploración y preparación de datos y la aplicación de reglas de asociación.
- Los productos que se requieren para la presentación son: 
    - archivo txt 'analisis/analisis_exploratorio.txt' con análisis exploratorio de datos informando características del dataset, variables, distribuciones, anomalias, etc. 
    - archivo txt 'analisis/transformaciones.txt' con transformaciones realizadas sobre los datos, como discretizaciones, normalizaciones, etc. a fin de disponer de un dataset limpio y preparado para el análisis.
    - archivo txt 'analisis/reglas_asociacion.txt' con reglas de asociación obtenidas, con sus respectivas métricas de soporte, confianza, lift, etc.
    - presentación en formato markdown 'analisis/presentacion.md' con 10 diapositivas explicando todo el proceso realizado, incluyendo 
        • breve descripción de las características del data set y de lo que buscan analizar (una hipótesis de negocio), con pruebas realizadas y gráficos que lo respalden.
        • procesamiento realizado sobre los datos (agrupamientos, discretizaciones, etc), y gráficos que lo respalden.
        • herramientas utilizadas
        • problemas y desafíos encontrados
        • reglas obtenidas, formas de selección/evaluación
        • presentación de 3 a 5 reglas interesantes y su aplicación al problema de negocio que intentaron resolver (o alguna otra cosa que haya surgido en el proceso)
- Puedes usar como introducción al problema y contexto de datos el analisis realizado por un equipo junior del dataset que estamos trabajando, pero dicho análisis NUNCA DEBE SER MENCIONADO, ni repetido, ni sus conclusiones reproducidas. Solo debe servir para contextualizar el problema y el dataset.  Dicho análisis está disponible en 'documents/analisis_conclusiones_equipo_junior.md'. 

Sobre el dataset:
    - El dataset está en 'data/completo-ago20-ago21.csv'.

Sobre los scripts:
    - El dataset ha analizar es un dataset grande, por lo que debes crear código robusto para su optimo procesamiento.
    - Cada documento debe tener asociado un script en python que lo genere, y se deben imprimier los resultdos por consola así se puede verificar el proceso.
    - Los scripts deben tener comentarios que expliquen lo que hacen utilizando un estilo minimalista, sin iconos, elementos gráficos o expresiones. Deben ser neutrales, sin personalización.
    - Las funciones deben tener notación camelCase, como por ejemplo: "def analisisExploratorio(df: pd.DataFrame) -> pd.DataFrame:"
    - Los scripts deben ser ejecutables de principio a fin, y deben tener un nombre que indique el tipo de análisis que realizan, como por ejemplo: "src/analisis_exploratorio.py", "src/transformaciones.py", "src/reglas_asociacion.py", "src/presentacion.md".

