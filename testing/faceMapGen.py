import numpy as np
import cv2 as cv

def main():
    map = np.zeros((1024,1024,3), dtype=np.uint8)

    for x in range(1024):
        for y in range(1024):
            map[x,y,0] = (x - (x % 4)) / 4
            map[x,y,1] = 127
            map[x,y,2] = (y - (y % 4)) / 4


    cv.imwrite("./map.png", map)



if __name__ == "__main__":
    main()
