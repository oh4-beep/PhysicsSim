#pragma once


class World {
    double gravity = 9.81;

public:
    double get_gravity() const { return gravity; }
    void set_gravity(double g) { gravity = g; }
};
