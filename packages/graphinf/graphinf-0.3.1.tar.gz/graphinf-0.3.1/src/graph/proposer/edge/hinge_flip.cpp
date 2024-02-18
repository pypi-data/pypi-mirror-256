#include "GraphInf/utility/functions.h"
#include "GraphInf/rng.h"
#include "GraphInf/graph/proposer/edge/hinge_flip.h"

namespace GraphInf
{

    const GraphMove HingeFlipProposer::proposeRawMove() const
    {
        auto edge = m_edgeSampler.sample();
        if (m_edgeProposalCounter.count(edge) == 0)
            m_edgeProposalCounter.insert({edge, 0});
        ++m_edgeProposalCounter[edge];

        BaseGraph::VertexIndex vertex = m_vertexSamplerPtr->sample();
        if (m_vertexProposalCounter.count(vertex) == 0)
            m_vertexProposalCounter.insert({vertex, 0});
        ++m_vertexProposalCounter[vertex];

        BaseGraph::Edge newEdge;
        if (m_flipOrientationDistribution(rng))
        {
            newEdge = {edge.first, vertex};
            edge = {edge.first, edge.second};
        }
        else
        {
            newEdge = {edge.second, vertex};
            edge = {edge.second, edge.first};
        }

        if (m_edgeSampler.contains(edge) and m_graphPtr->getEdgeMultiplicity(edge.first, edge.second) == 0)
            throw std::logic_error("HingeFlipProposer: Edge (" + std::to_string(edge.first) + ", " + std::to_string(edge.second) + ") exists in sampler with weight " + std::to_string(m_edgeSampler.getEdgeWeight(edge)) +
                                   ", but with multiplicity 0 in graph.");
        return {{edge}, {newEdge}};
    };

    void HingeFlipProposer::setUpWithGraph(const MultiGraph &graph)
    {
        m_edgeSampler.setUpWithGraph(graph);
        m_vertexSamplerPtr->setUpWithGraph(graph);
        m_graphPtr = &graph;
    }

    void HingeFlipProposer::applyGraphMove(const GraphMove &move)
    {

        for (auto edge : move.removedEdges)
        {
            edge = getOrderedEdge(edge);
            m_vertexSamplerPtr->onEdgeRemoval(edge);
            m_edgeSampler.onEdgeRemoval(edge);
        }
        for (auto edge : move.addedEdges)
        {
            edge = getOrderedEdge(edge);
            m_vertexSamplerPtr->onEdgeAddition(edge);
            m_edgeSampler.onEdgeAddition(edge);
        }
    }

    const double HingeFlipProposer::getLogProposalProbRatio(const GraphMove &move) const
    {
        BaseGraph::VertexIndex i = move.addedEdges[0].first;
        BaseGraph::VertexIndex j = move.removedEdges[0].second;
        BaseGraph::VertexIndex k = move.addedEdges[0].second;

        if (isTrivialMove(move))
        {
            // printf("Trivial move\n");
            return 0;
        }
        if (i == j and i != k)
        {
            // printf("Loopy move\n");
            return getLogPropRatioForLoopyMove(move);
        }
        if ((i == k or j == k) and i != j)
        {
            // printf("Selfie move\n");
            return getLogPropRatioForSelfieMove(move);
        }
        // printf("Normal move\n");
        return getLogPropRatioForNormalMove(move);
    }

    bool HingeFlipProposer::isTrivialMove(const GraphMove &move) const
    {
        const auto &addedEdge = getOrderedEdge(move.addedEdges[0]);
        const auto &removedEdge = getOrderedEdge(move.removedEdges[0]);

        if (addedEdge == removedEdge)
            return true;
        return false;
    }

    const double HingeFlipProposer::getLogPropRatioForNormalMove(const GraphMove &move) const
    {
        auto addedEdge = getOrderedEdge(move.addedEdges[0]);
        auto removedEdge = getOrderedEdge(move.removedEdges[0]);
        double addedEdgeWeight = m_edgeSampler.getEdgeWeight(addedEdge);
        double removedEdgeWeight = m_edgeSampler.getEdgeWeight(removedEdge);
        return log(addedEdgeWeight + 1) - log(removedEdgeWeight) + getLogVertexWeightRatio(move);
    }

    const double HingeFlipProposer::getLogPropRatioForLoopyMove(const GraphMove &move) const
    {
        return getLogPropRatioForNormalMove(move) - log(2);
    }

    const double HingeFlipProposer::getLogPropRatioForSelfieMove(const GraphMove &move) const
    {
        return getLogPropRatioForNormalMove(move) + log(2);
    }

} // namespace GraphInf
