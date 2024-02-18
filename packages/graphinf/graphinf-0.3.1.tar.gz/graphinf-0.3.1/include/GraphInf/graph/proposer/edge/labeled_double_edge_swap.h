#ifndef GRAPH_INF_LABELED_DOUBLE_EDGE_SWAP_H
#define GRAPH_INF_LABELED_DOUBLE_EDGE_SWAP_H

#include <unordered_map>
#include "SamplableSet.hpp"
#include "hash_specialization.hpp"
#include "labeled_edge_proposer.h"
#include "GraphInf/graph/proposer/sampler/edge_sampler.h"
#include "GraphInf/utility/functions.h"

namespace GraphInf
{

    class LabeledDoubleEdgeSwapProposer : public LabeledEdgeProposer
    {
        // private:
        //     mutable std::bernoulli_distribution m_swapOrientationDistribution = std::bernoulli_distribution(.5);
        // protected:
        //     std::unordered_map<LabelPair, EdgeSampler*> m_labeledEdgeSampler;
        // public:
        //     LabeledDoubleEdgeSwapProposer(bool allowSelfLoops=true, bool allowMultiEdges=true, double labelPairShift=1):
        //         LabeledEdgeProposer(allowSelfLoops, allowMultiEdges, labelPairShift) { }
        //     virtual ~LabeledDoubleEdgeSwapProposer(){ clear(); }
        //     const GraphMove proposeRawMove() const override ;
        //     void setUpFromGraph(const MultiGraph& graph) override ;
        //     const double getLogProposalProbRatio(const GraphMove& move) const override { return 0; }
        //     void applyGraphMove(const GraphMove& move) override ;
        //     void applyBlockMove(const BlockMove& move) override ;
        //     size_t getTotalEdgeCount() const ;
        //     void clear(){
        //         LabeledEdgeProposer::clear();
        //         for (auto p : m_labeledEdgeSampler)
        //             delete p.second;
        //         m_labeledEdgeSampler.clear();
        //     }
    };

} // namespace GraphInf

#endif
