import cv2,os
import datetime
from .segmentation import Segment
from .models import Log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = os.path.join(BASE_DIR, 'license')
imagesavepath = os.path.join(BASE_DIR, 'license\\img')
filename = 'savedImage.png'
colorimg = 'colorImg.png'

class VideoCamera(object):
	def __init__(self):
	    self.capWebcam = cv2.VideoCapture(0+ cv2.CAP_DSHOW)

	def __del__(self):
		self.capWebcam.release()

	def get_frame(self):
		lin_cascade = cv2.CascadeClassifier(os.path.join(filepath, 'haarcascade_russian_plate_number.xml'))
		# capWebcam = cv2.VideoCapture(
		# 	0 + cv2.CAP_DSHOW)  # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam
		if self.capWebcam.isOpened() == False:  # check if VideoCapture object was associated to webcam successfully
			print("error: capWebcam not accessed\n\n")  # if not, print error message to std out
			os.system("pause")  # pause until user presses a key so user can see error message
			return  # and exit function (which exits program)

		while cv2.waitKey(
				1) != 27 and self.capWebcam.isOpened():  # until the Esc key is pressed or webcam connection is lost
			ret, frame = self.capWebcam.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gus = cv2.GaussianBlur(gray, (5, 5), 0)
			# rete, thres = cv2.threshold(gus, 0, 150, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
			thres = cv2.adaptiveThreshold(gus, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

			license = lin_cascade.detectMultiScale(gus, 1.3, 5)
			for i, (x, y, w, h) in enumerate(license):
				cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
				roi_color = thres[y:y + h, x:x + w]
				roi = frame[y:y + h, x:x + w]
				r = 400.0 / roi_color.shape[1]
				dim = (400, int(roi_color.shape[0] * r))
				resized = cv2.resize(roi_color, dim, interpolation=cv2.INTER_AREA)

				os.chdir(imagesavepath)
				cv2.imwrite(colorimg, roi)
				cv2.imwrite(filename, roi_color)

				text = Segment.segmentation()
				saveLog(text)
				cv2.putText(frame, text, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
			ret, jpeg = cv2.imencode('.jpg', frame)
			return jpeg.tobytes()

def saveLog(req):
	if len(req) >4:
		# if Log.getTimeout() == 'None':
		lin = Log(numberplate=req)
		lin.save()
	else:
		pass

	return