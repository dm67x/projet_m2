#include "image.hpp"
#include "max_tree.hpp"

#include <iostream>

int main(int argc, char** argv)
{
    if (argc != 3) {
        std::cerr << "usage: " << argv[0] << " input output" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    std::string input{ argv[1] };
    std::string output{ argv[2] };

    Image img = image::load(input);

    // traitement
    auto nimg = image::negate(img);
    auto tree = maxtree::construct(nimg);

    std::cout << tree.parent.width << "x" << tree.parent.height << std::endl;
    std::cout << tree.S.size() << std::endl;

    image::write(tree.parent, output + "_parent.png");

    image::free(img);
    image::free(tree.parent);
    image::free(tree.zpar);
    return EXIT_SUCCESS;
}