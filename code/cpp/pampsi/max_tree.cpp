#include "max_tree.hpp"

#include <vector>
#include <iostream>
#include <algorithm>

Point maxtree::_findRoot(const Image& par, const Point& p)
{
    Point parP;
    parP.x = p.x;
    parP.y = p.y;
    parP.value = par(p.x, p.y);

    if (parP.value != p.value) {
        return _findRoot(par, parP);
    }

    return parP;
}

// 4-neighbors
std::vector<Point> maxtree::_neighbour(const Image& f, const Point& pt)
{
    std::vector<Point> result;
 
    const int y[] = { 0, 0, 1, -1 };
    const int x[] = { 1, -1, 0, 0 };
    
    for (int i = 0; i < 4; i++) {
        Point p;
        p.x = pt.x + x[i];
        p.y = pt.y + x[i];

        if (p.x >= 0 && p.x < f.width && p.y >= 0 && p.y < f.height) {
            p.value = f(p.x, p.y);
            result.push_back(p);
        }
    }

    return result;
}

void maxtree::_canonicalize(
    const Image& f, 
    const Image& parent, 
    const std::vector<Point>& S)
{
    for (auto p : S) {
        Point q;
        q.x = p.x;
        q.y = p.y;
        q.value = parent(p.x, p.y);

        //if (f(q.x, q.y) == f(parent(q.x, q.y)))
    }
}

MaxTree maxtree::construct(const Image& img)
{
    MaxTree result;
    result.f = img;
    result.parent = image::create(img.width, img.height, -1);
    result.zpar = image::create(img.width, img.height, -1);

    for (size_t i = 0; i < result.f.width; i++) {
        for (size_t j = 0; j < result.f.height; j++) {
            Point p;
            p.x = (int)i;
            p.y = (int)j;
            p.value = result.f(i, j);
            result.S.push_back(p);
        }
    }

    // Sort pixels
    std::sort(result.S.begin(), result.S.end(),
        [](const Point& p1, const Point& p2) {
            return p1.value < p2.value;
        }
    );

    for (size_t i = result.S.size() - 1; i > 0; i--) {
        auto p = result.S[i];
        result.parent(p.x, p.y) = p.value;
        result.zpar(p.x, p.y) = p.value;
        for (auto n : _neighbour(result.f, p)) {
            if (result.parent(n.x, n.y) == (unsigned char)-1)
                continue;

            auto r = _findRoot(result.zpar, n);
            if (!(r == p)) {
                result.zpar(r.x, r.y) = p.value;
                result.parent(r.x, r.y) = p.value;
            }
        }
    }

    return result;
}

void extinction::valuesArea(MaxTree& tree)
{

}

void extinction::filterArea(MaxTree&)
{

}

std::vector<Image> extinction::profile(
    const Image& img, 
    const std::vector<int>& extrema)
{
    std::vector<Image> profiles{};
    profiles.resize(extrema.size() * 2 + 1);
    int i = 0;

    // Min tree
    auto negate = image::negate(img);
    auto mintree = maxtree::construct(negate);
    auto area = mintree.area;
    //auto Aext = extinction::valuesArea(mintree, area);

    // Base
    profiles.at(i) = img;

    // Max tree

    return profiles;
}