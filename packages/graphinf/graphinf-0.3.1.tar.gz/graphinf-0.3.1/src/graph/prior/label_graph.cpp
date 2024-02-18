#include <string>
#include <vector>

#include "GraphInf/graph/prior/label_graph.h"
#include "GraphInf/exceptions.h"
#include "GraphInf/utility/functions.h"
#include "GraphInf/utility/maps.hpp"
#include "GraphInf/generators.h"

namespace GraphInf
{

    /* DEFINITION OF EDGE MATRIX PRIOR BASE CLASS */
    void LabelGraphPrior::recomputeConsistentState()
    {
        m_edgeCounts = computeEdgeCountsFromState(m_state);
        m_edgeCountPriorPtr->setState(m_state.getTotalEdgeNumber());
    }
    void LabelGraphPrior::recomputeStateFromGraph()
    {
        if (m_graphPtr->getSize() != m_blockPriorPtr->getSize())
        {
            // m_blockPriorPtr->setSize(m_graphPtr->getSize());
            // m_blockPriorPtr->sample();
            throw ConsistencyError(
                "LabelGraphPrior",
                "m_graphPtr->getSize()", std::to_string(m_graphPtr->getSize()),
                "m_blockPriorPtr->getSize()", std::to_string(m_blockPriorPtr->getSize()));
        }

        MultiGraph state(m_blockPriorPtr->getMaxBlockCount());
        for (const auto &edge : m_graphPtr->edges())
        {
            state.addMultiedge(
                m_blockPriorPtr->getBlock(edge.first), m_blockPriorPtr->getBlock(edge.second), m_graphPtr->getEdgeMultiplicity(edge.first, edge.second));
        }
        setState(state);
    }

    void LabelGraphPrior::setGraph(const MultiGraph &graph)
    {
        m_graphPtr = &graph;
        recomputeStateFromGraph();
    }

    void LabelGraphPrior::setPartition(const std::vector<BlockIndex> &labels)
    {
        m_blockPriorPtr->setState(labels);
        recomputeStateFromGraph();
    }

    void LabelGraphPrior::setState(const MultiGraph &labelGraph)
    {
        m_state = MultiGraph(labelGraph);
        recomputeConsistentState();
    }

    void LabelGraphPrior::applyLabelMoveToState(const BlockMove &move)
    {
        const auto &blockSeq = m_blockPriorPtr->getState();
        const auto &degree = m_graphPtr->getDegree(move.vertexIndex);

        if (m_state.getSize() <= move.nextLabel)
            m_state.resize(move.nextLabel + 1);

        m_edgeCounts.decrement(move.prevLabel, degree);
        m_edgeCounts.increment(move.nextLabel, degree);
        for (auto neighbor : m_graphPtr->getOutNeighbours(move.vertexIndex))
        {
            auto neighborBlock = blockSeq[neighbor];
            const auto mult = m_graphPtr->getEdgeMultiplicity(move.vertexIndex, neighbor);

            if (move.vertexIndex == neighbor) // for self-loops
                neighborBlock = move.prevLabel;
            m_state.removeMultiedge(move.prevLabel, neighborBlock, mult);

            if (move.vertexIndex == neighbor) // for self-loops
                neighborBlock = move.nextLabel;
            m_state.addMultiedge(move.nextLabel, neighborBlock, mult);
        }
    }

    void LabelGraphPrior::applyGraphMoveToState(const GraphMove &move)
    {
        const auto &blockSeq = m_blockPriorPtr->getState();

        for (auto removedEdge : move.removedEdges)
        {
            const BlockIndex &r(blockSeq[removedEdge.first]), s(blockSeq[removedEdge.second]);
            m_state.removeEdge(r, s);
            m_edgeCounts.decrement(r);
            m_edgeCounts.decrement(s);
        }
        for (auto addedEdge : move.addedEdges)
        {
            const BlockIndex &r(blockSeq[addedEdge.first]), s(blockSeq[addedEdge.second]);
            m_state.addEdge(r, s);
            m_edgeCounts.increment(r);
            m_edgeCounts.increment(s);
        }
    }

    void LabelGraphPrior::checkSelfConsistency() const
    {
        m_blockPriorPtr->checkSelfConsistency();
        m_edgeCountPriorPtr->checkSelfConsistency();

        for (BlockIndex r : m_state)
        {
            if (m_state.getDegree(r) != m_edgeCounts[r])
                throw ConsistencyError(
                    "LabelGraphPrior",
                    "m_state.degree", std::to_string(m_state.getDegree(r)),
                    "m_edgeCounts", std::to_string(m_edgeCounts[r]),
                    "r=" + std::to_string(r));
        }
        if (m_state.getTotalEdgeNumber() != m_edgeCountPriorPtr->getState())
            throw ConsistencyError(
                "LabelGraphPrior",
                "m_state.edgeCount", std::to_string(m_state.getTotalEdgeNumber()),
                "m_edgeCountPriorPtr", std::to_string(m_edgeCountPriorPtr->getState()));
    }

    const double LabelGraphDeltaPrior::getLogLikelihoodRatioFromGraphMove(const GraphMove &move) const
    {
        CounterMap<std::pair<BlockIndex, BlockIndex>> map;

        for (auto edge : move.addedEdges)
        {
            BlockIndex r = m_blockPriorPtr->getBlock(edge.first);
            BlockIndex s = m_blockPriorPtr->getBlock(edge.second);
            map.decrement({r, s});
            map.decrement({s, r});
        }
        for (auto edge : move.addedEdges)
        {
            BlockIndex r = m_blockPriorPtr->getBlock(edge.first);
            BlockIndex s = m_blockPriorPtr->getBlock(edge.second);
            map.increment({r, s});
            map.increment({s, r});
        }

        for (auto k : map)
        {
            if (k.second != 0)
                return -INFINITY;
        }
        return 0.;
    }

    const double LabelGraphDeltaPrior::getLogLikelihoodRatioFromLabelMove(const BlockMove &move) const
    {
        if (move.prevLabel != move.nextLabel)
            return -INFINITY;
        return 0.;
    }

    /* DEFINITION OF EDGE MATRIX UNIFORM PRIOR */

    void LabelGraphErdosRenyiPrior::sampleState()
    {
        LabelGraph labelGraph(m_blockPriorPtr->getMaxBlockCount());

        std::vector<std::pair<BlockIndex, BlockIndex>> allEdges;

        for (auto nr : m_blockPriorPtr->getVertexCounts())
        {
            if (nr.second == 0)
                continue;
            for (auto ns : m_blockPriorPtr->getVertexCounts())
            {
                if (ns.second == 0 or nr.first > ns.first)
                    continue;
                allEdges.push_back({nr.first, ns.first});
            }
        }

        auto edgeMultiplicities = sampleRandomWeakComposition(getEdgeCount(), allEdges.size());

        size_t counter = 0;
        for (auto m : edgeMultiplicities)
        {
            if (m != 0)
                labelGraph.addMultiedge(allEdges[counter].first, allEdges[counter].second, m);
            ++counter;
        }

        setState(labelGraph);
    }

    const double LabelGraphErdosRenyiPrior::getLogLikelihoodRatioFromGraphMove(const GraphMove &move) const
    {
        double currentLogLikelihood = getLogLikelihood(m_blockPriorPtr->getEffectiveBlockCount(), m_edgeCountPriorPtr->getState());
        double newLogLikelihood = getLogLikelihood(m_blockPriorPtr->getEffectiveBlockCount(), m_edgeCountPriorPtr->getState() + move.addedEdges.size() - move.removedEdges.size());
        return newLogLikelihood - currentLogLikelihood;
    }

    const double LabelGraphErdosRenyiPrior::getLogLikelihoodRatioFromLabelMove(const BlockMove &move) const
    {
        double currentLogLikelihood = getLogLikelihood(
            m_blockPriorPtr->getEffectiveBlockCount(), m_edgeCountPriorPtr->getState());
        double newLogLikelihood = getLogLikelihood(
            m_blockPriorPtr->getEffectiveBlockCount() + m_blockPriorPtr->getAddedBlocks(move), m_edgeCountPriorPtr->getState());
        return newLogLikelihood - currentLogLikelihood;
    }

    void LabelGraphPlantedPartitionPrior::recomputeConsistentState()
    {
        LabelGraphPrior::recomputeConsistentState();
        m_edgeCountIn = 0, m_edgeCountOut = 0;
        // if (m_blockPriorPtr->getEffectiveBlockCount() == 1){
        //     m_edgeCountIn = getEdgeCount();
        //     return;
        // }
        for (size_t r = 0; r < m_state.getSize(); ++r)
        {
            m_edgeCountIn += m_state.getEdgeMultiplicity(r, r);
            for (size_t s = r + 1; s < m_state.getSize(); ++s)
            {
                m_edgeCountOut += m_state.getEdgeMultiplicity(r, s);
            }
        }
    }

    void LabelGraphPlantedPartitionPrior::applyGraphMoveToState(const GraphMove &move)
    {
        LabelGraphPrior::applyGraphMoveToState(move);
        for (auto edge : move.addedEdges)
        {
            BlockIndex r = getBlock(edge.first), s = getBlock(edge.second);
            if (r == s)
                ++m_edgeCountIn;
            else
                ++m_edgeCountOut;
        }
        for (auto edge : move.removedEdges)
        {
            BlockIndex r = getBlock(edge.first), s = getBlock(edge.second);
            if (r == s)
                --m_edgeCountIn;
            else
                --m_edgeCountOut;
        }
    }

    void LabelGraphPlantedPartitionPrior::applyLabelMoveToState(const BlockMove &move)
    {
        LabelGraphPrior::applyLabelMoveToState(move);
        for (auto neighbor : m_graphPtr->getOutNeighbours(move.vertexIndex))
        {
            BlockIndex t = getBlock(neighbor);

            const auto mult = m_graphPtr->getEdgeMultiplicity(move.vertexIndex, neighbor);
            if (move.prevLabel == t or move.vertexIndex == neighbor)
                m_edgeCountIn -= mult;
            else
                m_edgeCountOut -= mult;

            if (move.nextLabel == t or move.vertexIndex == neighbor)
                m_edgeCountIn += mult;
            else
                m_edgeCountOut += mult;
        }
    }

    void LabelGraphPlantedPartitionPrior::sampleState()
    {
        std::uniform_int_distribution<size_t> dist(0, getEdgeCount());
        size_t Beff = m_blockPriorPtr->getEffectiveBlockCount(), B = m_blockPriorPtr->getMaxBlockCount();
        size_t E_in, E_out;
        if (Beff > 1)
        {
            E_in = dist(rng);
            E_out = getEdgeCount() - E_in;
        }
        else
        {
            E_in = getEdgeCount();
            E_out = 0;
        }
        std::vector<size_t> e_in = sampleUniformMultinomial(E_in, Beff), e_out;
        if (Beff > 1)
            e_out = sampleUniformMultinomial(E_out, Beff * (Beff - 1) / 2);

        LabelGraph labelGraph(B);

        size_t i = 0, j = 0;
        for (size_t r = 0; r < B; ++r)
        {
            if (m_blockPriorPtr->getVertexCounts().get(r) == 0)
                continue;
            labelGraph.addMultiedge(r, r, e_in[i++]);
            for (size_t s = r + 1; s < B; ++s)
            {
                if (m_blockPriorPtr->getVertexCounts().get(s) == 0 or e_out.size() == 0)
                    continue;
                labelGraph.addMultiedge(r, s, e_out[j++]);
            }
        }
        setState(labelGraph);
    }

    const double LabelGraphPlantedPartitionPrior::getLogLikelihood() const
    {
        size_t E = getEdgeCount(), B = m_blockPriorPtr->getEffectiveBlockCount();
        double logLikelihood = logFactorial(m_edgeCountIn) - m_edgeCountIn * log(B);
        if (B > 1)
        {
            logLikelihood += logFactorial(m_edgeCountOut) - m_edgeCountOut * log(B * (B - 1) / 2);
            logLikelihood += -log(E + 1);
        }

        for (size_t r = 0; r < B; ++r)
        {
            logLikelihood -= logFactorial(m_state.getEdgeMultiplicity(r, r));
            for (size_t s = r + 1; s < B; ++s)
            {
                logLikelihood -= logFactorial(m_state.getEdgeMultiplicity(r, s));
            }
        }
        return logLikelihood;
    }

    const double LabelGraphPlantedPartitionPrior::getLogLikelihoodRatioFromGraphMove(const GraphMove &move) const
    {
        size_t E = getEdgeCount(), B = getBlockCount();
        if (B == 1)
            return 0;
        int dEin = 0, dEout = 0, dE = move.addedEdges.size() - move.removedEdges.size();
        IntMap<BaseGraph::Edge> edgeCountDiff;
        for (auto edge : move.addedEdges)
        {
            BlockIndex r = getBlock(edge.first), s = getBlock(edge.second);
            if (r == s)
                ++dEin;
            else
                ++dEout;
            edgeCountDiff.increment(getOrderedEdge({r, s}));
        }
        for (auto edge : move.removedEdges)
        {
            BlockIndex r = getBlock(edge.first), s = getBlock(edge.second);
            if (r == s)
                --dEin;
            else
                --dEout;
            edgeCountDiff.decrement(getOrderedEdge({r, s}));
        }

        double ratio = 0;

        ratio += (B == 1) ? 0 : log(E + 1) - log(E + dE + 1);

        ratio += logFactorial(m_edgeCountIn + dEin) - (m_edgeCountIn + dEin) * log(B);
        ratio -= logFactorial(m_edgeCountIn) - (m_edgeCountIn)*log(B);

        if (B > 1)
        {
            ratio += logFactorial(m_edgeCountOut + dEout) - (m_edgeCountOut + dEout) * log(B * (B - 1) / 2);
            ratio -= logFactorial(m_edgeCountOut) - (m_edgeCountOut)*log(B * (B - 1) / 2);
        }

        for (const auto &diff : edgeCountDiff)
        {
            const auto &rs = diff.first;
            size_t ers = m_state.getEdgeMultiplicity(rs.first, rs.second);
            ratio -= logFactorial(ers + diff.second) - logFactorial(ers);
        }
        return ratio;
    }

    const double LabelGraphPlantedPartitionPrior::getLogLikelihoodRatioFromLabelMove(const BlockMove &move) const
    {
        size_t E = getEdgeCount(), B = getBlockCount();
        int dEin = 0, dEout = 0;
        IntMap<BaseGraph::Edge> edgeCountDiff;
        for (auto neighbor : m_graphPtr->getOutNeighbours(move.vertexIndex))
        {
            BlockIndex t = getBlock(neighbor);
            const auto mult = m_graphPtr->getEdgeMultiplicity(move.vertexIndex, neighbor);

            if (move.prevLabel == t)
                dEin -= mult;
            else
                dEout -= mult;
            edgeCountDiff.decrement(getOrderedEdge({move.prevLabel, t}), mult);

            t = (move.vertexIndex == neighbor) ? move.nextLabel : t;
            if (move.nextLabel == t)
                dEin += mult;
            else
                dEout += mult;
            edgeCountDiff.increment(getOrderedEdge({move.nextLabel, t}), mult);
        }

        double ratio = 0;
        size_t nextB = B + move.addedLabels;

        ratio += logFactorial(m_edgeCountIn + dEin) - (m_edgeCountIn + dEin) * log(nextB);
        ratio -= logFactorial(m_edgeCountIn) - (m_edgeCountIn)*log(B);
        ratio += logFactorial(m_edgeCountOut + dEout) - ((nextB == 1) ? 0 : ((m_edgeCountOut + dEout) * log(nextB * (nextB - 1) / 2)));
        ratio -= logFactorial(m_edgeCountOut) - ((B == 1) ? 0 : ((m_edgeCountOut)*log(B * (B - 1) / 2)));

        for (const auto &diff : edgeCountDiff)
        {
            const auto &rs = diff.first;
            size_t ers;
            if (rs.first < m_state.getSize() and rs.second < m_state.getSize())
                ers = m_state.getEdgeMultiplicity(rs.first, rs.second);
            else
                ers = 0;
            ratio -= logFactorial(ers + diff.second) - logFactorial(ers);
        }
        return ratio;
    }

    void LabelGraphPlantedPartitionPrior::checkSelfConsistency() const
    {
        LabelGraphPrior::checkSelfConsistency();
        if (m_edgeCountIn + m_edgeCountOut != getEdgeCount())
            throw ConsistencyError(
                "LabelGraphPlantedPartitionPrior",
                "(m_edgeCountIn, m_edgeCountOut)", "value=(" + std::to_string(m_edgeCountIn) + ", " + std::to_string(m_edgeCountIn) + ")",
                "m_edgeCountPriorPtr", "value=" + std::to_string(getEdgeCount()));
        size_t actualEdgeCountIn = 0, actualEdgeCountOut = 0;
        for (const auto vertex : *m_graphPtr)
        {
            actualEdgeCountIn += m_graphPtr->getEdgeMultiplicity(vertex, vertex);

            for (const auto &neighbor : m_graphPtr->getOutNeighbours(vertex))
            {
                if (vertex >= neighbor)
                    continue;
                BlockIndex r = getBlock(vertex), s = getBlock(neighbor);
                const auto mult = m_graphPtr->getEdgeMultiplicity(vertex, neighbor);
                if (r == s)
                    actualEdgeCountIn += mult;
                else
                    actualEdgeCountOut += mult;
            }
        }

        if (actualEdgeCountIn != m_edgeCountIn)
            throw ConsistencyError(
                "LabelGraphPlantedPartitionPrior",
                "m_edgeCountIn", "value=" + std::to_string(m_edgeCountIn),
                "m_graphPtr", "value=" + std::to_string(actualEdgeCountIn));
        if (actualEdgeCountOut != m_edgeCountOut)
            throw ConsistencyError(
                "LabelGraphPlantedPartitionPrior",
                "m_edgeCountOut", "value=" + std::to_string(m_edgeCountOut),
                "m_graphPtr", "value=" + std::to_string(actualEdgeCountOut));

        actualEdgeCountIn = actualEdgeCountOut = 0;
        for (size_t r = 0; r < m_state.getSize(); ++r)
        {
            actualEdgeCountIn += m_state.getEdgeMultiplicity(r, r);
            for (size_t s = r + 1; s < m_state.getSize(); ++s)
            {
                actualEdgeCountOut += m_state.getEdgeMultiplicity(r, s);
            }
        }

        if (actualEdgeCountIn != m_edgeCountIn)
            throw ConsistencyError(
                "LabelGraphPlantedPartitionPrior",
                "m_edgeCountIn", "value=" + std::to_string(m_edgeCountIn),
                "m_state", "value=" + std::to_string(actualEdgeCountIn));
        if (actualEdgeCountOut != m_edgeCountOut)
            throw ConsistencyError(
                "LabelGraphPlantedPartitionPrior",
                "m_edgeCountOut", "value=" + std::to_string(m_edgeCountOut),
                "m_state", "value=" + std::to_string(actualEdgeCountOut));
    }

    // /* DEFINITION OF EDGE MATRIX EXPONENTIAL PRIOR */
    //
    // void LabelGraphExponentialPrior::sampleState() {
    //     auto blockCount = m_blockPriorPtr->getBlockCount();
    //     auto flattenedLabelGraph = sampleRandomWeakComposition(
    //             m_edgeCountPriorPtr->getState(),
    //             blockCount*(blockCount+1)/2
    //             );
    //
    //     m_state = LabelGraph(blockCount, std::vector<size_t>(blockCount, 0));
    //     std::pair<BlockIndex, BlockIndex> rs;
    //     m_edgeCounts = std::vector<size_t>(blockCount, 0);
    //     size_t index = 0, correctedEdgeCount;
    //     for (auto edgeCountBetweenBlocks: flattenedLabelGraph) {
    //         rs = getUndirectedPairFromIndex(index, blockCount);
    //         m_edgeCounts[rs.first] += edgeCountBetweenBlocks;
    //         m_edgeCounts[rs.second] += edgeCountBetweenBlocks;
    //         m_state[rs.first][rs.second] += edgeCountBetweenBlocks;
    //         m_state[rs.second][rs.first] += edgeCountBetweenBlocks;
    //         index++;
    //     }
    // }
    //
    // double LabelGraphExponentialPrior::getLogLikelihoodRatioFromGraphMove(const GraphMove& move) const {
    //     double currentLogLikelihood =  getLogLikelihood(m_blockPriorPtr->getBlockCount(), m_edgeCountPriorPtr->getState());
    //     double newLogLikelihood =  getLogLikelihood(m_blockPriorPtr->getBlockCount(), m_edgeCountPriorPtr->getState() + move.addedEdges.size() - move.removedEdges.size());
    //     return newLogLikelihood - currentLogLikelihood;
    // }
    //
    // double LabelGraphExponentialPrior::getLogLikelihoodRatioFromLabelMove(const BlockMove& move) const {
    //     auto vertexCounts = m_blockPriorPtr->getVertexCounts();
    //
    //     bool creatingBlock = move.nextLabel == m_blockPriorPtr->getBlockCount();
    //     bool destroyingBlock = move.nextLabel != move.prevLabel &&
    //                         vertexCounts[move.prevLabel] == 1;
    //     double currentLogLikelihood =  getLogLikelihood(m_blockPriorPtr->getBlockCount(), m_edgeCountPriorPtr->getState());
    //     double newLogLikelihood =  getLogLikelihood(m_blockPriorPtr->getBlockCount() + creatingBlock - destroyingBlock, m_edgeCountPriorPtr->getState());
    //     return newLogLikelihood - currentLogLikelihood;
    // }

} // namespace GraphInf
