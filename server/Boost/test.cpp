#include <opencv2/opencv.hpp>
#include <iostream>
#include <memory>
#include <string>
#include <filesystem>
#include <vector>

#include "ImageProcessor.h"

namespace fs = std::filesystem;

int main(int argc, char* argv[])
{
    

    std::vector<std::string> paths = {"320/","640/","1280/","2560/"};
// "32/","320/","64/","640/","128/","1280/","256/","2560/"

    for (const std::string path: paths) {
        ImageProcessor imgProc;
        const fs::path pathToShow{ "../testImages/" + path };
        int i = 0;

        // cv::Mat img = cv::imread("../testImages/500.jpg");
        // imgProc.combineWithMask(&img);
        for (const auto& entry : fs::directory_iterator(pathToShow)) {
            i++;
            const auto filenameStr = entry.path().string();
            cv::Mat img = cv::imread(filenameStr);
            imgProc.combineWithMask(&img);
            // imgProc.writeMask("../testMask.jpg");
            // return 0;
            if (i == 2 || i == 5 || i == 20 || i == 100 || i == 1000 || i == 2500){
                imgProc.bicubic(5, "../outputMasks/" + path + std::to_string(i) + ".png" );
            }
        }
    }


    return 0;
}