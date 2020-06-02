import cv2
import numpy as np

#This is a project for Digital Image Processing (DIP) course at the Universidad de Antioquia.

#--------------------------------------------------------------------------
#------- Detección de movimiento y conteo de personas  ----------------------------------------------
#------- Conceptos básicos de PDI------------------------------------------
#------- Por: Alejandro Castaño Rojas  alejandro.castanor@udea.edu.co -----
#------- Por: Angélica Arroyave Mendoza angelica.arroyavem@udea.edu.co ----
#------- Curso Básico de Procesamiento de Digital de Imágenes -------------
#------- V0 Mayo de 2020--------------------------------------------------
#--------------------------------------------------------------------------

# DESCRIPCIÓN
# Este repositorio contiene la implementación de un blur gaussiano y el uso de morfología de 
# imágenes mediante la dilatación de estas usando la librería OpenCV 

# TECNOLOGÍAS
# Python 3
# OpenCV 3
# Numpy (python library)

#Uso de la libería OpenCv para capturar los fames del videp que se especifica como argumeto 
cap = cv2.VideoCapture('vtest.avi')
ret, frame1 = cap.read()
ret, frame2 = cap.read()

#Mientras el video funcione normalmente.
while cap.isOpened():
    # Calcularemos la diferencia absoluta entre el frame 1 y el frame 2 
    # para detectar los objetos en movimiento
    diff = cv2.absdiff(frame1, frame2) 
    # Pasamos el resultado a escala de grises
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # Cuando obtenemos la diferencia en escala de grises, aplicamos un blur Gaussiano
    # para suavizar las diferencias y poder notar únicamente las más abruptas
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Creamos un límite con los resultados del blur
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # Y con este aplicamos la dilatación para remarcar más aquellos movimientos notorios
    dilated = cv2.dilate(thresh, None, iterations=3)
    # Luego nos disponemos a encontrar los contornos de los objetos dilatados
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #Seteamos el contador de personas en 0 y empezamos a recorrer cada uno de los contornos
    person_counter = 0
    for contours in contours:
        # Durante el recorrido de los contornos, creamos un borde rectangular 
        # en cada uno de estos para poder dibujarlos mejor
        (x, y, width, height) = cv2.boundingRect(contours)

        # Vamos dibujar el área del contorno pero si el area es menor a 1000
        # no vamos a dibujar un rectangulo
        if cv2.contourArea(contours) < 1000:
            continue
        # Aumentamos el contador de personas dado que encontramos un contorno
        # que nos conviene
        person_counter += 1
        # Sacamos los momentos de los contornos encontrados, esto es con el fin de obtener el centroide
        # de las componentes X y Y de los contornos
        M = cv2.moments(contours)
        if (M["m00"] == 0): M["m00"] = 1  # Los momentos son una medida particular que indica la dispersión de una nube de puntos

        x_moment = int(M["m10"] / M["m00"])  #Aquí se obtiene el centroide para la componente x
        y_moment = int(M['m01'] / M['m00'])  # Aquí se obtiene el centroide de la componenye y
        # Dibujamos un circulo con los centroides encontrados
        cir = cv2.circle(frame1, (x_moment, y_moment), 7, (0, 0, 255), -1)
        #Seteamos la fuente para poner el texto en la pantalla de las coordenadas de cada contorno
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame1, '{},{}'.format(x, y), (x, y), font, 0.75, (255, 0, 255), 1, cv2.LINE_AA)

        # Dibujamos el rectangulo del cotorno
        cv2.rectangle(frame1, (x, y), (x + width, y + height), (255, 0, 0))
        # Escribimos en la parte superior izquierda si hay movimiento en el video
        cv2.putText(frame1, "Estado: {}".format("Movimiento"), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 218, 51), 3)
    # Escribimos en la parte superior izquierda si la cantidad de personas encontradas                
    cv2.putText(frame1, "Personas: {}".format(str(person_counter)), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 218, 51), 2)
    # Mostramos el frame 1
    cv2.imshow('Video', frame1)
    # e indicamos en cambio de frames
    frame1 = frame2
    ret, frame2 = cap.read()

    # En esta linea indica la velocidad del 
    # video y para cerrar la ventana cuando se oprima la tecla escape
    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
