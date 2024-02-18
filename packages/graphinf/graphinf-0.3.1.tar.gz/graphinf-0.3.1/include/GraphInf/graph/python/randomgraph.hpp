#ifndef GRAPH_INF_PYTHON_RANDOMGRAPH_HPP
#define GRAPH_INF_PYTHON_RANDOMGRAPH_HPP

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "BaseGraph/types.h"
#include "GraphInf/types.h"
#include "GraphInf/python/rv.hpp"
#include "GraphInf/graph/random_graph.hpp"
#include "GraphInf/graph/proposer/movetypes.h"

namespace GraphInf
{

    template <typename BaseClass = RandomGraph>
    class PyRandomGraph : public PyNestedRandomVariable<BaseClass>
    {
    protected:
        void _applyGraphMove(const GraphMove &move) override { PYBIND11_OVERRIDE(void, BaseClass, _applyGraphMove, move); }
        const double _getLogPrior() const override { PYBIND11_OVERRIDE(const double, BaseClass, _getLogPrior); }
        const double _getLogPriorRatioFromGraphMove(const GraphMove &move) const override { PYBIND11_OVERRIDE(const double, BaseClass, _getLogPriorRatioFromGraphMove, move); }
        void sampleOnlyPrior() override { PYBIND11_OVERRIDE(void, BaseClass, sampleOnlyPrior, ); }
        void setUpLikelihood() override { PYBIND11_OVERRIDE(void, BaseClass, setUpLikelihood, ); }
        void computeConsistentState() override { PYBIND11_OVERRIDE(void, BaseClass, computeConsistentState, ); }

    public:
        using PyNestedRandomVariable<BaseClass>::PyNestedRandomVariable;

        /* Pure abstract methods */
        const size_t getEdgeCount() const override
        {
            PYBIND11_OVERRIDE_PURE(const size_t &, BaseClass, getEdgeCount, );
        }

        /* Abstract methods */
        void setUp() override { PYBIND11_OVERRIDE(void, BaseClass, setUp, ); }
        const bool isCompatible(const MultiGraph &graph) const override { PYBIND11_OVERRIDE(bool, BaseClass, isCompatible, graph); }
        bool isSafe() const override { PYBIND11_OVERRIDE(bool, BaseClass, isSafe, ); }
        void checkSelfSafety() const override { PYBIND11_OVERRIDE(void, BaseClass, checkSelfSafety, ); }
        void checkSelfConsistency() const override { PYBIND11_OVERRIDE(void, BaseClass, checkSelfConsistency, ); }
        // void fromGraph(const MultiGraph &graph) override { PYBIND11_OVERRIDE(void, BaseClass, fromGraph, graph); }
        bool isValidGraphMove(const GraphMove &move) const override { PYBIND11_OVERRIDE(bool, BaseClass, isValidGraphMove, move); }
    };

    template <typename Label, typename BaseClass = VertexLabeledRandomGraph<Label>>
    class PyVertexLabeledRandomGraph : public PyRandomGraph<BaseClass>
    {
    protected:
        void _applyLabelMove(const LabelMove<Label> &move) override { PYBIND11_OVERRIDE(void, BaseClass, _applyLabelMove, move); }
        const double _getLogPriorRatioFromLabelMove(const LabelMove<Label> &move) const override { PYBIND11_OVERRIDE_PURE(const double, BaseClass, _getLogPriorRatioFromLabelMove, move); }

    public:
        using PyRandomGraph<BaseClass>::PyRandomGraph;

        /* Pure abstract methods */
        void setLabels(const std::vector<BlockIndex> &labels, bool reduce = false) override { PYBIND11_OVERRIDE_PURE(void, BaseClass, setLabels, labels, reduce); }
        void sampleOnlyLabels() override { PYBIND11_OVERRIDE_PURE(void, BaseClass, sampleOnlyLabels, ); }
        void sampleWithLabels() override { PYBIND11_OVERRIDE_PURE(void, BaseClass, sampleWithLabels, ); }
        const double getLabelLogJoint() const override { PYBIND11_OVERRIDE_PURE(const double, BaseClass, getLabelLogJoint, ); }

        const std::vector<Label> &getLabels() const override
        {
            PYBIND11_OVERRIDE_PURE(const std::vector<Label> &, BaseClass, getLabels, );
        }
        const size_t getLabelCount() const override
        {
            PYBIND11_OVERRIDE_PURE(const size_t &, BaseClass, getLabelCount, );
        }
        const CounterMap<Label> &getVertexCounts() const override
        {
            PYBIND11_OVERRIDE_PURE(const CounterMap<Label> &, BaseClass, getVertexCounts, );
        }
        const CounterMap<Label> &getEdgeLabelCounts() const override
        {
            PYBIND11_OVERRIDE_PURE(const CounterMap<Label> &, BaseClass, getEdgeLabelCounts, );
        }
        const MultiGraph &getLabelGraph() const override
        {
            PYBIND11_OVERRIDE_PURE(const MultiGraph &, BaseClass, getLabelGraph, );
        }

        /* Abstract methods */
        bool isValidLabelMove(const LabelMove<Label> &move) const override { PYBIND11_OVERRIDE(bool, BaseClass, isValidLabelMove, move); }
    };

    template <typename Label, typename BaseClass = NestedVertexLabeledRandomGraph<Label>>
    class PyNestedVertexLabeledRandomGraph : public PyVertexLabeledRandomGraph<Label, BaseClass>
    {
    public:
        using PyVertexLabeledRandomGraph<Label, BaseClass>::PyVertexLabeledRandomGraph;

        /* Pure abstract methods */
        void setNestedLabels(const std::vector<std::vector<Label>> &labels, bool reduce = false) override { PYBIND11_OVERRIDE_PURE(void, BaseClass, setNestedLabels, labels, reduce); }
        const size_t getDepth() const override { PYBIND11_OVERRIDE_PURE(const size_t, BaseClass, getDepth, ); }
        const Label getLabel(BaseGraph::VertexIndex vertex, Level level) const override { PYBIND11_OVERRIDE_PURE(const Label, BaseClass, getLabel, vertex, level); }
        const Label getNestedLabel(BaseGraph::VertexIndex vertex, Level level) const override { PYBIND11_OVERRIDE_PURE(const Label, BaseClass, getNestedLabel, vertex, level); }
        const std::vector<std::vector<Label>> &getNestedLabels() const override
        {
            PYBIND11_OVERRIDE_PURE(const std::vector<std::vector<Label>> &, BaseClass, getNestedLabels, );
        }
        const std::vector<Label> &getNestedLabels(Level level) const override
        {
            PYBIND11_OVERRIDE_PURE(const std::vector<Label> &, BaseClass, getNestedLabels, level);
        }
        const std::vector<size_t> &getNestedLabelCount() const override { PYBIND11_OVERRIDE_PURE(const std::vector<size_t> &, BaseClass, getNestedLabelCount, ); };
        const size_t getNestedLabelCount(Level level) const override { PYBIND11_OVERRIDE_PURE(const size_t, BaseClass, getNestedLabelCount, level); };
        const std::vector<CounterMap<Label>> &getNestedVertexCounts() const override { PYBIND11_OVERRIDE_PURE(const std::vector<CounterMap<Label>> &, BaseClass, getNestedVertexCounts, ); };
        const CounterMap<Label> &getNestedVertexCounts(Level level) const override { PYBIND11_OVERRIDE_PURE(const CounterMap<Label> &, BaseClass, getNestedVertexCounts, level); };
        const std::vector<CounterMap<Label>> &getNestedEdgeLabelCounts() const override { PYBIND11_OVERRIDE_PURE(const std::vector<CounterMap<Label>> &, BaseClass, getNestedEdgeLabelCounts, ); };
        const CounterMap<Label> &getNestedEdgeLabelCounts(Level level) const override { PYBIND11_OVERRIDE_PURE(const CounterMap<Label> &, BaseClass, getNestedEdgeLabelCounts, level); };
        const std::vector<MultiGraph> &getNestedLabelGraph() const override { PYBIND11_OVERRIDE_PURE(const std::vector<MultiGraph> &, BaseClass, getNestedLabelGraph, ); };
        const MultiGraph &getNestedLabelGraph(Level level) const override { PYBIND11_OVERRIDE_PURE(const MultiGraph &, BaseClass, getNestedLabelGraph, level); };

        /* Abstract methods */
    };

}

#endif
