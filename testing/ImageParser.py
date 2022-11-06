import cv2 as cv


class ImageParser():
    def __init__(self, files, isVideo, imgScaleDown = 25.0):
        self.isVideo = isVideo
        self.imgScaleDown = imgScaleDown
        if isVideo:
            self.videoFile = files
            self.vidcap = cv.VideoCapture(self.videoFile)
        else:
            self.imageFiles = files

    def getNextImage(self):
        if self.isVideo:
            success, img = self.vidcap.read()
            if success == False:
                return False, None
            outDim = (int(img.shape[1] / self.imgScaleDown), int(img.shape[0] / self.imgScaleDown))
            return (success, cv.resize(img, outDim, interpolation=cv.INTER_AREA))
        else:
            imgName = self.imageFiles.pop()
            img = cv.imread(imgName)
            outDim = (int(img.shape[1] / self.imgScaleDown), int(img.shape[0] / self.imgScaleDown))

            # if still has images it will return true, img else false, None
            return (self.imageFiles, cv.resize(img, outDim, interpolation=cv.INTER_AREA))
