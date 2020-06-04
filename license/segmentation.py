import cv2
import os
from keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = os.path.join(BASE_DIR, 'license')
imagesavepath = os.path.join(BASE_DIR, 'license\\img')
modelpath = os.path.join(filepath, 'license-character-rec.h5')
prediction_model = load_model(modelpath)
prediction_model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])


res = []
MIN_CONTOUR_AREA = 40
RESIZED_IMAGE_WIDTH = 100
RESIZED_IMAGE_HEIGHT = 100
filename = 'savedImage.png'
colorimg = 'colorImg.png'
segimg = 'seg.png'

letters = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O','P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z' ]
class Segment:

    def segmentation():
        pred= ""
        res = ""
        os.chdir(imagesavepath)
        color = cv2.imread(colorimg)
        limage = cv2.imread(filename)
        gray = cv2.cvtColor(limage, cv2.COLOR_BGR2GRAY)
        thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        ctrs, hiearchy = cv2.findContours(thres, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        for npaContour in sorted_ctrs:  # for each contour
            if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:  # if contour is big enough to consider
                [intX, intY, intW, intH] = cv2.boundingRect(npaContour)  # get and break out bounding rect
                if intH>1.2*intW :
                    imgROI = color[intY:intY + intH, intX:intX + intW]  # crop char out of threshold image
                    cv2.imwrite(segimg, imgROI)
                    img = image.load_img(segimg,color_mode = "grayscale", target_size=(RESIZED_IMAGE_WIDTH,RESIZED_IMAGE_HEIGHT))
                    img = image.img_to_array(img)
                    img = img/255
                    imgROIResized = np.array(img).reshape(-1,RESIZED_IMAGE_WIDTH,RESIZED_IMAGE_WIDTH,1)
                    res = prediction_model.predict(imgROIResized)
                    res = np.array(res)
                    # print(res)
                    res = res.argmax()
                    # print(res)
                    res = letters[res]
                    pred = pred+str(res)
                    # print(pred)
                    cv2.rectangle(color,  # draw rectangle on original training image
                                  (intX, intY),  # upper left corner
                                  (intX + intW, intY + intH),  # lower right corner
                                  (0, 0, 255),  # red
                                  1)  # thickness
                    # cv2.imshow("imgROIResized", color)
                    # cv2.waitKey(0)
        return pred

    def test():
        pred =[]
        imagesavepath = os.path.join(BASE_DIR, 'trainDataset\\A')
        os.chdir(imagesavepath)
        filename = 'img011-00309.png'
        limage = image.load_img(filename,color_mode = "grayscale", target_size=(RESIZED_IMAGE_WIDTH,RESIZED_IMAGE_WIDTH))
        img = image.img_to_array(limage)
        img = img / 255
        imgROIResized = np.array(img).reshape(-1, RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_WIDTH, 1)
        res = prediction_model.predict(imgROIResized)
        res = np.array(res)
        # res = res[0] + res[1] + res[2]
        # print(res)
        res = res.argmax()
        # print(res)
        res = letters[res]
        cv2.imshow("imgROIResized", limage)
        cv2.waitKey(0)
        return pred
if __name__ == "__main__":
    Segment.segmentation()