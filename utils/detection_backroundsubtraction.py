from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2

# open a pointer to the video stream and start the FPS timer
stream = cv2.VideoCapture('C:/Users/Usuari/OneDrive/Universitat/4-1/PSIV/Tracker/output7.mp4')
fps = FPS().start()
count = 0
# initializing subtractor 
fgbg = cv2.createBackgroundSubtractorMOG2().apply()

while True:
	# grab the frame from the threaded video file stream
	(grabbed, frame) = stream.read()
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed or count == 100:
		break
	# resize the frame and convert it to grayscale (while still
	# retaining 3 channels)
	frame = imutils.resize(frame, width=450)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = np.dstack([frame, frame, frame])
	fgmask = fgbg.apply(frame) 
	cv2.putText(fgmask, "Slow Method", (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)	
	# show the frame and update the FPS counter
	cv2.imshow("Frame", fgmask)
	cv2.waitKey(0)
	fps.update()
	count += 1
	
cap = cv2.VideoCapture('video1.mp4') 


cap.release() 
cv2.destroyAllWindows()

