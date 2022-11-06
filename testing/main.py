import cv2 as cv

from SR2D import SR2D

imgProcessor = SR2D("input.mov", True)

# imgProcessor.imgs.getNextImage()

imgProcessor.CombineAndScale(8)

imageRep = imgProcessor.getPixelRepresentation()

cv.imwrite('./imageRep.jpg', imageRep)


averageImage = imgProcessor.getAverageImage()

# cv.imshow('averageImage', averageImage)

cv.imwrite('./averageImage.jpg', averageImage)



# nearestNeighbor = imgProcessor.getNearestNeighborImage()

# # cv.imshow('nearestNeighbor', nearestNeighbor)

# cv.imwrite('generatedImgs/nearestNeighbor.jpg', nearestNeighbor)



# for i in range(3,7):
#     bilinearPixelImage = imgProcessor.bilinearPixelImage(distCenter = i )

#     # cv.imshow('bilinearPixelImage', bilinearPixelImage)

#     cv.imwrite('generatedImgs/bilinearPixelImage{}.jpg'.format(i), bilinearPixelImage)

# for i in range(3,7):
#     bicubicPixelImage = imgProcessor.bicubicPixelImage(distCenter = i)

#     # cv.imshow('bicubicPixelImage', bicubicPixelImage)

#     cv.imwrite('generatedImgs/bicubicPixelImage{}.jpg'.format(i), bicubicPixelImage)





# cv.waitKey(0)
