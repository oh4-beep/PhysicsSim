#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "physics.h"

namespace py = pybind11;

PYBIND11_MODULE(simcore, m) {
    m.doc() = "Physics core (C++), exposed to Python via pybind11";

    // -------------------------
    // Block
    // -------------------------
    py::class_<Block>(m, "Block")
        .def(py::init<double, double>(), py::arg("x"), py::arg("y"))
        .def_readwrite("mass", &Block::mass)
        .def_readwrite("width", &Block::width)
        .def_readwrite("height", &Block::height)
        .def_readwrite("x", &Block::x)
        .def_readwrite("y", &Block::y)
        .def_readwrite("vy", &Block::vy)
        .def("update", &Block::update, py::arg("dt"), py::arg("gameControl"));

    // expose gravity as module-level getters/setters (simple for Python)
    m.def("get_gravity", []() { return Block::gravity; });
    m.def("set_gravity", [](double g) { Block::gravity = g; });

    // -------------------------
    // GameControl
    // -------------------------
    py::class_<GameControl>(m, "GameControl")
        .def(py::init<>())

        // add a block (same signature as your C++ addBlock)
        .def("add_block", &GameControl::addBlock, py::arg("x"), py::arg("y"))

        // step sim
        .def("update", &GameControl::update, py::arg("dt"))

        // return a Python-friendly snapshot
        .def("get_blocks", [](GameControl &gc) {
            py::list out;
            int i = 0;
            for (auto &b : gc.blocks) {
                py::dict d;
                d["id"] = i;              // simple id = index for now
                d["x"] = b.x;
                d["y"] = b.y;
                d["width"] = b.width;
                d["height"] = b.height;
                d["mass"] = b.mass;
                d["vy"] = b.vy;
                out.append(d);
                i++;
            }
            return out;
        });
}
