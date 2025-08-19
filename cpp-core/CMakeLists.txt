
cmake_minimum_required(VERSION 3.16)
project(cryptoquant_core LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
add_library(cryptoquant_core STATIC src/arb.cpp)
target_include_directories(cryptoquant_core PUBLIC include)
add_executable(arb_engine src/main.cpp src/arb.cpp)
target_include_directories(arb_engine PRIVATE include)
