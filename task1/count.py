import cv2
import numpy as np

VIDEO = "count.mp4"


def get_color(roi):

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    red1 = cv2.inRange(hsv, (0,70,50), (10,255,255))
    red2 = cv2.inRange(hsv, (170,70,50), (180,255,255))

    red = cv2.countNonZero(red1) + cv2.countNonZero(red2)

    white = cv2.inRange(hsv,
                        (0,0,180),
                        (180,60,255))

    white = cv2.countNonZero(white)

    if red > white and red > 300:
        return "Red"

    elif white > red and white > 300:
        return "White"

    return None


def run_counter():

    cap = cv2.VideoCapture(VIDEO)

    if not cap.isOpened():
        print("Cannot open count.mp4")
        return

    subtractor = cv2.createBackgroundSubtractorMOG2()

    line_y = 300

    counted = []

    red_count = 0
    white_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        mask = subtractor.apply(frame)

        kernel = np.ones((5,5), np.uint8)

        mask = cv2.morphologyEx(mask,
                                cv2.MORPH_OPEN,
                                kernel)

        contours, _ = cv2.findContours(mask,
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        cv2.line(frame,
                 (0,line_y),
                 (frame.shape[1],line_y),
                 (255,0,0),
                 2)

        for cnt in contours:

            if cv2.contourArea(cnt) < 1200:
                continue

            x,y,w,h = cv2.boundingRect(cnt)

            cx = x + w//2
            cy = y + h//2

            roi = frame[y:y+h,x:x+w]

            color = get_color(roi)

            if color is None:
                continue

            cv2.rectangle(frame,
                          (x,y),
                          (x+w,y+h),
                          (0,255,0),
                          2)

            cv2.circle(frame,
                       (cx,cy),
                       4,
                       (0,0,255),
                       -1)

            cv2.putText(frame,
                        color,
                        (x,y-8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,255,255),
                        2)

            if abs(cy-line_y) < 5:

                if (cx,cy) not in counted:

                    counted.append((cx,cy))

                    if color=="Red":
                        red_count += 1
                    else:
                        white_count += 1

        total = red_count + white_count

        cv2.putText(frame,
                    f"Red : {red_count}",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,0,255),
                    2)

        cv2.putText(frame,
                    f"White : {white_count}",
                    (20,75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2)

        cv2.putText(frame,
                    f"Total : {total}",
                    (20,110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2)

        cv2.imshow("Counter", frame)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyWindow("Counter")
