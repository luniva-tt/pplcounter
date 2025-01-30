import cv2
import json 
import sys

# Initialize a list to store the clicked coordinates
coordinates = []

# Mouse callback function to capture clicked coordinates
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates.append((x, y))  # Append the coordinates of the click
        # print(f"Clicked at: ({x}, {y})")  # Print the coordinates on the console
        # Draw a circle on the clicked point to visualize the click
        cv2.circle(param, (x, y), 5, (0, 255, 0), -1)  # Update the frame with the circle

if len(sys.argv) > 1:  # Check if a feed argument was passed
    feed = sys.argv[1]
    print("argg recieved", int(feed))
    cap = cv2.VideoCapture(int(feed))  # Use the feed from the argument
else:
    cap = cv2.VideoCapture(0)
     

# Open the video file
# cap = cv2.VideoCapture(0)

# Display the first frame to create the window
ret, frame = cap.read()
if not ret:
    # print(feed)
    print("Failed to open video")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Create the window before setting the callback
cv2.imshow('Video', frame)

# Set the mouse callback function for the window
cv2.setMouseCallback('Video', click_event, param=frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1200, 600))
    
    # Display the frame and update the window with the circles
    cv2.imshow('Video', frame)

    # Wait until the user clicks 4 times
    # if len(coordinates) == 4:
    #     print(f"Coordinates: {coordinates}")
    #     break
    if len(coordinates) == 2:
        print(json.dumps(coordinates))  # Send coordinates as JSON string
        break

    # Wait for key press to proceed to the next frame
    if cv2.waitKey(3) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the video capture object and close any open windows
cap.release()
cv2.destroyAllWindows()
