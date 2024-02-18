#ifndef GRAPH_INF_PYTHON_EDGE_PROPOSER_HPP
#define GRAPH_INF_PYTHON_EDGE_PROPOSER_HPP

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "BaseGraph/types.h"
#include "GraphInf/types.h"
#include "GraphInf/graph/proposer/python/proposer.hpp"
#include "GraphInf/graph/proposer/edge/edge_proposer.h"
#include "GraphInf/graph/proposer/edge/hinge_flip.h"
#include "GraphInf/graph/proposer/edge/single_edge.h"
// #include "GraphInf/graph/proposer/edge/labeled_edge_proposer.h"
// #include "GraphInf/graph/proposer/edge/labeled_hinge_flip.h"

// namespace py = pybind11;
namespace GraphInf
{

    template <typename BaseClass = EdgeProposer>
    class PyEdgeProposer : public PyProposer<GraphMove, BaseClass>
    {
    public:
        using PyProposer<GraphMove, BaseClass>::PyProposer;
        ~PyEdgeProposer() override = default;

        /* Pure abstract methods */
        const GraphMove proposeRawMove() const override { PYBIND11_OVERRIDE_PURE(const GraphMove, BaseClass, proposeRawMove, ); }
        const double getLogProposalProbRatio(const GraphMove &move) const override { PYBIND11_OVERRIDE_PURE(const double, BaseClass, getLogProposalProbRatio, move); }

        /* Abstract & overloaded methods */
        void setUpWithGraph(const MultiGraph &graph) override { PYBIND11_OVERRIDE_PURE(void, BaseClass, setUp, graph); }
        void setUpWithPrior(const RandomGraph &prior) override { PYBIND11_OVERRIDE_PURE(void, BaseClass, setUp, prior); }
        void applyGraphMove(const GraphMove &move) override { PYBIND11_OVERRIDE(void, BaseClass, applyGraphMove, move); }
        void clear() override { PYBIND11_OVERRIDE(void, BaseClass, clear, ); }
    };

    template <typename BaseClass = HingeFlipProposer>
    class PyHingeFlipProposer : public PyEdgeProposer<BaseClass>
    {
    public:
        using PyEdgeProposer<BaseClass>::PyEdgeProposer;
        ~PyHingeFlipProposer() override = default;

        /* Pure abstract methods */
        const double getLogVertexWeightRatio(const GraphMove &move) const override { PYBIND11_OVERRIDE_PURE(const double, BaseClass, getLogVertexWeightRatio, move); }

        /* Abstract & overloaded methods */
    };

    template <typename BaseClass = SingleEdgeProposer>
    class PySingleEdgeProposer : public PyEdgeProposer<BaseClass>
    {
    public:
        using PyEdgeProposer<BaseClass>::PyEdgeProposer;
        ~PySingleEdgeProposer() override = default;

        /* Pure abstract methods */

        /* Abstract & overloaded methods */
        void applyGraphMove(const GraphMove &move) override { PYBIND11_OVERRIDE(void, BaseClass, applyGraphMove, move); }
    };

    // template<typename BaseClass = LabeledEdgeProposer>
    // class PyLabeledEdgeProposer: public PyEdgeProposer<BaseClass>{
    // public:
    //     using PyEdgeProposer<BaseClass>::PyEdgeProposer;
    //     ~PyLabeledEdgeProposer() override = default;
    //
    //     /* Pure abstract methods */
    //
    //     /* Abstract & overloaded methods */
    //     void setUp( const RandomGraph& randomGraph ) override { PYBIND11_OVERRIDE(void, BaseClass, setUp, randomGraph); }
    //     void setUpFromGraph(const MultiGraph& graph) override { PYBIND11_OVERRIDE(void, BaseClass, setUpFromGraph, graph); }
    //     void onLabelCreation(const BlockMove& move) override { PYBIND11_OVERRIDE(void, BaseClass, onLabelCreation, move); }
    //     void onLabelDeletion(const BlockMove& move) override { PYBIND11_OVERRIDE(void, BaseClass, onLabelDeletion, move); }
    //     void clear() override { PYBIND11_OVERRIDE(void, BaseClass, clear, ); }
    // };
    //
    //
    //
    // template<typename BaseClass = LabeledHingeFlipProposer>
    // class PyLabeledHingeFlipProposer: public PyEdgeProposer<BaseClass>{
    // public:
    //     using PyEdgeProposer<BaseClass>::PyEdgeProposer;
    //     ~PyLabeledHingeFlipProposer() override = default;
    //
    //     /* Pure abstract methods */
    //     VertexSampler* constructVertexSampler() const override { PYBIND11_OVERRIDE_PURE(VertexSampler*, BaseClass, constructVertexSampler, ); }
    //
    //     /* Abstract & overloaded methods */
    // };

}

#endif
