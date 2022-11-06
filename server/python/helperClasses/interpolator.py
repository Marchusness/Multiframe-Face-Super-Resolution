
import numpy as np


class Interpolator():
    def nearestNeighbor(image):
        def nearestPixel(y,x,maxY,maxX):
            for d in range(20):
                for i in range(-d,d+1):
                    if x+i < maxX and x+i >= 0:
                        if y-d >= 0:
                            numPixelsBottom = image[y-d][x+i][1]
                            if numPixelsBottom > 0:
                                return image[y-d][x+i][0]

                        if y+d < maxY:
                            numPixelsTop = image[y+d][x+i][1]
                            if numPixelsTop > 0:
                                return image[y+d][x+i][0]

                for i in range(-d+1,d):
                    if y+i < maxY and y+i >= 0:
                        if x-d >= 0:
                            numPixelsLeft = image[y+i][x-d][1]
                            if numPixelsLeft > 0:
                                return image[y+i][x-d][0]
                        
                        if x + d < maxX:
                            numPixelsRight = image[y+i][x+d][1]
                            if numPixelsRight > 0:
                                return image[y+i][x+d][0]

            return [0,0,0]

        height, width, _ = image.shape
        if image == None:
            return
        img = np.zeros([height,width,3],dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                img[i][j] = nearestPixel(i,j, height, width)
        return img
