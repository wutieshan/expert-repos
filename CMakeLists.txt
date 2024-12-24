# import
include(${CMAKE_SOURCE_DIR}/src/cxx/cmake/settings.cmake)
include(${CMAKE_SOURCE_DIR}/src/cxx/cmake/env.cmake)


cmake_minimum_required(VERSION 3.20 FATAL_ERROR)
# CMAKE_<LANG>_COMPILER必须位于cmake_minimum_required()之后, project()之前
set(CMAKE_C_COMPILER ${g_env_c_compiler})
set(CMAKE_CXX_COMPILER ${g_env_cxx_compiler})
project(${g_basic_project} VERSION ${g_basic_version} LANGUAGES C CXX)


# environment
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/${g_dir_output_lib})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/${g_dir_output_bin})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/${g_dir_output_bin})


# compiler flags
# add_compile_options(-lpthread)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Werror -Wextra -pedantic -std=c++20 -fPIC -O3 -g -pthread")


# include
include_directories(
    ${CMAKE_SOURCE_DIR}/${g_dir_include}
)


# executable
# 注意file(GLOB ...)有局限性, 它不能自动检测新添加的文件, 如果源文件列表发生变化, 需要重新运行cmake来生成新的构建系统
file(GLOB srcs
    "${g_dir_src}/main.cxx"
)
add_executable(${PROJECT_NAME} ${srcs})


# python C/C++ api
# target_include_directories(${PROJECT_NAME} PRIVATE "C:/tieshan/env/python/3.12.5/include")
# target_link_directories(${PROJECT_NAME} PRIVATE "C:/tieshan/env/python/3.12.5/libs")
# target_link_libraries(${PROJECT_NAME} PRIVATE "python312")