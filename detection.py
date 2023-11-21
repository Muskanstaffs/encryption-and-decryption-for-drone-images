import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8x.pt')

# Open the video file
video_path = "boat.mp4"
cap = cv2.VideoCapture(video_path)

# Get the original video frame dimensions
width = 400
height = 400

# Define the output video file and codec
output_path = "output_resized.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(output_path, fourcc, 30, (width, height))

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        for r in results:
            print(r.probs)

        # Save the annotated frame as an image with a unique filename
        cv2.imwrite("prediction.jpg", annotated_frame)

        # Resize the frame if needed
        resized_frame = cv2.resize(frame, (width, height))

        # Write the resized frame to the output video
        output_video.write(resized_frame)

        # Display the annotated frame
        cv2.imshow("Object detection", annotated_frame)

        # Automatically close after saving the image
        cv2.waitKey(1000)  # Wait for 1 second (1000 milliseconds)
        break
    else:
        break

# Release the video capture object and output video writer
cap.release()
output_video.release()

# Close all display windows
cv2.destroyAllWindows()

