Maestría en Data Mining – UTN Regional Paraná
Materia: Data Mining
Docente: Cecilia Dómina

Contenidos:
    • Unidad 1: Introducción. Definición de Data Mining y etapas del proceso de descubrimiento de conocimiento. Métodos supervisados y no supervisados. Principales técnicas de DM. Aplicaciones en diferentes industrias
    • Unidad 2: Exploración de los Datos. Tipos de variables. Estadísticas descriptivas. Visualización de datos (histogramas, boxplots, scatter plots). Correlaciones. Calidad de datos (outliers, missing). 
    • Unidad 3: Preparación de los Datos. Agregación. Muestreo. Discretización. Transformaciones. Normalización. Variables dummy. Creación y selección de variables. Importancia de la preparación de datos. 
    • Unidad 4: Reglas de Asociación. Conceptos básicos: itemset, itemset frecuente, itemset máximo e itemset cerrado. Algoritmo APriori. Evaluación de los patrones de asociación. Medidas de evaluación.
    • Unidad 5: Análisis de asociación avanzado y análisis de Secuencias. Reglas de asociación multilevel. Reglas generalizadas. Reglas de asociación temporales. Definición de análisis de secuencias. Análisis generalizado de secuencias. Restricciones temporales al análisis de secuencias
    • Unidad 6: Modelos de Clasificación. Árboles de decisión. Clasificadores basados en reglas. 
Observación: Esta unidad se agregó porque en las otras materias no ven árboles, vecinos y bayes, y me pareció necesario que entiendan como trabajan las diferentes técnicas y la diferencia con las reglas

Forma de evaluación
    • Trabajo práctico grupal de 2 personas.
        ◦ El objetivo del trabajo práctico es aplicar los conocimientos teóricos vistos en la materia, principalmente la exploración y preparación de datos y la aplicación de reglas de asociación.
        ◦ La elección de los datos sobre los cuales trabajar queda librada a los alumnos, para que puedan trabajar sobre temáticas de su interés, pero deben ser apropiados para aplicar reglas de asociación. Es interesante que trabajen con datos de los que conozcan un poco el dominio.
        ◦ Entrega escrita y posterior coloquio.
    •  Examen escrito individual de carácter teórico.
    • La nota final de la materia consiste de:
    • 
    • la nota del TP, donde se evalúan los contenidos : procesamiento de datos, reglas obtenidas (calidad y variedad de los resultado + pruebas con diferentes parámetros y filtros), presentación del trabajo (ppt + exposiciones), y la participación en clase durante el cursado
    • y la nota del examen
    • la última cohorte consideré 75% TP y 25% examen pero podría cambiar de acuerdo al caso para que sea lo más justo posible




Trabajo Práctico Materia: Data Mining
El objetivo del trabajo práctico es aplicar los conocimientos teóricos vistos en la materia, principalmente la exploración y preparación de datos y la aplicación de reglas de asociación.
La elección de los datos sobre los cuales trabajar queda librada a los alumnos, para que puedan trabajar sobre temáticas de su interés, pero deben ser apropiados para aplicar reglas de asociación. Deben tener en cuenta que sea interesante ver patrones de coocurrencia entre los atributos, como los ejemplo citados en clase.
Es interesante que trabajen con datos de los que conozcan un poco el dominio, para poder aportar conocimiento en el procesamiento de los datos y analizar si tienen sentido los resultados obtenidos, o si son obvios. Y además para encontrarse con problemas de calidad de datos. Si no tuvieran un conjunto de datos con el cual trabajar pueden descargar de alguno de los repositorios existentes, por ejemplo:
https://www.kdnuggets.com/datasets/index.html
https://www.kaggle.com/datasets
https://data.buenosaires.gob.ar/
u otros

Se recomienda formar grupos de dos o tres personas. En lo posible con diferente formación/perfiles, para complementarse en la forma de trabajar y también que haya alguien con formación en sistemas o facilidad para manejar las herramientas de software que elijan.
Requerimientos sobre el data set a utilizar:
    • Los datos pueden estar en uno o más archivos / tablas de la base de datos (tendrían que bajarlos a texto). Si están en más de un archivo tienen que tener algún campo por el cual unirlos.
    • Volumen de datos, idealmente 10.000 registros o más.
    • Preferentemente 10 o más atributos. En lo posible que haya atributos numéricos y categóricos.
    • Los datos deben estar despersonalizados, no deben existir datos de contacto directo (nombre, apellido, dni, dirección exacta - si barrio o cp -, nro teléfono, pueden tener un ID). 
    • Puede ser que busquen resolver un problema de clasificación. Es decir que pueden tener especial interés en explicar un atributo (existente o a calcular) en función de los otros. Esto no es un requisito, al contrario, debiera ser interesante encontrar relaciones entre atributos cualesquiera, pero se permite también trabajar con datos que tengan alguna clasificación.

Sobre la presentación del TP 
5 a 10 diapositivas y 30 minutos de exposición por grupo 
Explicando: 
    • breve descripción de las características del data set y de lo que buscan analizar (una hipótesis de negocio)
    • procesamiento realizado sobre los datos (agrupamientos, discretizaciones, etc)
    • herramientas utilizadas
    • problemas y desafíos encontrados
    • reglas obtenidas, formas de selección/evaluación
    • presentación de 3 a 5 reglas interesantes y su aplicación al problema de negocio que intentaron resolver (o alguna otra cosa que haya surgido en el proceso)
Los TP se van trabajando desde la primera semana de cursado (y yo los voy guiando con eso), con lo cual hay mucho que ya resulta obvio al momento de la exposición y no hace falta explicar. Particularmente en estos casos que rendirían libres se pueden extender un poco más, pero la idea siempre es que sea un resumen ejecutivo/técnico (no un cuento chino)
