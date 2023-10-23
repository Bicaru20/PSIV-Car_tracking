from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2
import os 

path_file = os.path.join(os.path.dirname(os.path.dirname(
    __file__)),'video\\short.mp4')

config = {
    "show": True
}


def detect_with_background_subtraction(self, frame):
	output = frame.copy()

	# Apply background subtraction
	fg_mask = self.apply(frame)

	# Clean up the mask (optional)
	kernel = np.ones((5, 5), np.uint8)
	fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

	dilation_kernel = np.ones((8, 8), np.uint8)  # Adjust the kernel size as needed
	fg_mask = cv2.dilate(fg_mask, dilation_kernel)

	# Find contours in the foreground mask
	contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	centroids = []

	for contour in contours:
		x, y, w, h = cv2.boundingRect(contour)

		# Calculate centroid
		centroid_x = x + w // 2
		centroid_y = y + h // 2

		# Ensure the detected object is of a minimum size
		if w > 45 and h > 45:
			centroids.append((centroid_x, centroid_y))
			cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.circle(output, (centroid_x, centroid_y), 4, (0, 0, 255), -1)

	# Display the annotated frame
	if config["show"]:
		cv2.imshow("Background Subtraction", output)
		cv2.waitKey(0)

#TODO: Reduir el soroll de la imatge

def object_detection():
	stream = cv2.VideoCapture(path_file)
	fps = FPS().start()
	count = 0
	# initializing subtractor 
	fgbg = cv2.createBackgroundSubtractorMOG2()

	all_centroids = []
	while True:
		# grab the frame from the threaded video file stream
		(grabbed, frame) = stream.read()
		# if the frame was not grabbed, then we have reached the end
		# of the stream
		if not grabbed or count == 1000:
			break
		# resize the frame and convert it to grayscale (while still
		# retaining 3 channels)
		detect_with_background_subtraction(fgbg, frame)
	
		fps.update()
		count += 1

	
	return all_centroids


if __name__ == "__main__":
	object_detection()

