# TP-satelites
Trabajo Práctico del Workshop en técnicas en programación científica 2016


![Ejemplo de las observaciones del satelite Metop A (ASCAT)](whole_as.png "Ejemplo de las observaciones del satelite Metop A (ASCAT)")


#Satélites: altímetros y escaterómetros


Los satelites polares son de gran utilidad, miden variables que se utilizan en
meteorología y ciencias de la atmósfera entre otros. A bordo de los satelites
se instalan instrumentos como por ejemplo los altímetros de radar los cuales
miden altura de olas marinas (altura significativa de ola).
Otro instrumento es el escaterómetro el cual mide velocidad y dirección del viento.

Las observaciones de estos satelites se encuentan disponibles en servidores FTP
[por ejemplo](https://podaac.jpl.nasa.gov/announcements/2013-06-21\_MetOp-A\_ASCAT\_FTP\_and\_OPeNDAP\_Directory\_Change)


#Modelado del problema

Se pide desarollar un software que permita graficar las observaciones de uno o más
satelites a nivel global para un intevalo de tiempo dado por linea de comando.

El software deberia poder conectarse al FTP, descargar y decodifcar
las observaciones. Cada satelite tiene su formato particular.

Junto a la observacion, latitud y longitud se informa una medida del error de observacion, todos son valores numéricos. Se desea poder controlar hasta que error se graficará.

Como los satelites dejan de responder y todo el tiempo hay satelites
nuevos se pide que el sistema permita agregar y quitar satelites con el minimo impacto en el código.

Usar argparse para la linea de comando y datetine.

#Bonus track

Para ciertas aplicaciones donde no son necesarias de tantas
observaciones se utiliza la tecnica de apicar un promedio de vecinos
se pide implementar este algoritmo y que tambien sea flexible a nuevas tecnicas.

#Metodologia

Lo primero a realizar es un diagrama de clases y un diagrama de secuencias de
donde se muestran que mensajes se envian los objetos entre si, lo que permitirá
comenzar a entender el problema y a aclarar dudas. Una vez revisado con el docente el diagrama de clases
preliminar se pasa a la etapa de programación.
En paralelo se puede ir investigado, como bajar archivos de internet
como recorrer un directorio, como decodificar las observaciones, como graficar
un mapa.
