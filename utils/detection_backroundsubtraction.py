from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2
import os 

path_file = os.path.join(os.path.dirname(os.path.dirname(
    __file__)),'video\\output7.mp4')

config = {
    "show": True
}

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
		frame = imutils.resize(frame, width=450)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame = np.dstack([frame, frame, frame])
		fgmask = fgbg.apply(frame) 
		cnts, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
		cnts = [c for c in cnts if cv2.contourArea(c) > 500]
		centroids = []
		for c in cnts:
			(x, y, w, h) = cv2.boundingRect(c)
			centroid_x = x + w // 2
			centroid_y = y + h // 2
			centroids.append((centroid_x, centroid_y))
			
			cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
			cv2.circle(frame, (centroid_x, centroid_y), 4, (0, 0, 255), -1)
		
		if config["show"]:
			cv2.imshow("Frame", frame)
			cv2.waitKey(0)

		if centroids != []:
			all_centroids.append((centroids, centroids))
	
		fps.update()
		count += 1

	
	return all_centroids


if __name__ == "__main__":
	object_detection()

