#pragma once
#include <vector>

class GameControl;  // forward declaration

class Block {
public:
    double mass;
    double width;
    double height;

    double x;
    double y;
    double vy;

    static double gravity;

    Block(double startX, double startY);

    void update(double dt, GameControl& gameControl);
};

class GameControl {
public:
    std::vector<Block> blocks;

    void addBlock(double x, double y);
    void update(double dt);
};
