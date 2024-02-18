#ifndef GRAPH_INF_BLOCK_COUNT_H
#define GRAPH_INF_BLOCK_COUNT_H

#include "GraphInf/exceptions.h"
#include "GraphInf/types.h"
#include "GraphInf/rng.h"
#include "GraphInf/utility/functions.h"
#include "prior.hpp"

namespace GraphInf
{

    class BlockCountPrior : public BlockLabeledPrior<size_t>
    {
    protected:
        void _applyGraphMove(const GraphMove &move) override {}
        void _applyLabelMove(const BlockMove &move) override { throw DepletedMethodError("BlockCount", "_applyLabelMove"); }
        void _samplePriors() override {}
        const double _getLogPrior() const override { return 0; }
        const double _getLogPriorRatioFromGraphMove(const GraphMove &move) const override { return 0; }
        const double _getLogPriorRatioFromLabelMove(const BlockMove &move) const override { return 0; }

    public:
        using BlockLabeledPrior<size_t>::BlockLabeledPrior;
        virtual const double getLogLikelihoodFromState(const size_t &) const = 0;
        virtual const double getLogLikelihood() const override { return getLogLikelihoodFromState(m_state); }
        const double getLogLikelihoodRatioFromGraphMove(const GraphMove &move) const override { return 0; }
        const double getLogLikelihoodRatioFromLabelMove(const BlockMove &move) const override { throw DepletedMethodError("BlockCount", "getLogLikelihoodRatioFromLabelMove"); }
        void setStateFromPartition(const BlockSequence &blocks) { setState(*max_element(blocks.begin(), blocks.end()) + 1); }
        virtual void setMaxBlockCount(size_t maxBlockCount) {}
    };

    class BlockCountDeltaPrior : public BlockCountPrior
    {
    public:
        BlockCountDeltaPrior() {}
        BlockCountDeltaPrior(size_t blockCount) { setState(blockCount); }
        BlockCountDeltaPrior(const BlockCountDeltaPrior &other) { setState(other.getState()); }
        virtual ~BlockCountDeltaPrior(){};
        const BlockCountDeltaPrior &operator=(const BlockCountDeltaPrior &other)
        {
            setState(other.m_state);
            return *this;
        }

        void sampleState() override {}

        const double getLogLikelihoodFromState(const size_t &blockCount) const override
        {
            return (blockCount != m_state) ? -INFINITY : 0;
        }
        void checkSelfSafety() const override
        {
            if (m_state == 0)
                throw SafetyError("BlockCountDeltaPrior", "m_blockCount", "0");
        }
    };

    class BlockCountPoissonPrior : public BlockCountPrior
    {
        double m_mean;
        std::poisson_distribution<size_t> m_poissonDistribution;

    public:
        BlockCountPoissonPrior() {}
        BlockCountPoissonPrior(double mean) { setMean(mean); }
        BlockCountPoissonPrior(const BlockCountPoissonPrior &other)
        {
            setMean(other.m_mean);
            setState(other.m_state);
        }
        virtual ~BlockCountPoissonPrior(){};
        const BlockCountPoissonPrior &operator=(const BlockCountPoissonPrior &other)
        {
            setMean(other.m_mean);
            setState(other.m_state);
            return *this;
        }

        const double getMean() const { return m_mean; }
        void setMean(double mean)
        {
            m_mean = mean;
            m_poissonDistribution = std::poisson_distribution<size_t>(mean);
        }
        void sampleState() override;
        const double getLogLikelihoodFromState(const size_t &state) const override;

        void checkSelfSafety() const override;
    };

    class BlockCountUniformPrior : public BlockCountPrior
    {
        size_t m_min, m_max;
        std::uniform_int_distribution<size_t> m_uniformDistribution;

    public:
        BlockCountUniformPrior() {}
        BlockCountUniformPrior(size_t min, size_t max) { setMinMax(min, max); }
        BlockCountUniformPrior(const BlockCountUniformPrior &other)
        {
            setMinMax(other.m_min, other.m_max);
            setState(other.m_state);
        }
        virtual ~BlockCountUniformPrior(){};
        const BlockCountUniformPrior &operator=(const BlockCountUniformPrior &other)
        {
            setMin(other.m_min);
            setMax(other.m_max);
            setState(other.m_state);
            return *this;
        }

        const double getMin() const { return m_min; }
        const double getMax() const { return m_max; }
        void setMin(size_t min)
        {
            m_min = min;
            checkMin();
            m_uniformDistribution = std::uniform_int_distribution<size_t>(m_min, m_max);
        }
        void setMax(size_t max)
        {
            m_max = max;
            checkMax();
            m_uniformDistribution = std::uniform_int_distribution<size_t>(m_min, m_max);
        }
        void setMaxBlockCount(size_t maxBlockCount) override
        {
            setMax(maxBlockCount);
            sample();
        }
        void setMinMax(size_t min, size_t max)
        {
            setMin(min);
            setMax(max);
        }
        void sampleState() override { setState(m_uniformDistribution(rng)); }
        const double getLogLikelihoodFromState(const size_t &state) const override
        {
            if (state > m_max or state < m_min)
                return -INFINITY;
            return -log(m_max - m_min + 1);
        };

        void checkMin() const;
        void checkMax() const;
        void checkSelfSafety() const override;
    };

    class NestedBlockCountPrior : public BlockCountPrior
    {
    protected:
        std::vector<size_t> m_nestedState;
        size_t m_depth;

    public:
        const double getLogLikelihoodFromState(const size_t &) const override
        {
            throw DepletedMethodError("NestedBlockCount", "getLogLikelihoodFromState");
        };
        virtual const double getLogLikelihoodFromNestedState(const std::vector<size_t> &) const = 0;
        const double getLogLikelihood() const override
        {
            return getLogLikelihoodFromNestedState(m_nestedState);
        }

        const size_t getDepth() const { return m_depth; }
        const std::vector<size_t> &getNestedState() const { return m_nestedState; }
        const size_t &getNestedState(Level level) const { return m_nestedState[level]; }
        void createNewLevel()
        {
            m_nestedState.push_back(1);
            ++m_depth;
        }
        void destroyLastLevel()
        {
            m_nestedState.pop_back();
            --m_depth;
        }
        void setNestedState(const std::vector<size_t> &nestedBlockCounts)
        {
            m_nestedState = nestedBlockCounts;
            m_state = nestedBlockCounts[0];
            m_depth = m_nestedState.size();
            for (auto it = m_nestedState.rbegin() + 1; it != m_nestedState.rend(); ++it)
            {
                if (*it == 1)
                    --m_depth;
                else
                    break;
            }
        }
        void setNestedState(const size_t blockCount, Level level)
        {
            m_nestedState[level] = blockCount;
            if (level < m_depth - 1 and blockCount == 1)
                m_depth = level + 1;
            if (level == 0)
                m_state = blockCount;
        }
        void setNestedStateFromNestedPartition(const std::vector<std::vector<BlockIndex>> &nestedBlocks)
        {
            std::vector<size_t> nestedState;
            for (auto b : nestedBlocks)
                nestedState.push_back(*max_element(b.begin(), b.end()) + 1);
            setNestedState(nestedState);
        }
        void checkSelfConsistency() const override
        {
            if (m_state != m_nestedState[0])
                throw ConsistencyError(
                    "NestedBlockCountPrior",
                    "m_state", "value=" + std::to_string(m_state),
                    "m_nestedState[0]", "value=" + std::to_string(m_nestedState[0]));
            size_t actualDepth = m_nestedState.size();
            for (auto it = m_nestedState.rbegin() + 1; it != m_nestedState.rend(); ++it)
            {
                if (*it == 1)
                    --actualDepth;
                else
                    break;
            }
            if (m_depth != actualDepth)
                throw ConsistencyError(
                    "NestedBlockCountPrior",
                    "m_depth", "value=" + std::to_string(m_depth),
                    "m_nestedState", "depth=" + std::to_string(actualDepth));
        }
    };

    // #include "GraphInf/utility/functions.h"

    class NestedBlockCountUniformPrior : public NestedBlockCountPrior
    {
    protected:
        size_t m_graphSize;

    public:
        NestedBlockCountUniformPrior(size_t graphSize = 1) : NestedBlockCountPrior(), m_graphSize(graphSize) {}
        virtual ~NestedBlockCountUniformPrior(){};

        void sampleState() override
        {
            std::vector<size_t> nestedState;
            std::uniform_int_distribution<size_t> dist(1, m_graphSize - 1);
            nestedState.push_back(dist(rng));
            while (nestedState.back() != 1)
            {
                std::uniform_int_distribution<size_t> nestedDist(1, nestedState.back() - 1);
                nestedState.push_back(nestedDist(rng));
            }
            setNestedState(nestedState);
        }

        const double getLogLikelihoodFromNestedState(const std::vector<size_t> &nestedState) const override
        {
            for (size_t l = 1; l < nestedState.size(); ++l)
                if (nestedState[l - 1] <= nestedState[l])
                    return -INFINITY;

            double logLikelihood = -log(m_graphSize - 1);
            for (size_t l = 0; l < nestedState.size() - 1; ++l)
                logLikelihood -= log(nestedState[l] - 1);
            return logLikelihood;
        }

        const size_t getGraphSize() const { return m_graphSize; }
        void setGraphSize(size_t size) { m_graphSize = size; }
        void checkSelfSafety() const override
        {
            if (m_graphSize < 0)
                throw SafetyError("NestedBlockCountUniformPrior", "m_graphSize", "<0");
        }
    };

}

#endif
