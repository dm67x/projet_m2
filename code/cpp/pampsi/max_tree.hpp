#pragma once

#include "image.hpp"

#include <vector>
#include <stack>

struct Point
{
    int x;
    int y;
    unsigned char value;

    friend bool operator==(const Point& p1, const Point& p2)
    {
        return p1.x == p2.x && p1.y == p2.y && p1.value == p2.value;
    }
};

struct MaxTree
{
    Image f;
    Image parent;
    Image zpar;
    std::vector<Point> S;
    std::vector<float> area;
};

namespace maxtree
{

static Point _findRoot(const Image&, const Point&);
static std::vector<Point> _neighbour(const Image&, const Point&);
static void _canonicalize(const Image&, const Image&, const std::vector<Point>&);

MaxTree construct(const Image&);
void computeAttribute(const MaxTree&);

}

namespace extinction
{

void valuesArea(MaxTree&);
void filterArea(MaxTree&);
std::vector<Image> profile(const Image&, const std::vector<int>&);

}