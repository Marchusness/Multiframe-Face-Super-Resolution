#ifndef IMAGEPROCESSOR_H
#define IMAGEPROCESSOR_H
#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

class ImageProcessor {
    private:

        class CustomMat {
        public:
            struct Pixel {
                Pixel(){
                    r = 0;
                    g = 0;
                    b = 0;
                    numPixels = 0;
                }
                uint r;
                uint g;
                uint b;
                uint numPixels;
                uint8_t gr(){
                    return static_cast<uint8_t>(int(float(r) / numPixels + 0.5));
                }
                uint8_t gg(){
                    return static_cast<uint8_t>(int(float(g) / numPixels + 0.5));
                }
                uint8_t gb(){
                    return static_cast<uint8_t>(int(float(b) / numPixels + 0.5));
                }
            };
            Pixel* mat;
            int width;
            int height;
            CustomMat(){
                width = 1024;
                height = 1024;
                mat = new Pixel[width * height];
                for(int i = 0; i < width * height; i++){
                    mat[i] = Pixel();
                }
            }
            CustomMat(int _width, int _height){
                width = _width;
                height = _height;
                mat = new Pixel[width * height];
                for(int i = 0; i < width * height; i++){
                    mat[i] = Pixel();
                }
            }
            Pixel* at(int y, int x){
                return &mat[width * y + x];
            }
            cv::Mat getMask(){
                cv::Mat mask = cv::Mat::zeros(cv::Size(width,height),CV_8UC3);
                uint8_t* maskptr = reinterpret_cast<uint8_t*>(mask.data);
                Pixel* matptr = mat;
                // std::cout << int((*matptr).gr()) << " " << int((*matptr).gg()) << " " << int((*matptr).gb()) << std::endl;
                for (
                    int i = 0; 
                    i < width * height; 
                    i++, maskptr += 3, matptr++ ){
                        maskptr[0] = (*matptr).gr();
                        maskptr[1] = (*matptr).gg();
                        maskptr[2] = (*matptr).gb();
                }
                return mask;
            }
        };

        CustomMat mask;

        std::string base64_chars =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz"
            "0123456789+/";

        bool is_base64(unsigned char c);
        std::string base64_decode(std::string const& encoded_string);

    public:
        void combineWithMask(cv::Mat* inputImage, int imgUpscale = 10);
        ImageProcessor();
        void nearestNeighbour(std::string path = "../nearestNeighbour.png");
        void bicubic(int dist = 5, std::string path = "../bicubic.png");
        void processMessage(std::string message);
        void showMask();
        void writeMask(std::string path = "../testMask.jpg");
        ~ImageProcessor();
};
#endif
