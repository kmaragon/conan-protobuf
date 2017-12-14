project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

list(GET CONAN_BINDIRS_PROTOBUF 0 protobuf_dir)
find_program(protoc_command "protoc" HINTS "${protobuf_dir}")

add_custom_command(
    COMMAND "${protoc_command}" --cpp_out "${CMAKE_CURRENT_BINARY_DIR}" test.proto
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/test.proto"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/test.pb.h" "${CMAKE_CURRENT_BINARY_DIR}/test.pb.cc"
)

add_executable(example example.cpp "${CMAKE_CURRENT_BINARY_DIR}/test.pb.cc")
target_include_directories(example PUBLIC ${CONAN_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(example ${CONAN_LIBS})
