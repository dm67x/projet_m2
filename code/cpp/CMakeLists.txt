cmake_minimum_required(VERSION 3.8)

project(Pampsi)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY bin)
add_subdirectory(third_party/stb)
include_directories(third_party/stb)
file(GLOB SRCFILES pampsi/**.cpp pampsi/**.hpp)
add_executable(pampsi ${SRCFILES})
target_include_directories(pampsi PUBLIC pampsi)
target_link_libraries(pampsi PRIVATE stb)