// #include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include "ImageProcessor.h"
#include <queue>


ImageProcessor::ImageProcessor(){
    mask = CustomMat(1024,1024);
}

bool ImageProcessor::is_base64(unsigned char c){
    return (isalnum(c) || (c == '+') || (c == '/'));
}

std::string ImageProcessor::base64_decode(std::string const& encoded_string){
    int in_len = encoded_string.size();
    int i = 0;
    int j = 0;
    int in_ = 0;
    unsigned char char_array_4[4], char_array_3[3];
    std::string ret;

    while (in_len-- && (encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
        char_array_4[i++] = encoded_string[in_]; in_++;
        if (i == 4) {
            for (i = 0; i < 4; i++)
                char_array_4[i] = base64_chars.find(char_array_4[i]);

            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

            for (i = 0; (i < 3); i++)
                ret += char_array_3[i];
            i = 0;
        }
    }

    if (i) {
        for (j = i; j < 4; j++)
            char_array_4[j] = 0;

        for (j = 0; j < 4; j++)
            char_array_4[j] = base64_chars.find(char_array_4[j]);

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
        char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
        char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

        for (j = 0; (j < i - 1); j++) ret += char_array_3[j];
    }

    return ret;
}

struct Point{
    int x;
    int y;
    Point(int _x, int _y){
        x = _x;
        y = _y;
    }
};

void ImageProcessor::nearestNeighbour(std::string path){
    cv::Mat img = mask.getMask();

    std::queue<Point> pixels;

    for(int i=0; i<img.rows; i++){
        for(int j=0; j<img.cols; j++) {
            // You can now access the pixel value with cv::Vec3b
            auto pixel = img.at<cv::Vec3b>(i,j);
            if (pixel[0] != 0 || pixel[1] != 0 || pixel[2] != 0) {
                pixels.push(Point(i,j));
            }
            // std::cout <<  << " " << img.at<cv::Vec3b>(i,j)[1] << " " << img.at<cv::Vec3b>(i,j)[2] << std::endl;
        }
    }
     
    while (!pixels.empty()){
        Point curPoint = pixels.front();
        pixels.pop();

        cv::Vec3b curPixel = img.at<cv::Vec3b>(curPoint.x,curPoint.y);
        for (int i = 0; i < 4; i ++ ){
            int x = curPoint.x;
            int y = curPoint.y;
            if (i%2 == 0){ // 0 or 2
                y += -1 + i;
            } else { // 1 or 3
                x += -2 + i;
            }
            if (x >= 0 && x < img.rows && y >= 0 && y < img.cols) {
                cv::Vec3b nextPoint = img.at<cv::Vec3b>(x,y);
                if (nextPoint[0] == 0 && nextPoint[1] == 0 && nextPoint[2] == 0){
                    img.at<cv::Vec3b>(x,y)[0] = curPixel[0];
                    img.at<cv::Vec3b>(x,y)[1] = curPixel[1];
                    img.at<cv::Vec3b>(x,y)[2] = curPixel[2];
                    pixels.push(Point(x,y));
                }
            }
        }
    }

    cv::imwrite(path, img);
}

void ImageProcessor::bicubic(int dist, std::string path){
    cv::Mat outputImage = cv::Mat::zeros(cv::Size(mask.width,mask.height),CV_8UC3);

    // handle all center points without checking for outside bounds
    for (int i = dist; i < outputImage.rows - dist; i++) {
        // for (int j = dist; j < outputImage.cols - dist; j++){
        for (int j = dist; j < outputImage.cols - dist; j++){
            long pixelValSum = 0;
            long rSum = 0;
            long gSum = 0;
            long bSum = 0;
            for (int curDist = 0; curDist < dist; curDist++){
                for(int subDist = 1-curDist; subDist < curDist+1; subDist++){
                    double pixelWeighting = 1 / fmin(0.25, curDist);
                    // handles all 4 corners
                    for(int c = 0; c < 4; c++){
                        int x = i;
                        int y = j;
                        if (c == 0){
                            x += curDist;
                            y -= subDist;
                        } else if (c==1)
                        {
                            x -= curDist;
                            y += subDist;
                        } else if (c==2)
                        {
                            x += subDist;
                            y += curDist;
                        } else if (c==3)
                        {
                            x -= subDist;
                            y -= curDist;
                        }
                        CustomMat::Pixel* curPixel = mask.at(y, x);
                        pixelValSum += curPixel->numPixels * pixelWeighting;
                        rSum += double(curPixel->r) * pixelWeighting;
                        gSum += double(curPixel->g) * pixelWeighting;
                        bSum += double(curPixel->b) * pixelWeighting;
                    }
                }
            }
            if (pixelValSum > 0){
                cv::Vec3b pix = outputImage.at<cv::Vec3b>(cv::Point(i, j));
                pix[0] = int((rSum) / pixelValSum);
                pix[1] = int((gSum) / pixelValSum);
                pix[2] = int((bSum) / pixelValSum);
                // pix[0] = 255;
                // pix[1] = 255;
                // pix[2] = 255;
                outputImage.at<cv::Vec3b>(cv::Point(i, j)) = pix;
            }
        }
    }
    // nearestNeighbour(path, outputImage);
    cv::imwrite(path, outputImage);
}

void ImageProcessor::combineWithMask(cv::Mat* inputImage, int imgUpscale){

    // cv::imwrite("./wtf.jpg", *inputImage);
    // Find number of pixels.
    // cv::transpose(*inputImage, *inputImage);
    // cv::flip(*inputImage, *inputImage, 1);

    int numberOfPixels = inputImage->rows * inputImage->cols / 2 ;

    // std::cout << inputImage->rows << " " << inputImage->cols << " "  << numberOfPixels << std::endl;

    // Get floating point pointers to the data matrices
    // uint8_t* maskptr = reinterpret_cast<uint8_t*>(inputImage->data);
    // uint8_t* imgptr = reinterpret_cast<uint8_t*>(inputImage->data) + numberOfPixels * 3;

    // uint8_t* endPtr = reinterpret_cast<uint8_t*>(inputImage->data) + numberOfPixels * 3;

    int hu = imgUpscale / 2;
    int it = hu + 1;
    int imgRows = inputImage->rows;
    int imgCols = inputImage->cols;
    int rows = inputImage->rows/imgUpscale;
    int cols = inputImage->cols/imgUpscale;

    cv::MatIterator_<cv::Vec3b> itMask = inputImage->begin<cv::Vec3b>() + hu + imgCols * hu; 
    cv::MatIterator_<cv::Vec3b> itImg = inputImage->begin<cv::Vec3b>() + numberOfPixels + hu + imgCols * hu; 
    cv::MatIterator_<cv::Vec3b> rowEnd = inputImage->begin<cv::Vec3b>() + hu; 
    cv::MatIterator_<cv::Vec3b> itEnd = inputImage->begin<cv::Vec3b>() + numberOfPixels; 
    // int sum = 0;
    // Loop over all pixesl ONCE
    for (
        int r = 0;
        r < rows;
        r ++, itMask += imgCols * it, itImg += imgCols * it
    ) {
        for(
            int c = 0;
            c < cols && itMask < itEnd;
            c++, itMask+=it, itImg+=it
        ) {
            // if the mask is not black 
            if ((itMask)[0][1] > 60) {
                
                int b = (itMask)[0][2];
                int g = 127;
                int r = (itMask)[0][0];

                // int maskX = (r*16 + ((g-g%16)/16));
                // int maskY = (b*16 + g%16);
                int maskX = 1024 - 1 - r*4;
                int maskY = b*4;

                // std::cout << r << " " << g << " " << b << " " << maskX << " " << maskY << std::endl;

                CustomMat::Pixel* prevColor = mask.at(maskX, maskY);

                prevColor->r += uint((itImg)[0][0]);
                prevColor->g += uint((itImg)[0][1]);
                prevColor->b += uint((itImg)[0][2]);
                prevColor->numPixels++;
            } 
        }
    }
    

    // std::cout << sum << std::endl;
}

void ImageProcessor::processMessage(std::string message){
    std::string dec_jpg =  base64_decode(message);
    std::vector<uchar> data(dec_jpg.begin(), dec_jpg.end());
    cv::Mat img = cv::imdecode(cv::Mat(data), 1);
    // cv::imwrite("./Test.jpg", img);
    combineWithMask(&img);
}

void ImageProcessor::showMask(){
    cv::imshow("mask", mask.getMask());
}

void ImageProcessor::writeMask(std::string path){
    cv::imwrite(path, mask.getMask());
}

ImageProcessor::~ImageProcessor(){
    
}
