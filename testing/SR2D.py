import numpy as np
import cv2 as cv
from ImageParser import ImageParser
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 1

class SR2D():
    def __init__(self, files, isVideo):
        self.imgs = ImageParser(files, isVideo)

    def CombineAndScale(self, enlargement):
        self.enlargement = enlargement
        self.averageImage = None

        # is an matrix or arrays.
        # in the arrays will be all pixels
        self.combinedPixels = None

        success, img = self.imgs.getNextImage()

        outDim = (img.shape[1] * enlargement, img.shape[0] * enlargement)

        cv.imwrite("generatedImgs/firstImg.jpg", img)

        sift = cv.SIFT_create()

        imCount = 1
        self.averageImage = cv.resize(img, outDim, interpolation=cv.INTER_CUBIC)
        outkp, outdes = sift.detectAndCompute(self.averageImage, None)

        cv.imwrite("generatedImgs/initialAverageImage.jpg", self.averageImage)

        self.combinedPixels = np.array([[[None,0] for _ in range(outDim[0])] for _ in range(outDim[1])])


        while True:
            success, img = self.imgs.getNextImage()

            if not success:
                return

            # find the keypoints and descriptors with SIFT

            
            imgkp, imgdes = sift.detectAndCompute(img, None)
            
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks = 50)
            flann = cv.FlannBasedMatcher(index_params, search_params)
            # flann = matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)

            matches = flann.knnMatch(np.asarray(outdes,np.float32),np.asarray(imgdes,np.float32),2)

            # store all the good matches as per Lowe's ratio test.
            good = []
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)

            if len(good)>MIN_MATCH_COUNT:
                imCount += 1

                dstPts = np.float32([ outkp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
                srcPts = np.float32([ imgkp[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
                M, _ = cv.findHomography(srcPts, dstPts, cv.RANSAC,5.0)

                for rowIndex, row in enumerate(img):
                    for colIndex, pixel in enumerate(row):
                        x, y, w = np.dot(M, [colIndex, rowIndex, 1])
                        x = int(x/w + 0.5)
                        y = int(y/w + 0.5)
                        if x < 0 or y < 0:
                            continue
                        if x >= outDim[0] or y >= outDim[1]:
                            continue
                        if self.combinedPixels[y][x][1] == 0:
                            self.combinedPixels[y][x][0] = pixel
                        else:
                            alpha = 1.0/(self.combinedPixels[y][x][1] + 1) # new pixel value alpha 
                            beta = 1.0 - alpha # original value alpha
                            for rgb in range(3):
                                self.combinedPixels[y][x][0][rgb] = self.combinedPixels[y][x][0][rgb] * beta + pixel[rgb] * alpha # new pixel average 
                        self.combinedPixels[y][x][1] += 1
                
                w, h, _ = self.averageImage.shape
                aligned = cv.warpPerspective(img, M, (h,w))

                alpha = 1.0/(imCount + 1)
                beta = 1.0 - alpha
                self.averageImage = cv.addWeighted(aligned, alpha, self.averageImage, beta, 0.0)   
                if imCount > 50:
                    return 

    def getPixelRepresentation(self):
        return np.array([[ pixel[0] if pixel[1] > 0 else [0,0,0] for pixel in row] for row in self.combinedPixels])

    def getAverageImage(self):
        return self.averageImage

    def getNearestNeighborImage(self):
        height, width, _ = self.combinedPixels.shape
        if self.combinedPixels == None:
            return
        img = np.zeros([height,width,3],dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                img[i][j] = self.nearestPixel(i,j, height, width)
        return img

    def nearestPixel(self,y,x,maxY,maxX):
        avgPixel = [0,0,0]
        numPixels = 0
        for d in range(20):
            for i in range(-d,d+1):
                if x+i < maxX and x+i >= 0:
                    if y-d >= 0:
                        numPixelsBottom = self.combinedPixels[y-d][x+i][1]
                        if numPixelsBottom > 0:
                            return self.combinedPixels[y-d][x+i][0]

                    if y+d < maxY:
                        numPixelsTop = self.combinedPixels[y+d][x+i][1]
                        if numPixelsTop > 0:
                            return self.combinedPixels[y+d][x+i][0]

            for i in range(-d+1,d):
                if y+i < maxY and y+i >= 0:
                    if x-d >= 0:
                        numPixelsLeft = self.combinedPixels[y+i][x-d][1]
                        if numPixelsLeft > 0:
                            return self.combinedPixels[y+i][x-d][0]
                    
                    if x + d < maxX:
                        numPixelsRight = self.combinedPixels[y+i][x+d][1]
                        if numPixelsRight > 0:
                            return self.combinedPixels[y+i][x+d][0]

            if numPixels > 0:
                return avgPixel

        return [0,0,0]
    
    def bilinearPixelImage(self, distCenter = 8):
        height, width, _ = self.combinedPixels.shape
        if self.combinedPixels == None:
            return
        img = np.zeros([height,width,3],dtype=np.uint8)
        checkLocations = [[0,0]]
        for i in range(distCenter):
            checkLocations.append([i,0])
            checkLocations.append([-i,0])
            checkLocations.append([0,i])
            checkLocations.append([0,-i])
        for i in range(height):
            for j in range(width):
                img[i][j] = self.bilinearPixel(i,j, height, width, checkLocations)
        return img

    def bilinearPixel(self,y,x,maxY,maxX, checkLocations):
        avgPixel = np.array([0,0,0])
        numPixels = 0

        for dy, dx in checkLocations:
            if y + dy < 0 or y + dy >= maxY or x + dx < 0 or x + dx >= maxX:
                continue
            numPixelsLocation = self.combinedPixels[y + dy][x + dx][1]
            if numPixelsLocation > 0:
                numPixels += numPixelsLocation

        for dy, dx in checkLocations:
            if y + dy < 0 or y + dy >= maxY or x + dx < 0 or x + dx >= maxX:
                continue
            numPixelsLocation = self.combinedPixels[y + dy][x + dx][1]
            if numPixelsLocation > 0:
                alpha = numPixelsLocation/numPixels # amount contribution
                avgPixel = avgPixel + np.array(self.combinedPixels[y + dy][x + dx][0]) * alpha # new pixel average 
        
        return avgPixel

    def bicubicPixelImage(self, distCenter = 8):
        height, width, _ = self.combinedPixels.shape
        if self.combinedPixels == None:
            return
        img = np.zeros([height,width,3],dtype=np.uint8)
        locationWeighting = [[0,0,2]]
        for dist in range(1,distCenter):
            for i in range(1-dist, dist+1):
                locationWeighting.append([dist,-i,1/dist])
                locationWeighting.append([-dist,i,1/dist])
                locationWeighting.append([i, dist,1/dist])
                locationWeighting.append([-i, -dist,1/dist])
        for i in range(height):
            for j in range(width):
                img[i][j] = self.bicubicPixel(i,j, height, width, locationWeighting)
        return img

    def bicubicPixel(self,y,x,maxY,maxX,locationWeighting):
        avgPixel = np.array([0,0,0])
        numPixels = 0

        for dy, dx, w in locationWeighting:
            if y + dy < 0 or y + dy >= maxY or x + dx < 0 or x + dx >= maxX:
                continue
            numPixelsLocation = self.combinedPixels[y + dy][x + dx][1] * w
            if numPixelsLocation > 0:
                numPixels += numPixelsLocation

        for dy, dx, w in locationWeighting:
            if y + dy < 0 or y + dy >= maxY or x + dx < 0 or x + dx >= maxX:
                continue
            numPixelsLocation = self.combinedPixels[y + dy][x + dx][1] * w
            if numPixelsLocation > 0:
                alpha = numPixelsLocation/(numPixels) # new pixel value alpha 
                avgPixel = avgPixel + np.array(self.combinedPixels[y + dy][x + dx][0]) * alpha # new pixel average 
        
        return avgPixel
        


        