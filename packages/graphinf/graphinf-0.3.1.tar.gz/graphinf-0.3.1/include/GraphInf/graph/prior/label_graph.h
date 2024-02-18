#ifndef GRAPH_INF_LABEL_GRAPH_H
#define GRAPH_INF_LABEL_GRAPH_H

#include "prior.hpp"
#include "edge_count.h"
#include "block.h"
#include "GraphInf/graph/proposer/movetypes.h"
#include "GraphInf/types.h"
#include "GraphInf/exceptions.h"
#include "GraphInf/utility/functions.h"
#include "GraphInf/utility/maps.hpp"
#include "GraphInf/generators.h"

namespace GraphInf
{

    class LabelGraphPrior : public BlockLabeledPrior<LabelGraph>
    {
    protected:
        EdgeCountPrior *m_edgeCountPriorPtr = nullptr;
        BlockPrior *m_blockPriorPtr = nullptr;
        CounterMap<BlockIndex> m_edgeCounts;
        const MultiGraph *m_graphPtr;

        void _samplePriors() override
        {
            m_edgeCountPriorPtr->sample();
            m_blockPriorPtr->sample();
        }
        const double _getLogPrior() const override { return m_edgeCountPriorPtr->getLogJoint() + m_blockPriorPtr->getLogJoint(); }

        void _applyGraphMove(const GraphMove &move) override
        {
            m_edgeCountPriorPtr->applyGraphMove(move);
            m_blockPriorPtr->applyGraphMove(move);
            applyGraphMoveToState(move);
        }
        void _applyLabelMove(const BlockMove &move) override
        {
            if (move.prevLabel == move.nextLabel)
                return;

            applyLabelMoveToState(move);
            m_blockPriorPtr->applyLabelMove(move);

            // if (move.addedLabels==-1){
            //     destroyBlock(move);
            // }
        }

        // virtual void destroyBlock(const BlockMove&move){ }

        const double _getLogPriorRatioFromGraphMove(const GraphMove &move) const override
        {
            return m_edgeCountPriorPtr->getLogJointRatioFromGraphMove(move) + m_blockPriorPtr->getLogJointRatioFromGraphMove(move);
        }
        const double _getLogPriorRatioFromLabelMove(const BlockMove &move) const override
        {
            return m_blockPriorPtr->getLogJointRatioFromLabelMove(move);
        }

        virtual void applyGraphMoveToState(const GraphMove &);
        virtual void applyLabelMoveToState(const BlockMove &);
        virtual void recomputeStateFromGraph();
        CounterMap<BlockIndex> computeEdgeCountsFromState(const LabelGraph &state)
        {
            CounterMap<BlockIndex> edgeCounts;
            for (auto v : state)
                edgeCounts.set(v, state.getDegree(v));
            return edgeCounts;
        }
        virtual void recomputeConsistentState();

    public:
        LabelGraphPrior() {}
        LabelGraphPrior(EdgeCountPrior &edgeCountPrior, BlockPrior &blockPrior)
        {
            setEdgeCountPrior(edgeCountPrior);
            setBlockPrior(blockPrior);
        }
        LabelGraphPrior(const LabelGraphPrior &other)
        {
            setEdgeCountPrior(*other.m_edgeCountPriorPtr);
            setBlockPrior(*other.m_blockPriorPtr);
        }
        const LabelGraphPrior &operator=(const LabelGraphPrior &other)
        {
            setEdgeCountPrior(*other.m_edgeCountPriorPtr);
            setBlockPrior(*other.m_blockPriorPtr);
            return *this;
        }

        const EdgeCountPrior &getEdgeCountPrior() const { return *m_edgeCountPriorPtr; }
        EdgeCountPrior &getEdgeCountPriorRef() const { return *m_edgeCountPriorPtr; }
        void setEdgeCountPrior(EdgeCountPrior &edgeCountPrior)
        {
            m_edgeCountPriorPtr = &edgeCountPrior;
            m_edgeCountPriorPtr->isRoot(false);
        }
        const BlockPrior &getBlockPrior() const { return *m_blockPriorPtr; }
        BlockPrior &getBlockPriorRef() const { return *m_blockPriorPtr; }
        void setBlockPrior(BlockPrior &blockPrior)
        {
            m_blockPriorPtr = &blockPrior;
            m_blockPriorPtr->isRoot(false);
        }

        void setGraph(const MultiGraph &graph);
        const MultiGraph &getGraph() { return *m_graphPtr; }
        void setState(const LabelGraph &) override;
        virtual void setPartition(const std::vector<BlockIndex> &);
        void samplePartition()
        {
            m_blockPriorPtr->sample();
            recomputeStateFromGraph();
        }

        const size_t &getEdgeCount() const { return m_edgeCountPriorPtr->getState(); }
        const CounterMap<BlockIndex> &getEdgeCounts() const { return m_edgeCounts; }

        const size_t getBlockCount() const
        {
            return m_blockPriorPtr->getBlockCount();
        }
        const std::vector<BlockIndex> getBlocks() const
        {
            return m_blockPriorPtr->getState();
        }
        const BlockIndex getBlock(BaseGraph::VertexIndex vertex) const
        {
            return m_blockPriorPtr->getBlock(vertex);
        }

        virtual const double getLogLikelihoodRatioFromGraphMove(const GraphMove &) const override = 0;
        virtual const double getLogLikelihoodRatioFromLabelMove(const BlockMove &) const override = 0;

        virtual void reducePartition()
        {
            m_blockPriorPtr->reduceState();
            recomputeStateFromGraph();
        }

        bool isSafe() const override
        {
            return (m_blockPriorPtr != nullptr) and (m_blockPriorPtr->isSafe()) and (m_edgeCountPriorPtr != nullptr) and (m_edgeCountPriorPtr->isSafe());
        }
        void computationFinished() const override
        {
            m_isProcessed = false;
            m_blockPriorPtr->computationFinished();
            m_edgeCountPriorPtr->computationFinished();
        }
        void checkSelfConsistencywithGraph() const;
        virtual void checkSelfConsistency() const override;

        void checkSelfSafety() const override
        {
            if (m_blockPriorPtr == nullptr)
                throw SafetyError("LabelGraphPrior", "m_blockPriorPtr");
            if (m_edgeCountPriorPtr == nullptr)
                throw SafetyError("LabelGraphPrior", "m_edgeCountPriorPtr");
            m_blockPriorPtr->checkSafety();
            m_edgeCountPriorPtr->checkSafety();
        }
    };

    class LabelGraphDeltaPrior : public LabelGraphPrior
    {
    public:
        LabelGraph m_labelGraph;
        BlockDeltaPrior m_blockDeltaPrior;
        EdgeCountDeltaPrior m_edgeCountDeltaPrior;
        void recomputeConsistentState() override
        {
            m_labelGraph.clearEdges();
            m_labelGraph.resize(m_state.getSize());
            for (const auto &rs : m_state.edges())
                m_labelGraph.addMultiedge(rs.first, rs.second, m_state.getEdgeMultiplicity(rs.first, rs.second));
        }

    public:
        LabelGraphDeltaPrior() {}
        LabelGraphDeltaPrior(const std::vector<BlockIndex> &blocks, const LabelGraph &labelGraph) : LabelGraphPrior(),
                                                                                                    m_blockDeltaPrior(blocks), m_edgeCountDeltaPrior(labelGraph.getTotalEdgeNumber()), m_labelGraph(0)
        {
            setEdgeCountPrior(m_edgeCountDeltaPrior);
            setBlockPrior(m_blockDeltaPrior);
            setState(labelGraph);
        }
        LabelGraphDeltaPrior(const LabelGraphDeltaPrior &other) : LabelGraphPrior(other),
                                                                  m_blockDeltaPrior(other.getBlocks()), m_labelGraph(0)
        {
            setState(other.getState());
        }
        virtual ~LabelGraphDeltaPrior() {}
        const LabelGraphDeltaPrior &operator=(const LabelGraphDeltaPrior &other)
        {
            this->setState(other.getState());
            return *this;
        }
        void sampleState() override{};

        const double getLogLikelihood() const override { return 0.; }

        const double getLogLikelihoodRatioFromGraphMove(const GraphMove &move) const override;
        const double getLogLikelihoodRatioFromLabelMove(const BlockMove &move) const override;

        void checkSelfConsistency() const override{};
        void checkSelfSafety() const override
        {
            if (m_labelGraph.getSize() == 0)
                throw SafetyError("LabelGraphDeltaPrior", "m_labelGraph", "empty");
        }

        void computationFinished() const override { m_isProcessed = false; }
    };

    class LabelGraphErdosRenyiPrior : public LabelGraphPrior
    {
    public:
        using LabelGraphPrior::LabelGraphPrior;
        void sampleState() override;
        const double getLogLikelihood() const override
        {
            return getLogLikelihood(m_blockPriorPtr->getEffectiveBlockCount(), m_edgeCountPriorPtr->getState());
        }
        const double getLogLikelihoodRatioFromGraphMove(const GraphMove &) const override;
        const double getLogLikelihoodRatioFromLabelMove(const BlockMove &) const override;

    private:
        double getLogLikelihoodRatio(size_t blockCountAfter, size_t edgeNumberAfter) const
        {
            return getLogLikelihood(blockCountAfter, edgeNumberAfter) - getLogLikelihood(m_edgeCountPriorPtr->getState(), m_blockPriorPtr->getEffectiveBlockCount());
        }
        double getLogLikelihood(size_t blockCount, size_t edgeCount) const
        {
            return -logMultisetCoefficient(blockCount * (blockCount + 1) / 2, edgeCount);
        }
    };

    class LabelGraphPlantedPartitionPrior : public LabelGraphPrior
    {
    protected:
        size_t m_edgeCountIn = 0, m_edgeCountOut = 0;
        void applyGraphMoveToState(const GraphMove &) override;
        void applyLabelMoveToState(const BlockMove &) override;
        void recomputeConsistentState() override;

    public:
        using LabelGraphPrior::LabelGraphPrior;
        void sampleState() override;
        const double getLogLikelihood() const override;
        const double getLogLikelihoodRatioFromGraphMove(const GraphMove &) const override;
        const double getLogLikelihoodRatioFromLabelMove(const BlockMove &) const override;
        void checkSelfConsistency() const override;
        const size_t getEdgeCountIn() const { return m_edgeCountIn; }
        const size_t getEdgeCountOut() const { return m_edgeCountOut; }
    };

    // class LabelGraphExponentialPrior: public LabelGraphPrior {
    // public:
    //
    //     LabelGraphExponentialPrior() {}
    //     LabelGraphExponentialPrior(double edgeCountMean, BlockPrior& blockPrior):
    //         LabelGraphPrior(), m_edgeCountMean(edgeCountMean){
    //         setEdgeCountPrior(*new EdgeCountDeltaPrior(0));
    //         setBlockPrior(blockPrior);
    //     }
    //     LabelGraphExponentialPrior(const LabelGraphExponentialPrior& other){
    //         setEdgeCountPrior(*other.m_edgeCountPriorPtr);
    //         setBlockPrior(*other.m_blockPriorPtr);
    //     }
    //     const LabelGraphExponentialPrior& operator=(const LabelGraphExponentialPrior& other){
    //         setEdgeCountPrior(*other.m_edgeCountPriorPtr);
    //         setBlockPrior(*other.m_blockPriorPtr);
    //         return *this;
    //     }
    //     virtual ~LabelGraphExponentialPrior(){
    //         delete m_edgeCountPriorPtr;
    //     }
    //     void sampleState() override;
    //     double getLogLikelihood() const override {
    //         return getLogLikelihood(m_blockPriorPtr->getBlockCount(), m_edgeCountPriorPtr->getState());
    //     }
    //     double getLogLikelihoodRatioFromGraphMove(const GraphMove&) const override;
    //     double getLogLikelihoodRatioFromLabelMove(const BlockMove&) const override;
    //
    // private:
    //     double m_edgeCountMean;
    //     size_t m_edgeCount;
    //     double getLikelihoodRatio(size_t blockCountAfter, size_t edgeNumberAfter) const {
    //         return getLogLikelihood(m_edgeCountPriorPtr->getState(), m_blockPriorPtr->getBlockCount())
    //             - getLogLikelihood(blockCountAfter, edgeNumberAfter);
    //     }
    //     double getLogLikelihood(size_t blockCount, size_t edgeCount) const {
    //         return edgeCount * log(m_edgeCountMean / (m_edgeCountMean + 1))
    //              - blockCount * (blockCount + 1) / 2 * log(m_edgeCountMean + 1);
    //     }
    // };

} // namespace GraphInf

#endif
