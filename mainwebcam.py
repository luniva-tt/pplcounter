from ultralytics import solutions
import cv2
import numpy as np
import imutils
import requests
  
url = "http://192.168.1.79:8080/shot.jpg"
  
# Define region points
region_points = [(600,0), (600,600)] 

# Init ObjectCounter
counter = solutions.ObjectCounter(
    show=True,  # Display the output
    region=region_points,  # Pass region points
    model=r"D:\headdatset\yolov5n.pt",  # model="yolo11n-obb.pt" for object counting using YOLO11 OBB model.
    classes=[0],  # If you want to count specific classes i.e person and car with COCO pretrained model.
    show_in=True,  # Display in counts
    show_out=True,  # Display out counts
    # line_width=2,  # Adjust the line width for bounding boxes and text display
)

# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=800, height=600)

    img =cv2.resize(img,(1200,600))
    img = counter.count(img)

    cv2.imshow("Android Cam", img)
  
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()

