import cv2
import random
import sys

### ESTE ALGORITMO EFECTIVAMENTE SIGUE UN OBJETO; PERO NO SABEMOS COMO DECIRLE CUAL :V

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print("" + str(major_ver) + " | " + str(minor_ver) + " | " + str(subminor_ver))
if __name__ == '__main__':

    # Set up tracker.
    # Instead of MIL, you can also use
    #                0           1      2      3      4             5         6        7
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
    trackers = {
        'BOOSTING': cv2.TrackerBoosting_create(),
        'MIL': cv2.TrackerMIL_create(),
        'KCF': cv2.TrackerKCF_create(),
        'TLD': cv2.TrackerTLD_create(),
        'MEDIANFLOW': cv2.TrackerTLD_create(),
        'GOTURN': cv2.TrackerGOTURN_create(),
        'MOSSE': cv2.TrackerMOSSE_create(),
        'CSRT': cv2.TrackerCSRT_create()
    }

    # Read video
    video = cv2.VideoCapture("vtest.avi")

    # Exit if video not opened.
    if not video.isOpened():
        print
        "Could not open video"
        sys.exit()

    # Read first frame1.
    ok, frame1 = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box
    #bbox = (634, 236, 60, 96)

    # Initialize tracker with first frame1 and bounding box
    #ok = tracker.init(frame1, bbox)

    while True:
        # Read a new frame1
        _, frame1 = video.read()
        ok, frame2 = video.read()
        if not ok:
            break
        ####### Piece of code ################
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ######################################

        bbox_s = []
        bbox_s_counter = 0
        AREA_MAX = 1000
        for contour_index in range(len(contours)):
            bbox_item = cv2.boundingRect(contours[contour_index])
            tracker = trackers[tracker_type]
            ok = tracker.init(frame1, bbox_item)
            if cv2.contourArea(contours[contour_index]) < AREA_MAX:
                bbox_s.append([])
                continue
            bbox_s_counter += 1
            bbox_s.append([bbox_item, frame1, tracker])


        for contour_index in range(len(contours)):
            if cv2.contourArea(contours[contour_index]) < AREA_MAX:
                continue
            # Start timer
            timer = cv2.getTickCount()
            bbox, frame1, tracker = bbox_s[contour_index]
            # Update tracker
            ok2, bbox = tracker.update(frame1)

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Draw bounding box
            if ok2:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                #cv2.rectangle(frame1, p1, p2, (255, 0, 0), 2, 1)
                cv2.rectangle(frame1, p1, p2, (random.randint(0, 255), random.randint(0, 255), random.randint(0,255)), 2, 1)
            else:
                # Tracking failure
                cv2.putText(frame1, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                new_tracker = trackers[tracker_type]
                new_tracker.init(frame1, cv2.boundingRect(contours[contour_index]))
                bbox_s[contour_index][1] = cv2.boundingRect(contours[contour_index])
                bbox_s[contour_index][2] = new_tracker

            # Display tracker type on frame1
            cv2.putText(frame1, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            # Display FPS on frame1
            cv2.putText(frame1, "FPS : " + str(int(fps)) + " | Personas:" + str(bbox_s_counter), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            # Display result
            cv2.imshow("Tracking", frame1)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27: break
