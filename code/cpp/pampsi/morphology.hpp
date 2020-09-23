#pragma once

#include "image.hpp"

namespace morphology
{

Image& area_opening(const Image&);
Image& area_closing(const Image&);

}