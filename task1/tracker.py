import cv2
VIDEO = "c:/Users/deeks/OneDrive/Desktop/opencv/task1/tracker.mp4"

def run_tracker():

    cap = cv2.VideoCapture(VIDEO)
    if not cap.isOpened():
        print("Cannot open tracker.mp4")
        return

    ret, frame = cap.read()
    if not ret:
        return

    print("Select the GREY car and press ENTER.")
    bbox = cv2.selectROI("Select Car", frame, False)
    cv2.destroyWindow("Select Car")

    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, bbox)
    while True:

        ret, frame = cap.read()
        if not ret:
            break

        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            cx = x + w // 2
            cy = y + h // 2
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, "Grey Car", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("Tracker", frame)
        if cv2.waitKey(25) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyWindow("Tracker")

if __name__ == "__main__":
    run_tracker()
