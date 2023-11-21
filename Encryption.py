import yagmail
from Crypto.Cipher import DES3
import os
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8x.pt')

# Open the video
video_path = "boat.mp4"
cap = cv2.VideoCapture(video_path)

# Get the original video frame dimensions
new_width = 200
new_height = 200

# Define the output video file and codec
output_path = "output_resized.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(output_path, fourcc, 30, (new_width, new_height))

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
        resized_frame = cv2.resize(frame, (new_width, new_height))

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

# Input file path
file_path = "prediction.jpg"

# Generate a random 16-byte key for Triple DES
tdes_key = os.urandom(16)

# Save the randomly generated key to a file
with open('random_key.bin', 'wb') as key_file:
    key_file.write(tdes_key)

# Initialize Triple DES cipher with the random key in MODE_EAX for Confidentiality & Authentication
# and nonce for generating a random/pseudo-random number used for authentication
cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

# Open and read the file from the given path
with open(file_path, 'rb') as input_file:
    file_bytes = input_file.read()

# Perform Encryption operation
new_file_bytes = cipher.encrypt(file_bytes)

# Write the encrypted data to a new file
encrypted_file_path = "Encrypted_image" + file_path
with open(encrypted_file_path, 'wb') as output_file:
    output_file.write(new_file_bytes)

print('Encryption Done!')

# Set up Yagmail to send the email
yag = yagmail.SMTP('deepmachine748@gmail.com', 'prtndxpwmblbfemo')

# Compose the email
subject = "Encrypted Image and Private Key"
contents = ["Please find the encrypted image and the private key attached."]

# Attach the encrypted image and the private key
attachments = [encrypted_file_path, 'random_key.bin']

# Send the email
yag.send('muskankhosla1997@gmail.com', subject, contents, attachments)

print('Email Sent!')
