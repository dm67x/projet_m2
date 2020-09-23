#pragma once

#include <cstdint>
#include <string>
#include <vector>

struct Image
{
    size_t width;
    size_t height;
    unsigned char* data;
    unsigned char& operator()(int, int);
    unsigned char operator()(int, int) const;
};

namespace image
{

Image copy(const Image&);
Image create(size_t, size_t, int);
Image load(const std::string&);
void write(const Image&, const std::string&);
void free(const Image&);

Image negate(const Image&);

}
