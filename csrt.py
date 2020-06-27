from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
global a,b

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())


(major, minor) = cv2.__version__.split(".")[:2]

if int(major) == 3 and int(minor) < 3:
	tracker = cv2.Tracker_create(args["tracker"].upper())


else:

	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
	}


	tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

initBB = None
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)


else:
	vs = cv2.VideoCapture(args["video"])
fps = None

# loop over frames from the video stream
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame

	# check to see if we have reached the end of the stream
	if frame is None:
		break


	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]

	# check to see if we are currently tracking an object
	if initBB is not None:

		(success, box) = tracker.update(frame)
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
			print(str(x+w/2)+","+str(y+h/2))
		a=str(x+w/2)
		b=str(y+h/2)

		# update the FPS counter
		fps.update()
		fps.stop()




	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	if key == ord("s"):
		initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		tracker.init(frame, initBB)
		fps = FPS().start()


	elif key == ord("q"):
		break


if not args.get("video", False):
	vs.stop()


else:
	vs.release()

cv2.destroyAllWindows()