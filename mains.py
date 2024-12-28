import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*


# model=YOLO(r"headdataset\best(office).pt")
model = YOLO('yolov5n.pt')

area1=[(268, 472), (325, 467), (567, 583), (482, 593)]
area2=[(343, 474), (574, 578), (604, 534), (434, 442)]


cv2.namedWindow('RGB')
cap = cv2.VideoCapture(0)

# Read the class names for YOLO detections
my_file = open(r"coco.txt")
data = my_file.read()
class_list = data.split("\n")

count=0
people_entering={}
people_exiting={}
tracker = Tracker()
entering = set()
exiting = set()
n_p = 0


  
# Replace the below URL with your own IP provided by the IP WEBCAM APP.
# Make sure to add "/shot.jpg" at last.
# url = "http://192.168.1.79:8080/shot.jpg"
# url = "https://www.youtube.com/watch?v=J7iXt9fLI2U&ab_channel=KevinStratvert"
# video = pafy.new(url)
# best = video.getbest(preftype="mp4")

# cap = cv2.VideoCapture(best.url)
# cap = cv2.VideoCapture(0)
while True:    

    # img_resp = requests.get(url)
    # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    # img = cv2.VideoCapture(img_arr, -1)
    # img = imutils.resize(img, width=800, height=600)

    ret, frame = cap.read()
    if not ret:
        print("no ret")
        break
    if frame is None:
        print("Error: Received empty frame.")
        break
    frame=cv2.resize(frame,(1200,600))

    count += 1
    if count % 2 != 0:
        continue

    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    list = []
    conf_threshold = 0.5

    for index, row in px.iterrows():
        x1, y1, x2, y2, d = map(int, row[:5])
        c = class_list[d]
        if 'Head' in c:
            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            cv2.putText(frame, c, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(255, 255, 255), 2)
            list.append([x1, y1, x2, y2])

   
    bbox_id = tracker.update(list)
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox

        # Check for entering the first area (area1)
        results2 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
        if results2 >= 0 and id not in people_entering:
            people_entering[id] = (x4, y4)  # Mark as entering
            cv2.rectangle(frame, (x3, y3), (x4, y4), (255, 0, 0), 2) #draw blue

        # Check for entering the second area (area2)
        if id in people_entering:
            results3 = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
            if results3 >= 0 and id not in entering:  # Make sure it's only added once
                entering.add(id)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                cv2.circle(frame, (x4, y4), 4, (255, 0, 255), 1)
                cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        # Check for exiting the first area (area2)
        results = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
        if results >= 0 and id not in people_exiting:
            people_exiting[id] = (x4, y4)  # Mark as exiting
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2) # Draw a red rectangle around the person

        # Check for exiting the second area (area1)
        if id in people_exiting:
            results1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
            if results1 >= 0 and id not in exiting:  # Make sure it's only added once
                exiting.add(id)
                cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                # cv2.circle(frame, (x4, y4), 4, (255, 0, 255), 1)
                # cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

    cv2.polylines(frame, [np.array(area1, np.int32)], True, (255, 0, 0), 2)
    cv2.putText(frame, str('1'), (410, 531), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

    cv2.polylines(frame, [np.array(area2, np.int32)], True, (255, 0, 0), 2)
    cv2.putText(frame, str('2'), (466, 485), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

    # Initialize number if not already initialized
    if 'number' not in locals():
        number = 0
        
    if 'number1' not in locals():
        number1 = 0

    i = len(entering)
    o = len(exiting)

    if i:
        number += 1
    if o:
        number1 += 1

    # Display the number of people entering
    cv2.putText(frame, "Entering: " + str(i), (60, 80), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)

    # Display the number of people exiting
    cv2.putText(frame, "Exiting: " + str(o), (60, 140), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)

    # Display the total number of people
    # cv2.putText(frame, "No of people: " + str(number), (100, 200), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)


    # Display the frame with bounding boxes and count
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    

cap.release()
cv2.destroyAllWindows()

