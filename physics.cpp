#include "physics.h"
#include <algorithm>
#include <unordered_map>

// screen height for tkinter (y increases downward)
static const double SCREEN_HEIGHT = 800.0;

// gravity strength (pixels per second squared)
double Block::gravity = 980.0;  
// 980 ≈ 9.8 m/s² scaled for pixels (you can tune this later)

// --------------------
// Block
// --------------------

Block::Block(double startX, double startY)
{
    x = startX;
    y = startY;

    width = 50;
    height = 50;
    mass = 1.0;

    vy = 0.0;
}

void Block::update(double dt, GameControl& gameControl)
{
    (void)gameControl;

    // apply gravity (positive = downward in tkinter)
    vy += gravity * dt;

    // integrate position
    y += vy * dt;
}

// --------------------
// GameControl
// --------------------

void GameControl::addBlock(double x, double y)
{
    blocks.emplace_back(x, y);
}

void GameControl::update(double dt)
{
    static const double CONTACT_EPS = 0.5;

    std::unordered_map<const Block*, double> prev_y;
    prev_y.reserve(blocks.size());
    for (auto& block : blocks) {
        prev_y[&block] = block.y;
    }

    for (auto& block : blocks) {
        block.update(dt, *this);
    }

    std::vector<Block*> order;
    order.reserve(blocks.size());
    for (auto& block : blocks) {
        order.push_back(&block);
    }

    std::sort(order.begin(), order.end(), [](const Block* a, const Block* b) {
        return a->y > b->y;
    });

    for (size_t i = 0; i < order.size(); ++i) {
        Block* block = order[i];
        double groundY = SCREEN_HEIGHT - block->height;

        if (block->y > groundY) {
            block->y = groundY;
            block->vy = 0.0;
        }

        double prev_bottom = prev_y[block] + block->height;
        double next_bottom = block->y + block->height;

        double support_y = 1e9;
        double support_vy = 0.0;
        bool supported = false;

        for (size_t j = 0; j < i; ++j) {
            Block* below = order[j];
            bool x_overlap = block->x < below->x + below->width &&
                             block->x + block->width > below->x;
            if (!x_overlap) {
                continue;
            }

            double top = below->y;
            bool swept_hit = prev_bottom <= top + CONTACT_EPS &&
                             next_bottom >= top - CONTACT_EPS;
            bool overlap_now = block->y + block->height > top - CONTACT_EPS &&
                               block->y < top + below->height + CONTACT_EPS;

            if (swept_hit || overlap_now) {
                if (top < support_y) {
                    support_y = top;
                    support_vy = below->vy;
                    supported = true;
                }
            }
        }

        if (supported) {
            block->y = support_y - block->height;
            block->vy = support_vy;
        }
    }
}
