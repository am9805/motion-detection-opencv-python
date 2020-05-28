import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.avi')
# cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

persons = []


def addPerson(x_arg, y_arg):
    personToPush = (x_arg, y_arg)
    if (len(persons) == 0):
        persons.append(personToPush)
    print(personToPush)
    # else:
    #   for i in range(len(persons)):
    #     # if abs(x - x_arg) > 5 and abs(y - y_arg) > 5:


while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contours in contours:
        (x, y, width, height) = cv2.boundingRect(contours)

        addPerson(x, y)

        # Vamos ahalalr el área del contorno y si el area es menor a
        # no vamos a dibujar un rectangulo, si no, si
        if cv2.contourArea(contours) < 1000:
            continue

        M = cv2.moments(contours)
        if (M["m00"] == 0): M["m00"] = 1
        # Los momentos son una medida particular que indica la dispersión de una nube de puntos

        x_moment = int(
            M["m10"] / M["m00"])  # Getting the x coordinate, aqui se obtiene el centroide para la componente x
        y_moment = int(M['m01'] / M['m00'])  # Aqui se obtiene el centroide de la componenye y
        cir = cv2.circle(frame1, (x_moment, y_moment), 7, (0, 0, 255), -1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame1, '{},{}'.format(x, y), (x, y), font, 0.75, (255, 0, 255), 1, cv2.LINE_AA)
        # nuevoContorno = cv2.convexHull(contours)
        # cv2.drawContours(frame1, [nuevoContorno], 0, (255,0,0), 3) #Drawing the found contours

        cv2.rectangle(frame1, (x, y), (x + width, y + height), (255, 0, 0))
        cv2.putText(frame1, "Estado:{}".format("Movimiento"), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 218, 51), 3)
        # cv2.putText(frame1, str(personsCounter), (10,60),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 218, 51), 3 )

    # cv2.drawContours(frame1, contours, -1, (0,255,0), 2)
    cv2.imshow('blur', blur)
    cv2.imshow('thresh', thresh)
    cv2.imshow('Video', frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
