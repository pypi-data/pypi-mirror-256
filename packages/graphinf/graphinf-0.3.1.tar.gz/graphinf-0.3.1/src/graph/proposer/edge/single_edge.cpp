#include "GraphInf/utility/functions.h"
#include "GraphInf/rng.h"
#include "GraphInf/graph/proposer/edge/single_edge.h"

namespace GraphInf
{

    const GraphMove SingleEdgeProposer::proposeRawMove() const
    {
        auto vertex1 = m_vertexSamplerPtr->sample();
        auto vertex2 = m_vertexSamplerPtr->sample();

        BaseGraph::Edge proposedEdge = {vertex1, vertex2};

        if (not m_graphPtr->hasEdge(vertex1, vertex2))
            return {{}, {proposedEdge}};

        if (m_addOrRemoveDistribution(rng))
            return {{}, {proposedEdge}};
        return {{proposedEdge}, {}};
    }

    void SingleEdgeProposer::setUpWithGraph(const MultiGraph &graph)
    {
        m_graphPtr = &graph;
        for (auto vertex : graph)
        {
            m_vertexSamplerPtr->onVertexInsertion(vertex);
            for (auto neighbor : graph.getOutNeighbours(vertex))
            {
                const auto mult = graph.getEdgeMultiplicity(vertex, neighbor);
                if (vertex <= neighbor)
                    m_vertexSamplerPtr->onEdgeInsertion({vertex, neighbor}, mult);
            }
        }
    }

    const double SingleEdgeUniformProposer::getLogProposalProbRatio(const GraphMove &move) const
    {
        double logProbability = 0;

        for (auto edge : move.removedEdges)
            if (m_graphPtr->getEdgeMultiplicity(edge.first, edge.second) == 1)
                logProbability += log(.5);

        for (auto edge : move.addedEdges)
            if (m_graphPtr->getEdgeMultiplicity(edge.first, edge.second) == 0)
                logProbability -= log(.5);
        return logProbability;
    }

    void SingleEdgeDegreeProposer::applyGraphMove(const GraphMove &move)
    {
        for (auto edge : move.removedEdges)
            m_vertexDegreeSampler.onEdgeRemoval(edge);
        for (auto edge : move.addedEdges)
            m_vertexDegreeSampler.onEdgeAddition(edge);
    }

    const double SingleEdgeDegreeProposer::getGammaRatio(BaseGraph::Edge edge, const double difference) const
    {
        double gamma = 0;
        gamma += log(m_vertexDegreeSampler.getVertexWeight(edge.first) + difference);
        gamma += log(m_vertexDegreeSampler.getVertexWeight(edge.second) + difference);
        gamma -= log(m_vertexDegreeSampler.getTotalWeight() + difference);

        gamma -= log(m_vertexDegreeSampler.getVertexWeight(edge.first));
        gamma -= log(m_vertexDegreeSampler.getVertexWeight(edge.second));
        gamma += log(m_vertexDegreeSampler.getTotalWeight());

        return gamma;
    }

    const double SingleEdgeDegreeProposer::getLogProposalProbRatio(const GraphMove &move) const
    {
        double logRatio = 0;

        for (auto edge : move.removedEdges)
        {
            logRatio += getGammaRatio(edge, -1);
            if (m_graphPtr->getEdgeMultiplicity(edge.first, edge.second) == 1)
                logRatio += -log(.5);
        }
        for (auto edge : move.addedEdges)
        {
            logRatio += getGammaRatio(edge, 1);
            if (m_graphPtr->getEdgeMultiplicity(edge.first, edge.second) == 0)
                logRatio += -log(.5);
        }
        return logRatio;
    }

} // namespace GraphInf
