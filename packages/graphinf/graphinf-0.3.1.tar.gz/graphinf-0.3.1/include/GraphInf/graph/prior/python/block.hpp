#ifndef GRAPH_INF_PYTHON_BLOCK_H
#define GRAPH_INF_PYTHON_BLOCK_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

#include "GraphInf/types.h"
#include "GraphInf/graph/prior/prior.hpp"
#include "GraphInf/graph/prior/python/prior.hpp"
#include "GraphInf/graph/prior/block_count.h"
#include "GraphInf/graph/prior/block.h"

namespace GraphInf
{

    template <typename BaseClass = BlockPrior>
    class PyBlockPrior : public PyVertexLabeledPrior<std::vector<BlockIndex>, BlockIndex, BaseClass>
    {
    protected:
        void _applyLabelMove(const BlockMove &move) override { PYBIND11_OVERRIDE(void, BaseClass, _applyLabelMove, move); }
        const double _getLogPriorRatioFromLabelMove(const BlockMove &move) const override { PYBIND11_OVERRIDE(const double, BaseClass, _getLogPriorRatioFromLabelMove, move); }
        void setBlockCountFromPartition(const BlockSequence &blocks) override { PYBIND11_OVERRIDE(void, BaseClass, setBlockCountFromPartition, blocks); }

    public:
        using PyVertexLabeledPrior<std::vector<BlockIndex>, BlockIndex, BaseClass>::PyVertexLabeledPrior;
        ~PyBlockPrior() override = default;
        /* Pure abstract methods */

        /* Overloaded abstract methods */
        void setState(const BlockSequence &blocks) override { PYBIND11_OVERRIDE(void, BaseClass, setState, blocks); }
        void setSize(size_t size) override { PYBIND11_OVERRIDE(void, BaseClass, setSize, size); }
        const double getLogLikelihoodRatioFromLabelMove(const BlockMove &move) const override { PYBIND11_OVERRIDE_PURE(const double, BaseClass, getLogLikelihoodRatioFromLabelMove, move); }
        bool creatingNewBlock(const BlockMove &move) const override { PYBIND11_OVERRIDE(bool, BaseClass, creatingNewBlock, move); }
        bool destroyingBlock(const BlockMove &move) const override { PYBIND11_OVERRIDE(bool, BaseClass, destroyingBlock, move); }
        const int getAddedBlocks(const BlockMove &move) const override { PYBIND11_OVERRIDE(const int, BaseClass, getAddedBlocks, move); }
    };

}

#endif
