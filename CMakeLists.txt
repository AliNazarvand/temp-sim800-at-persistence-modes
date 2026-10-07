cmake_minimum_required(VERSION 3.16)
project(sim800_at_persistence_modes VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(MSVC)
    add_compile_options(/W4 /permissive-)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(SIM800_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include")

find_package(Python3 COMPONENTS Interpreter QUIET)
if(Python3_Interpreter_FOUND)
    add_custom_target(generate
        COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_headers.py"
        WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
        COMMENT "Regenerating C++ headers from YAML"
    )
endif()

enable_testing()

set(_HDR_DIR "${SIM800_INCLUDE_DIR}/sim800_at_persistence_modes")

if(EXISTS "${_HDR_DIR}/at_basic.hpp" AND EXISTS "${_HDR_DIR}/sms.hpp"
   AND EXISTS "${_HDR_DIR}/at_3gpp.hpp")
    add_executable(test_generated_headers tests/test_generated_headers.cpp)
    target_include_directories(test_generated_headers PRIVATE ${SIM800_INCLUDE_DIR})
    add_test(NAME test_generated_headers COMMAND test_generated_headers)
else()
    message(STATUS "Skipping test_generated_headers: generated headers not present yet (run scripts/generate_headers.py)")
endif()

add_executable(test_doc_examples tests/test_doc_examples.cpp)
target_include_directories(test_doc_examples PRIVATE ${SIM800_INCLUDE_DIR})
add_test(NAME test_doc_examples COMMAND test_doc_examples)