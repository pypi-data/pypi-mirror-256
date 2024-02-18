#ifndef GRAPH_INF_PYTHON_PROPOSER_HPP
#define GRAPH_INF_PYTHON_PROPOSER_HPP

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "GraphInf/graph/proposer/proposer.hpp"
#include "GraphInf/python/rv.hpp"

namespace py = pybind11;
namespace GraphInf
{

    template <typename MoveType, typename BaseClass = Proposer<MoveType>>
    class PyProposer : public PyNestedRandomVariable<BaseClass>
    {
    public:
        using PyNestedRandomVariable<BaseClass>::PyNestedRandomVariable;

        /* Pure abstract methods */
        const MoveType proposeMove() const override { PYBIND11_OVERRIDE_PURE(const MoveType, BaseClass, proposeMove, ); }

        /* Abstract & overloaded methods */
        ~PyProposer() override = default;
        void clear() override { PYBIND11_OVERRIDE(void, BaseClass, clear, ); }
    };

}

#endif
