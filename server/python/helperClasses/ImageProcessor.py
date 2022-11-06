import base64
import cv2 as cv
import numpy as np

class ImageProcessor():
    def __init__(self):
        self.mask = np.zeros((4096,4096,3))

    def processMessage(self, message):
        img_binary = base64.b64decode(message)
        #jpg <- binary
        img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
        #raw image <- jpg
        img = cv.imdecode(img_jpg, cv.IMREAD_COLOR)

        height, width, _ = img.shape


        self.map = img[:int(height/2)][:] 
        self.originalFrame = img[int(height/2):][:] 

        for x in range(self.map.shape[0]):
            for y in range(self.map.shape[1]):
                # map the pixel from the original frame to the location in the mask
                if (self.map[x,y] != [0,0,0]).all():
                    # how the face mask was generated:
                    # faceMask[x,y,0] = (x - (x % 16)) / 16
                    # faceMask[x,y,1] = (x % 16)*16 + (y % 16)
                    # faceMask[x,y,2] = (y - (y % 16)) / 16
                    r = self.map[x,y,0]
                    g = self.map[x,y,1]
                    b = self.map[x,y,2]

                    # getting the location from the RGB value
                    maskX = int(r*16 + ((g-g%16)/16))
                    maskY = int(b*16 + g%16)

                    self.mask[maskX,maskY] = self.originalFrame[x,y,:]

    def displayMask(self):
        cv.imwrite("./test.png", self.mask)


if __name__ == '__main__':
    processor = ImageProcessor()

    img = cv.imread("./testingImg.jpg")
    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 65]
    man = cv.imencode('.jpg', img, encode_param)[1]
    b64Data = base64.b64encode(man.tobytes())

    processor.processMessage(b64Data)

    cv.imshow("Mask", processor.mask)
    cv.imshow("Map", processor.map)
    cv.imshow("OriginalFrame", processor.originalFrame)

    cv.waitKey(0)