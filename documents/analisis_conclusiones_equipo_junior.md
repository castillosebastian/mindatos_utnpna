
Aplicación de técnicas de Minería de Datos a Operaciones de Compra-Venta de Ganado Vacuno con Destino a Faena


Shai Bejar - Sergio Civico


Minería de Datos, U.T.N. Facultad Regional Paraná, Av. Almafuerte 1033, (E3102SLK)
Paraná, Entre Ríos

Resumen: El presente trabajo propone una primera investigación y análisis inicial del procedimiento de Minería de Datos (MD), principalmente la exploración y preparación de datos y la aplicación de reglas de asociación para el conjunto de datos extraídos de la base pública https://datos.gob.ar/dataset denominado “Sio-Carnes”, Sistema unificado de información de operaciones de compra venta de ganado con destino a faena. El informe comienza con una breve introducción de la información a procesar, luego un detalle de la metodología utilizada a lo largo del desarrollo de aplicación de las técnicas de Minería de Datos para exploración y procesamiento. Finalmente, con el conjunto resultante de datos transaccionales obtenido a partir de los pasos previos, se implementan diferentes algoritmos que permiten hallar los itemsets frecuentes y sus potenciales reglas de asociación en base a parámetros predefinidos. Por último, se proponen una serie de conclusiones y trabajo a futuro.

Palabras clave: Minería de datos, faena, ganado vacuno, operaciones, compra-venta

Introducción
Se consultó en primera instancia una fuente de información confiable con gran cantidad de datos de público acceso, en este sentido la fuente de información nacional https://datos.gob.ar/dataset provee de datasets generados por organismos de gobierno de Argentina. En total el sitio contiene 1050 datasets.
Para el presente trabajo, se tomó en consideración la base del sistema Sio Carnes que contiene información de operaciones de compra venta de ganado bovino (y porcino) con destino a faena y surge de los datos obtenidos de las liquidaciones electrónicas presentadas a la AFIP junto con los Documentos de Tránsito Electrónicos (DTe) obtenidos del SENASA.
Este dataset contiene los siguientes atributos:
Fecha: corresponde al día en el que se realizó la operación.
Origen: Provincia y Localidad.
Destino: dividido en 10 zonas
Raza: según declarado en liquidación de AFIP
Cabezas: cantidad de cabezas comercializadas.
Categoría: según resolución 32/2018.
Precio: valor de la operación según la unidad de medida.
Cantidad: en unidades de cabezas o kilogramos.
Unidades de Medida: cabezas, kilogramos vivos.
En cuanto al primer paso del proceso de Minería de Datos (MD) que consiste en la recolección de información y definición del ámbito del problema, se decide adoptar una metodología por fases, que será desarrollada en el siguiente punto. En síntesis, la base de datos original que se utilizó como punto de partida del análisis contiene más de un 1.800.000 datos, y se corresponde a un periodo entre Agosto 2020 y Agosto 2021. Mientras que, la base de test utilizada a lo largo de todo el trabajo fue del 10% de la original conteniendo aproximadamente 190.000 datos. A partir de este conjunto de datos se intentará determinar, durante el desarrollo del presente trabajo, el análisis y descubrimiento de patrones mediante reglas de asociación en función de la teoría revisada a lo largo de la asignatura.
Realizando un primer análisis de la base de datos original, es posible observar una serie de relaciones interesantes entre los atributos de la BD. Con el fin de aumentar el nivel de detalle, a continuación se muestran las Zonas referenciadas en el modelo de la BD:
Zona 1: Buenos Aires y CABA
Zona 2: Buenos Aires Norte
Zona 3: Buenos Aires Centro
Zona 4: Buenos Aires Sur
Zona 5: Entre Ríos, Santa Fe y Córdoba
Zona 6: La Pampa y San Luis
Zona 7: Chubut, Neuquen, Río Negro, Santa Cruz, Tierra del Fuego
Zona 8: La Rioja, San Juan y Mendoza
Zona 9: Misiones, Corrientes, Formosa y Chaco
Zona 10: Jujuy, Salta, Santiago del Estero, Tucuman y Catamarca

Figura 1: Zonas delimitadas según compra-venta ganado con destino a faena (SIO Carnes).





Metodología
Se aplicó una metodología sistemática, desarrollando cada uno de los pasos de análisis estudiados a lo largo de la asignatura. En este apartado se hará especial hincapié en la selección, limpieza y tratamiento de los datos originales, su procesamiento, posterior aplicación de algoritmos para la búsqueda de patrones mediante reglas de asociación, para finalmente extraer nuevo conocimiento o confirmar relaciones existentes .
Los datos identificados como el historial de compras y ventas de ganado vacuno con destino a faena se obtuvieron aplicando un método de data scraping para lograr una base consolidada y referencial al conjunto de datos procesados de manera de obtener un año completo de información. Sin embargo, en una primera etapa de análisis, se procedió a la descarga de la BD en bruto tal como ofrece el sitio web https://datos.gob.ar/dataset, con un conjunto limitado de 188.956 registros totales correspondientes a los meses de enero y febrero del 2021, para luego trabajar con la BD completa para un año desde el día 01/08/2020 hasta el día 01/08/2021, con un total de 1.721.218 registros totales. 
Entonces, en una primera fase de análisis exploratorio, se utilizó una estructura de datos reducida, con un conjunto de datos cuyos atributos son los siguientes:
Tabla: Atributos iniciales para el dataset reducido

Las técnicas utilizadas para la preparación de los datos facilitaron la interpretación inicial de la información, la robustez de los datos y la capacidad de análisis del trabajo a posteriori.
Mediante herramientas de eliminación de valores nulos, discretización de variables continuas, identificación de transacciones temporales, entre otras, se obtuvieron algoritmos y pasos a seguir modelo para el preprocesamiento de los datos en la siguiente fase.
	2.1 Primera etapa: exploración
En primer lugar, se observaron los principales estadísticos para los datos de los atributos numéricos de la BD completa.






A simple vista se observan las grandes diferencias entre los valores mínimos y máximos de cada atributo, lo que determina de antemano una necesidad de procesamiento en este punto.
Luego, se determinaron la cantidad de datos faltantes de cada atributo, que deja en evidencia algún faltante de relevancia en los atributos “Precio Kg” y “Cantidad de Kg”.
Tabla: Atributos dataset y datos faltantes

Paso siguiente, se realizaron gráficos de “nube de palabras” e Histograma para el atributo “Raza”, con el fin de obtener el registro más frecuente.

Figura 2: Nube de palabras más frecuentes

Figura 3: Gráfico de barras horizontales para el atributo Raza.
De la misma forma se realizaron los gráficos para el atributo “Zona Destino”:
Figura 4: Gráfico de nube de palabras atributo Zonas

Figura 5: Histograma atributo Zonas.

Se observa que para el atributo “Raza” la variable más frecuente es el Bovino Criollo, y en el caso de la “Zona Destino” la variable más frecuente es la Zona 5.
Continuando con el análisis exploratorio, a partir de las siguientes figuras es posible observar que si agrupamos las Zonas por Cabezas Comercializadas, la que más transacciones obtuvo es la Zona 4. Por el contrario, si se agrupan las Zonas por el Total Vendido, aparecen más transacciones en la Zona 5.

Figura 6: gráfico de barras comparativo entre la agrupación de Zonas por Cabezas Comercializadas (a) y Total Vendido (b)

Finalmente, se realizó una breve inspección de los datos en función de la cantidad de outliers que presenta cada atributo continuo. Este paso se profundizará en el siguiente apartado donde se desarrolla la etapa de procesamiento.
2.2 Segunda etapa: preparación
Con los resultados del primer paso correspondiente a la exploración de los datos, comienza la etapa de preparación, dentro de la cual se procede a eliminar valores atípicos, agregar o eliminar datos faltantes, modificar nombres de columnas y agregar aquellas que se consideran relevantes al modelo.
Cabe aclarar que, a partir del trabajo previo realizado con la BD reducida, se realizaron las primeras depuraciones:
El atributo “Precio Cabeza” no es representativo del modelo puesto que contenía alrededor del 5% de datos sobre el total.
El atributo “Precio Kg” se transformó en variable tipo “float” puesto que al cargar el archivo en Colab aparecía como cadena, lo que impedía realizar ningún tipo de cálculo numérico para estos registros.
Se renombraron las columnas para aquellos atributos con nombres conteniendo espacio entre palabras.
A continuación, se realizó una investigación de la cantidad de datos nulos en las columnas, eliminando los registros con datos faltantes en las columnas Precio Kg y Cantidad Kg, correspondientes a transacciones relativas al atributo “Precio Cabeza” eliminado durante el primer paso.
Luego, se creó el atributo “Total Vendido” que corresponde a una cuenta entre dos atributos existentes, es decir a la multiplicación entre el Precio Kg y Cantidad Kg vendidos.
Al finalizar estos procesos, se obtuvo la siguiente tabla de datos:

En cuanto al tratamiento de las variables continuas, se realizó una secuencia de pasos para determinar y eliminar outliers:
Utilización de los estadísticos de cada una de las variables en cuestión resultantes de la etapa de exploración.
Gráfico boxplot para descubrimiento de outliers.

Figura 7: Gráfico explicativo de los parámetros que se incluyen en el Boxplot.
Cálculo de cuantiles y eliminación de outliers mediante las fórmulas de estadística descriptiva.
Retorno al paso ii) para verificar la existencia de outliers.
En el caso de verificar outliers en el paso iv) se procede a eliminarlos nuevamente.
Se repiten los pasos a partir del i) con la siguiente variable a evaluar.
A continuación se cita un ejemplo como caso de estudio de los pasos explicados en el apartado anterior. Atributo tipo continuo denominado “Precio Kg”:
i) Estadísticos
 
ii) Boxplot e Histograma
Figura 8: Boxplot e Histograma para el atributo “Precio Kg”
iii) Primera operación de cálculo de cuantiles y eliminación de outliers
Se observan 25.739 valores atípicos.

iv) Segunda operación Boxplot e Histograma

Figura 9: Boxplot e Histograma para el atributo “Precio Kg”.
v) Eliminación de outliers
Se observan 1.421 valores atípicos.
vi) Nuevos estadísticos para el atributo “Precio Kg”

En este punto es importante notar las diferencias presentadas entre los estadísticos del comienzo del proceso cíclico para eliminación de outliers y la tabla final.






Claramente los valores mínimos y máximos se aproximan una vez procesados los datos, lo que supone una composición más armónica del conjunto para continuar con la limpieza del siguiente atributo.
A su vez, si se representan los valores temporalmente agrupados por Mes para el atributo “Precio Kg”, se observa una diferencia sustancial en la distribución antes de aplicar la limpieza de outliers y después.

Figura 10: Gráfico de barras para el atributo “Precio Kg” por transacciones mensualizadas, antes de la limpieza de los datos.



Figura 11: Gráfico de barras para el atributo “Precio Kg” por transacciones mensualizadas, después de la limpieza de los datos.

En resumen, se eliminaron en total 27.160 registros entre la primera y segunda pasada  a partir del análisis de la variable “Precio Kg”. Luego, para el atributo “Cantidad Kg” durante la primera pasada se eliminaron 152.490, la segunda 85.236 y la tercera 46.515, totalizando 284.241 registros eliminados, considerando un remanente de outliers de 29.601 registros.
Finalmente para la variable continua “Cabezas Comercializadas” mediante el mismo análisis se observan aproximadamente 45.000 registros outliers a eliminar.
Es importante aclarar en este punto que para próximos análisis es conveniente apartar los datos outliers en un modelo y luego correr los algoritmos para descubrir patrones, y mantener el conjunto original con outliers y correr en paralelo los algoritmos para determinar reglas de asociación, para corroborar las posibles repercusiones de eliminar datos de la BD original y principalmente si se presentan modificaciones sustanciales en las conclusiones. Ahora bien, para los fines prácticos del presente trabajo, este procedimiento exhaustivo quedará abierto para futuras investigaciones. En síntesis, para trabajos futuros se deberá prestar especial atención en cuanto a la eliminación de la BD original de unos 350.000 registros outliers que representan más del 15% del conjunto total.
Otra instancia relevante al proceso de preparación de los datos es la Discretización de aquellas variables continuas, que por sus características deben modificarse para introducirlas luego a los modelos de búsqueda de patrones mediante reglas de asociación. Continuando con el ejemplo para el atributo “Precio Kg”, se utilizó la discretización que ofrece la librería sklearn denominada KBinsDiscretizer. Así, se obtienen rangos con distribución uniforme, a partir de la cual se sugiere una serie de rangos que discretizan los valores continuos del atributo que se pueden observar en el gráfico siguiente.







Figura 12: Gráfico de barras sobre el atributo “Precio Kg” de los rangos discretizados.
Los rangos de los atributos discretizados obtenidos a partir de  la ejecución del KBinsDiscretizer son los que se detallan a continuación.
Cabezas Comercializadas → “CabComDisc”:
[1; 2.04; 3.08; 4.12; 5.16; 6.2; 7.24; 8.28; 9.32; 10.36; 11.4; 12.44; 13.48; 14.52; 15.56; 16.6; 17.64; 18.68; 19.72; 20.76; 21.8; 22.84; 23.88; 24.92; 25.96; 27]
Cantidad de Kg → “CantKgDisc”:
[1.00000; 764.2; 1.527,4; 2.290,6; 3.053,8; 3.817; 4.580,2; 5.343,4; 6.106,6; 6.869,8; 7.633; 8.396,2; 9.159,4; 9.922,6; 10.685,8; 11.449; 12.212,2; 12.975,4; 13.738,6; 14.501,8; 15.265]
Precio Kg → “precioKgDisc”:
[16,25; 54,25; 92,25; 130,25; 168,25; 206,25]
Al finalizar el ciclo de preparación de la información previo a la aplicación de algoritmos para las técnicas conocidas como reglas de asociación entre los atributos del modelo, se resume el contenido del último dataset:

Como último paso de este procedimiento de exploración y preparación del dataset, se exportan los datos en un nuevo archivo de extensión .CSV con el fin de mantener un ordenamiento en las etapas subsiguientes.
3. Tercera etapa: modelos para la construcción de patrones
Si bien en los pasos previos se realizó la exploración y el procesamiento de los datos, al comenzar con la implementación de los algoritmos y la generación de itemsets frecuentes, se considera la discretización de los atributos agregando una leyenda adicional al nombre del rango para identificar adecuadamente a qué columna hace referencia. Esto es:

A posterior, se seleccionan únicamente aquellos atributos que forman parte del análisis deseado, y corresponden a las variables categóricas existentes en el modelo y procesadas.

A continuación, se construyó el array entre los atributos categóricos que fueron planteados como objetivos iniciales para la evaluación y búsqueda de patrones: {Zona Destino; Raza; Categoría; CabComDisc; precioKgDisc; cantKgDisc}.
Al momento de corroborar los nombres de las columnas del array (transformado a Data Frame), se observa una columna de valores nulos que se procede a eliminar.
Con el fin de visualizar los ítems más frecuentes, se utilizó un gráfico de barras horizontales.

Figura 13: Gráfico de barras horizontales de ítems más populares del array.

Así, se observan variables categóricas presentes en el array como el Precio por Kg entre 92.25 y 130.25 en primer lugar, la Zona 5 en segundo lugar y la Raza “Bovino Criollo” en tercer lugar.
Algoritmo Apriori
Se aplica el Algoritmo Apriori a partir del último array generado. En primer lugar se descubren los itemsets frecuentes con un soporte del 5%. Como resultaba lógico, a partir del gráfico de items más frecuentes, se observa en repetidas oportunidades el rango de PKG y la Zona 5.
En segundo lugar, las reglas de asociación para el algoritmo Apriori se aplicaron para un umbral de confianza del 50%, obteniendo los siguientes resultados ordenados según confianza:

Si se realiza un gráfico comparativo entre las diferentes medidas, se observa algún pico para la Convicción (verde), el Lift (celeste) y una punta poco pronunciada para la confianza.

Figura 14: Comparación entre los indicadores resultantes de las reglas de asociación.

Luego, un análisis adicional de reglas de asociación utilizando un umbral del Lift igual a uno, se obtiene una gran cantidad de reglas (60 aproximadamente). A continuación se citan las cinco más relevantes:

Algoritmo FP-Growth
Se implementó en segunda instancia la ejecución del algoritmo FP-Growth. En este caso se generó un array para insertarlo directamente como ItemsetList.
Para hallar los itemsets frecuentes se utilizaron los mismos umbrales para los indicadores soporte (5%) y confianza (50%), obteniendo las siguientes reglas de asociación:

FP-Growth con otras medidas (Lift)
Para profundizar el análisis de patrones y reglas de asociación, se intentó ejecutar un algoritmo basado en FP-Growth que permite utilizar el indicador Lift como parámetro adicional.
En este caso, previo a la ejecución del modelo se eliminaron los espacios existentes entre los nombres de los atributos y los espacios entre los valores de cada registro.
Para el análisis de Itemsets frecuentes se agrupó la Raza en función de la cantidad de Cabezas Comercializadas. De esta manera se obtienen las siguientes reglas de asociación, aunque de las más de 600 reglas sugeridas no se realizó ningún tipo de conclusión.

Algoritmo AprioriAll para relaciones secuenciales
Para generar la secuencia como una lista de listas de listas, se ejecutó el siguiente código:
sequences = [[a[1]['Raza'].tolist() for j in str(a[0][1])] for a in list(data.groupby([pd.Grouper(freq='W-MON'), pd.Grouper(freq='D')]))]

Esto produce una secuencia que representa las transacciones a partir de las razas comercializadas por día y por semana.
De todas formas, al intentar correr el algoritmo y luego de un tiempo de espera prolongado, no es posible ejecutarlo correctamente, por lo que se decide desestimar este análisis.

4. Análisis Temporal
Como análisis final del dataset, se aplicaron herramientas temporales con el fin de identificar asociaciones entre atributos que puedan presentar por ejemplo algún tipo de estacionalidad a lo largo del tiempo. En este sentido, se procede a indexar el atributo “Fecha Comprobante” que indica el día en el cual se realizó una determinada transacción, y mostrar las Razas comercializadas,  agrupadas por las diferentes Zonas, por cada fecha de transacción.
Para obtener un array acorde a lo que solicita el algoritmo Apriori se ejecuta el siguiente código:
transactions = [[a[0][1:2][0]] + a[1]['Raza'].tolist() for a in list(data.groupby([pd.Grouper(freq='D'), 'Zona Destino']))]
lo que arroja una lista de transacciones del tipo siguiente:
[['ZONA 10','Otra 99','Holando Argentino','Braford','ZONA 10',  'Brangus','Bovino Criollo','Flieckvieh Simmental'],...]
Los resultados del procesamiento de las transacciones anteriores se exponen a continuación: 

Figura 15: Gráfico de barras horizontales para los itemsets más frecuentes.

Finalmente, se aplican las reglas de asociación con un soporte del 5% y una Confianza del 95%, obteniendo las siguientes reglas:

Para tener un segundo análisis de la misma base temporal se aplicó el algoritmo FP-Growth con igual soporte (5%) y confianza (95%), obteniendo los siguientes resultados:

5. Conclusiones
En primer lugar, el origen de los datos consultados a partir del dataset obtenido del proyecto Sio-Carnes, si bien es un conjunto con abundante información, queda en evidencia que la calidad de los datos en bruto presentan algunas falencias que llevaron a la aplicación de estrategias resolutivas vistas durante el cursado de la asignatura. Por ejemplo, en el caso de la columna “Precio Cabeza”, la misma solo contaba con aproximadamente el 5% de sus datos completos, y como consecuencia se procedió a eliminarla del modelo de análisis.
A su vez, por falta de conocimiento del origen de estas falencias, es probable que la aplicación de las técnicas de eliminación y reemplazo de datos conlleve a un recorte importante del dataset original, perdiendo información valiosa en algunos casos. Ello, sin la posibilidad de consultar a un experto idóneo en la temática. A pesar del recorte producido para mejorar la calidad de los datos, fue posible utilizar el dataset resultante para la aplicación de las técnicas de minería de datos objetivo del presente estudio.
Cabe destacar que el dataset presenta por defecto un disposición transaccional, es decir que cada registro representa una transacción en particular, lo que facilitó el análisis y la aplicación del procedimiento de exploración, procesamiento y búsqueda de patrones.
	La búsqueda y construcción de patrones entre los atributos del dataset, se basaron en las potenciales relaciones entre las variables categóricas (Zonas Destino, Razas y Categorías) y los atributos numéricos previamente discretizados (Precio Kg, Cantidad Kg y Cabezas Comercializadas) a través de la aplicación de los algoritmos Apriori y FP-Growth. Para lograr una correcta aproximación a las reglas de asociación deseadas de manera tal que las mismas adquieran sentido dentro del ámbito del negocio, se manipularon los parámetros que propone el algoritmo, como el Soporte mínimo, Confianza y Lift.
Una de las reglas interesantes obtenidas a partir de la aplicación del algoritmo Apriori corresponde a {ZONA 1 B, PKG (92.25, 130.25]}  => {Bovino Criollo}, la cual identifica una relación de asociación entre la Zona de comercialización “Buenos Aires y CABA”, en un rango de precios por Kg entre 92.25 y 130.25 pesos, y la raza Bovino Criollo, que se comercializa mayormente en esta zona.
Otra relación de asociación importante es marcada por la regla {Holando Argentino} => {ZONA 5 B}, que evidencia la característica lechera de la raza Holando Argentino, al comercializarse fuertemente en la llamada Región Centro del país identificada como ZONA 5B en el dataset.
Si bien se observa otra regla con gran fuerza, en los resultados del algoritmo Apriori, la cual identifica la relación {CC (1.8, 2.6]} => {CKG (464.45, 927.9]}, representando la Cantidad de Cabezas Comercializadas  (en su forma discreta) y la Cantidad de Kg comercializados  (también, en su forma discreta), entendemos que se trata reglas que carecen de valor para el análisis, al tratarse de atributos correlacionados fuertemente de manera natural.
Al utilizar el indicador Lift con parámetro igual a uno, aparece la regla de asociación entre la Raza Aberdeen Angus y la Zona 3 B, con un Lift de 1.85 lo que supone una atracción positiva entre ambos ítems: {Aberdeen Angus} => {(ZONA 3 B)}.
Otra regla de asociación que resulta novedosa dentro del conjunto de reglas a partir del umbral del Lift igual a uno, corresponde a la aparición de una Categoría identificando su relación con una Raza según: {Bovino Vaca Regular (6 o más dientes)} => {Bovino Criollo}.
Mediante la interpretación de las reglas de asociación provistas por el algoritmo FP-Growth, se observan las mismas reglas de asociación con un umbral de soporte del 0.05 y confianza del 0.5, que para el caso anterior ejecutando el algoritmo Apriori, lo cual confirma la correlación entre los resultados de ambos algoritmos.
Finalmente, se analizó la relación de comercialización conjunta para determinadas Razas agrupadas por Fecha de transacción y Zona. Es decir, cada registro correspondiente a una transacción representa un conjunto de Razas asociadas por la misma Fecha y la misma Zona. En este escenario, al aplicar el algoritmo Apriori bajo un soporte mínimo de 0.05 para el cálculo de itemsets frecuentes y posterior búsqueda de reglas de asociación con una confianza del 0.95, se encuentran otras relaciones interesantes. Se destacan a continuación tres reglas con una confianza superior al 97%:
{Bovino Criollo, Hereford} => {Aberdeen Angus}
{Otra 99, Hereford} => {Aberdeen Angus}
{Bovino Criollo, Hereford, Otra 99} => {Aberdeen Angus}


Referencias
Datos Argentina. (s/f). Gob.ar. Recuperado el 25 de septiembre de 2021, de https://datos.gob.ar/
Maltagliatti, I. (2019). Sistema de Recomendacion de Artistas Musicales Mediante Minera de Reglas de Asociacion. 14.
Dómina, M. C. (2021, septiembre). Reglas de Asociación.
Wikipedia contributors. (s/f). Diagrama de caja. Wikipedia, The Free Encyclopedia. Recuperado el 25 de septiembre de 2021, de https://es.wikipedia.org/w/index.php?title=Diagrama_de_caja&oldid=138526402
Tan, P.-N., Steinbach, M., Karpatne, A., & Kumar, V. (2017). Introduction to Data Mining (2a ed.). Pearson.


