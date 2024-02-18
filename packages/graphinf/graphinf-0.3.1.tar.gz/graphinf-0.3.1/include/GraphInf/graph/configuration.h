#ifndef GRAPH_INF_CONFIGURATION_H
#define GRAPH_INF_CONFIGURATION_H

#include <map>
#include <utility>
#include <vector>

#include "BaseGraph/types.h"
#include "GraphInf/graph/likelihood/configuration.h"
#include "GraphInf/graph/random_graph.hpp"
#include "GraphInf/graph/util.h"
#include "GraphInf/generators.h"

namespace GraphInf
{

    class ConfigurationModelBase : public RandomGraph
    {
    protected:
        ConfigurationModelLikelihood m_likelihoodModel;
        DegreePrior *m_degreePriorPtr;

        void _applyGraphMove(const GraphMove &move) override
        {
            m_degreePriorPtr->applyGraphMove(move);
            RandomGraph::_applyGraphMove(move);
        }
        const double _getLogPrior() const override { return m_degreePriorPtr->getLogJoint(); }
        const double _getLogPriorRatioFromGraphMove(const GraphMove &move) const override
        {
            return m_degreePriorPtr->getLogJointRatioFromGraphMove(move);
        }
        void sampleOnlyPrior() override { m_degreePriorPtr->sample(); }
        void setUpLikelihood() override
        {
            m_likelihoodModel.m_statePtr = &m_state;
            m_likelihoodModel.m_degreePriorPtrPtr = &m_degreePriorPtr;
        }

        ConfigurationModelBase(size_t graphSize) : RandomGraph(graphSize, m_likelihoodModel, true, true) { setUpLikelihood(); }
        ConfigurationModelBase(size_t graphSize, DegreePrior &degreePrior) : RandomGraph(graphSize, m_likelihoodModel, true, true), m_degreePriorPtr(&degreePrior)
        {
            setUpLikelihood();
            m_degreePriorPtr->isRoot(false);
            m_degreePriorPtr->setSize(m_size);
        }
        void computeConsistentState() override
        {
            m_degreePriorPtr->setGraph(m_state);
        }

    public:
        DegreePrior &getDegreePriorRef() const { return *m_degreePriorPtr; }
        const DegreePrior &getDegreePrior() const { return *m_degreePriorPtr; }
        void setDegreePrior(DegreePrior &prior)
        {
            m_degreePriorPtr = &prior;
            m_degreePriorPtr->isRoot(false);
        }
        // void fromGraph(const MultiGraph &graph) override
        // {
        //     RandomGraph::fromGraph(graph);
        //     m_degreePriorPtr->setGraph(graph);
        // }

        const size_t getEdgeCount() const override { return m_degreePriorPtr->getEdgeCount(); }
        const size_t getDegree(BaseGraph::VertexIndex vertex) const { return m_degreePriorPtr->getDegree(vertex); }
        const std::vector<size_t> &getDegrees() const { return m_degreePriorPtr->getState(); }

        void computationFinished() const override
        {
            m_isProcessed = false;
            m_degreePriorPtr->computationFinished();
        }

        void checkSelfConsistency() const override
        {
            RandomGraph::checkSelfConsistency();
            checkGraphConsistencyWithDegreeSequence(
                "ConfigurationModelBase", "m_state", m_state, "m_degreePriorPtr", getDegrees());
        }

        void checkSelfSafety() const override
        {
            RandomGraph::checkSelfSafety();
            if (not m_degreePriorPtr)
                throw SafetyError("ConfigurationModelBase", "m_degreePriorPtr");
            m_degreePriorPtr->checkSafety();
        }
    };

    class ConfigurationModel : public ConfigurationModelBase
    {
        std::unique_ptr<DegreePrior> m_degreePriorUPtr = nullptr;
        std::unique_ptr<EdgeProposer> m_edgeProposerUPtr = nullptr;

    public:
        ConfigurationModel(const DegreeSequence &degrees) : ConfigurationModelBase(degrees.size())
        {
            m_degreePriorUPtr = std::unique_ptr<DegreePrior>(new DegreeDeltaPrior(degrees));
            setDegreePrior(*m_degreePriorUPtr.get());

            m_edgeProposerUPtr = std::unique_ptr<EdgeProposer>(makeEdgeProposer("degree", false, true, true, true));
            m_edgeProposerPtr = m_edgeProposerUPtr.get();
            m_edgeProposerPtr->isRoot(false);

            checkSafety();
            sample();
        }
        ConfigurationModel(const MultiGraph &graph) : ConfigurationModelBase(graph.getSize())
        {
            auto degrees = graph.getDegrees();
            m_degreePriorUPtr = std::unique_ptr<DegreePrior>(new DegreeDeltaPrior(degrees));
            setDegreePrior(*m_degreePriorUPtr.get());

            m_edgeProposerUPtr = std::unique_ptr<EdgeProposer>(makeEdgeProposer("degree", false, true, true, true));
            m_edgeProposerPtr = m_edgeProposerUPtr.get();
            m_edgeProposerPtr->isRoot(false);

            checkSafety();
            sample();
        }

        const bool isCompatible(const MultiGraph &graph) const override
        {
            return RandomGraph::isCompatible(graph) and graph.getDegrees() == m_degreePriorPtr->getState();
            ;
        }
    };

    class ConfigurationModelFamily : public ConfigurationModelBase
    {
        std::unique_ptr<EdgeCountPrior> m_edgeCountPriorUPtr = nullptr;
        std::unique_ptr<DegreePrior> m_degreePriorUPtr = nullptr;
        std::unique_ptr<EdgeProposer> m_edgeProposerUPtr = nullptr;

    public:
        ConfigurationModelFamily(
            size_t size,
            double edgeCount,
            bool useDegreeHyperPrior = true,
            bool canonical = false,
            bool degreeConstrained = false,
            std::string edgeProposerType = "degree") : ConfigurationModelBase(size)
        {
            m_edgeCountPriorUPtr = std::unique_ptr<EdgeCountPrior>(makeEdgeCountPrior(edgeCount, canonical));
            m_degreePriorUPtr = std::unique_ptr<DegreePrior>(makeDegreePrior(size, *m_edgeCountPriorUPtr, useDegreeHyperPrior));
            setDegreePrior(*m_degreePriorUPtr);

            m_edgeProposerUPtr = std::unique_ptr<EdgeProposer>(makeEdgeProposer(edgeProposerType, canonical, degreeConstrained, true, true));
            setEdgeProposer(*m_edgeProposerUPtr);

            checkSafety();
            sample();
        }
    };

} // end GraphInf
#endif
