#include "image.hpp"
#include "stb_image.h"
#include "stb_image_write.h"

#include <cassert>
#include <cstring>
#include <iostream>
#include <stdexcept>

unsigned char& Image::operator()(int x, int y)
{
    assert(x >= 0);
    assert(y >= 0);
    assert(x < width);
    assert(y < height);

    return data[x + y * height];
}

unsigned char Image::operator()(int x, int y) const
{
    assert(x >= 0);
    assert(y >= 0);
    assert(x < width);
    assert(y < height);

    return data[x + y * height];
}

Image image::copy(const Image& img)
{
    Image copy;
    copy.width = img.width;
    copy.height = img.height;
    copy.data = new unsigned char[copy.width * copy.height];
    std::memcpy(copy.data, img.data, img.width * img.height);
    return copy;
}

Image image::create(size_t w, size_t h, int v)
{
    Image result;
    result.width = w;
    result.height = h;
    result.data = new unsigned char[w * h];

    for (size_t i = 0; i < w * h; i++) {
        result.data[i] = (unsigned char)v;
    }

    return result;
}

Image image::load(const std::string& filename)
{
    Image result;

    int width;
    int height;
    int channel;

    result.data = stbi_load(
        filename.c_str(), 
        &width, 
        &height, 
        &channel, 
        1);

    result.width = width;
    result.height = height;

    if (!result.data) {
        throw std::runtime_error("cannot read image");
    }

    return result;
}

void image::write(const Image& img, const std::string& filename)
{
    int result = stbi_write_png(
        filename.c_str(), 
        (int)img.width, 
        (int)img.height, 
        1, 
        img.data, 
        (int)img.width);

    if (result == 0) {
        throw std::runtime_error("cannot write image");
    }
}

Image image::negate(const Image& img)
{
    Image copy = image::copy(img);
    unsigned char maxValue = 0;
    const size_t width = copy.width;
    const size_t height = copy.height;

    // find max value
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            if (maxValue < copy(i, j)) {
                maxValue = copy(i, j);
            }
        }
    }

    // substract to all values
    for (size_t i = 0; i < width * height; i++) {
        copy.data[i] = maxValue - copy.data[i];
    }

    return copy;
}

void image::free(const Image& img)
{
    stbi_image_free(img.data);
}