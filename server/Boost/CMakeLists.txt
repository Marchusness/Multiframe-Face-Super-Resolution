
cmake_minimum_required(VERSION 3.5)

# Set the project name
project (project)
set(CMAKE_OSX_ARCHITECTURES "arm64")
set(CMAKE_CXX_STANDARD 17)

# Add an executable
add_executable(project main.cpp)

# opencv
find_package(OpenCV REQUIRED)
target_link_libraries( project  ${OpenCV_LIBS})

# boost
set(Boost_USE_STATIC_LIBS OFF) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF) 
find_package(Boost 1.80.0 COMPONENTS beast) 
include_directories(${Boost_INCLUDE_DIRS}) 
target_link_libraries(project ${Boost_LIBRARIES})

# custom ImageProcessor
add_library(ImageProcessor ImageProcessor.cpp)
target_link_libraries( ImageProcessor  ${OpenCV_LIBS})
target_link_libraries(project ImageProcessor)





# building the test excecutable
add_executable(test test.cpp)
find_package(OpenCV REQUIRED)
target_link_libraries( test  ${OpenCV_LIBS})

# custom ImageProcessor
target_link_libraries(test ImageProcessor)