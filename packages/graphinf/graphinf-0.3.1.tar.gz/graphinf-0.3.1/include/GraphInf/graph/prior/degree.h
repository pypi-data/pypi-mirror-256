#ifndef GRAPH_INF_CM_DEGREE_H
#define GRAPH_INF_CM_DEGREE_H

#include <map>
#include "GraphInf/types.h"
#include "prior.hpp"
#include "edge_count.h"
#include "GraphInf/graph/proposer/movetypes.h"
#include "GraphInf/utility/maps.hpp"

namespace GraphInf
{

    class DegreePrior : public Prior<DegreeSequence>
    {
    protected:
        size_t m_size;
        EdgeCountPrior *m_edgeCountPriorPtr = nullptr;
        DegreeCountsMap m_degreeCounts;

        void _samplePriors() override
        {
            m_edgeCountPriorPtr->sample();
        }

        void _applyGraphMove(const GraphMove &move) override;

        const double _getLogPrior() const override
        {
            return m_edgeCountPriorPtr->getLogJoint();
        }
        const double _getLogPriorRatioFromGraphMove(const GraphMove &move) const override
        {
            return m_edgeCountPriorPtr->getLogJointRatioFromGraphMove(move);
        }

        // void onBlockCreation(const BlockMove&) override;

        void applyGraphMoveToState(const GraphMove &);
        void applyGraphMoveToDegreeCounts(const GraphMove &);

    public:
        /* Constructors */
        DegreePrior(size_t graphSize) : m_size(graphSize) {}
        DegreePrior(size_t graphSize, EdgeCountPrior &prior) : m_size(graphSize)
        {
            setEdgeCountPrior(prior);
        }
        DegreePrior(const DegreePrior &other)
        {
            setEdgeCountPrior(*other.m_edgeCountPriorPtr);
        }
        virtual ~DegreePrior() {}
        const DegreePrior &operator=(const DegreePrior &other)
        {
            setEdgeCountPrior(*other.m_edgeCountPriorPtr);
            return *this;
        }

        void setGraph(const MultiGraph &);
        // const MultiGraph& getGraph() const { return *m_graphPtr; }
        virtual void setState(const DegreeSequence &) override;
        static const DegreeCountsMap computeDegreeCounts(const std::vector<size_t> &degreeSequence);
        static const size_t computeEdgeCountFromDegrees(const std::vector<size_t> &degrees);

        const size_t getSize() const { return m_size; }
        void setSize(size_t size) { m_size = size; }
        const size_t &getEdgeCount() const { return m_edgeCountPriorPtr->getState(); }
        const EdgeCountPrior &getEdgeCountPrior() const { return *m_edgeCountPriorPtr; }
        EdgeCountPrior &getEdgeCountPriorRef() const { return *m_edgeCountPriorPtr; }
        void setEdgeCountPrior(EdgeCountPrior &prior)
        {
            m_edgeCountPriorPtr = &prior;
            m_edgeCountPriorPtr->isRoot(false);
        }

        const size_t &getDegree(BaseGraph::VertexIndex idx) const { return m_state[idx]; }
        virtual const DegreeCountsMap &getDegreeCounts() const { return m_degreeCounts; }

        virtual const double getLogLikelihoodRatioFromGraphMove(const GraphMove &) const override = 0;

        virtual void computationFinished() const override
        {
            m_isProcessed = false;
            m_edgeCountPriorPtr->computationFinished();
        }
        static void checkDegreeSequenceConsistencyWithEdgeCount(const DegreeSequence &, size_t);
        static void checkDegreeSequenceConsistencyWithDegreeCounts(const DegreeSequence &, const DegreeCountsMap &);

        bool isSafe() const override
        {
            return (m_edgeCountPriorPtr != nullptr) and (m_edgeCountPriorPtr->isSafe());
        }
        void checkSelfConsistency() const override;
        virtual void checkSelfSafety() const override
        {
            if (m_edgeCountPriorPtr == nullptr)
                throw SafetyError("DegreePrior", "m_edgeCountPriorPtr");
            m_edgeCountPriorPtr->checkSafety();
        }
        void recomputeConsistentState();
    };

    class DegreeDeltaPrior : public DegreePrior
    {
        DegreeSequence m_degreeSeq;
        EdgeCountDeltaPrior m_edgeCountDeltaPrior;

    public:
        DegreeDeltaPrior(const DegreeSequence &degrees) : DegreePrior(degrees.size()), m_edgeCountDeltaPrior(DegreePrior::computeEdgeCountFromDegrees(degrees))
        {
            setEdgeCountPrior(m_edgeCountDeltaPrior);
            setState(degrees);
        }

        DegreeDeltaPrior(const DegreeDeltaPrior &degreeDeltaPrior) : DegreePrior(degreeDeltaPrior.m_size, degreeDeltaPrior.getEdgeCountPriorRef())
        {
            setState(degreeDeltaPrior.getState());
        }
        virtual ~DegreeDeltaPrior() {}
        const DegreeDeltaPrior &operator=(const DegreeDeltaPrior &other)
        {
            this->setState(other.getState());
            return *this;
        }

        void setState(const DegreeSequence &degrees) override
        {
            m_size = degrees.size();
            m_degreeSeq = degrees;
            DegreePrior::setState(degrees);
        }
        void sampleState() override{};

        const double getLogLikelihood() const override { return 0.; }

        const double getLogLikelihoodRatioFromGraphMove(const GraphMove &move) const override;
        void checkSelfConsistency() const override{};
        void checkSelfSafety() const override
        {
            if (m_degreeSeq.size() == 0)
                throw SafetyError("DegreeDeltaPrior", "m_degreeSeq");
        }

        void computationFinished() const override { m_isProcessed = false; }
    };

    class DegreeUniformPrior : public DegreePrior
    {
        const double getLogLikelihoodFromEdgeCount(size_t edgeCount) const
        {
            return -logMultisetCoefficient(getSize(), 2 * edgeCount);
        }

    public:
        using DegreePrior::DegreePrior;
        void sampleState() override;

        const double getLogLikelihood() const override
        {
            return getLogLikelihoodFromEdgeCount(m_edgeCountPriorPtr->getState());
        }
        const double getLogLikelihoodRatioFromGraphMove(const GraphMove &move) const override
        {
            int dE = move.addedEdges.size() - move.removedEdges.size();
            const size_t &E = m_edgeCountPriorPtr->getState();
            return getLogLikelihoodFromEdgeCount(E + dE) - getLogLikelihoodFromEdgeCount(E);
        }
    };

    class DegreeUniformHyperPrior : public DegreePrior
    {
        bool m_exact;

    public:
        /* Constructors */
        DegreeUniformHyperPrior(size_t graphSize, bool exact = false) : DegreePrior(graphSize), m_exact(exact) {}
        DegreeUniformHyperPrior(size_t graphSize, EdgeCountPrior &prior, bool exact = false) : DegreePrior(graphSize, prior), m_exact(exact) {}

        void sampleState() override;
        const double getLogLikelihood() const override;
        const double getLogLikelihoodRatioFromGraphMove(const GraphMove &) const override;
    };

} // GraphInf

#endif
