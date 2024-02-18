#ifndef GRAPH_INF_LABELPROPOSER_H
#define GRAPH_INF_LABELPROPOSER_H

#include "GraphInf/graph/proposer/movetypes.h"
#include "GraphInf/graph/proposer/proposer.hpp"
// #include "GraphInf/graph/random_graph.hpp"
#include "GraphInf/rng.h"
#include "GraphInf/rv.hpp"
#include "GraphInf/exceptions.h"
#include "GraphInf/generators.h"
#include "GraphInf/utility/functions.h"

namespace GraphInf
{

    template <typename Label>
    class VertexLabeledRandomGraph;

    template <typename Label>
    class LabelProposer : public Proposer<LabelMove<Label>>
    {
    protected:
        const VertexLabeledRandomGraph<Label> *m_graphPriorPtr = nullptr;
        mutable std::uniform_int_distribution<BaseGraph::VertexIndex> m_vertexDistribution;
        mutable std::uniform_real_distribution<double> m_uniform01 = std::uniform_real_distribution<double>(0, 1);
        const double m_sampleLabelCountProb;
        virtual const double getLogProposalProbForReverseMove(const LabelMove<Label> &move) const = 0;
        virtual const double getLogProposalProbForMove(const LabelMove<Label> &move) const = 0;
        virtual bool isCreatingLabelMove(const LabelMove<Label> &move, bool reverse) const = 0;

    public:
        LabelProposer(double sampleLabelCountProb = 0.1) : m_sampleLabelCountProb(sampleLabelCountProb) {}
        virtual void setUpWithPrior(const VertexLabeledRandomGraph<Label> &graphPrior)
        {
            m_graphPriorPtr = &graphPrior;
            m_vertexDistribution = std::uniform_int_distribution<BaseGraph::VertexIndex>(0, graphPrior.getSize() - 1);
        }
        const double getLogProposalProbRatio(const LabelMove<Label> &move) const
        {
            if (move.prevLabel == move.nextLabel)
                return 0.;
            return getLogProposalProb(move, true) - getLogProposalProb(move);
        }
        virtual const double getLogProposalProb(const LabelMove<Label> &move, bool reverse = false) const
        {
            if (isCreatingLabelMove(move, reverse))
                return log(m_sampleLabelCountProb);
            double dS = 0;
            if (reverse)
                dS = getLogProposalProbForReverseMove(move);
            else
                dS = getLogProposalProbForMove(move);
            return log(1 - m_sampleLabelCountProb) + dS;
        }

        const double getSampleLabelCountProb() const { return m_sampleLabelCountProb; }
        virtual void applyLabelMove(const LabelMove<Label> &move){};

        const VertexLabeledRandomGraph<Label> &getGraphPrior()
        {
            return *m_graphPriorPtr;
        };

        const LabelMove<Label> proposeMove() const override
        {
            BaseGraph::VertexIndex vertex = m_vertexDistribution(rng);
            return proposeMove(vertex);
        }
        const LabelMove<Label> proposeMove(const BaseGraph::VertexIndex &vertex) const
        {
            if (m_uniform01(rng) < m_sampleLabelCountProb)
                return proposeNewLabelMove(vertex);
            return proposeLabelMove(vertex);
        }
        virtual const LabelMove<Label> proposeLabelMove(const BaseGraph::VertexIndex &) const = 0;
        virtual const LabelMove<Label> proposeNewLabelMove(const BaseGraph::VertexIndex &) const = 0;
        bool isTrivialMove(const LabelMove<Label> &move) const
        {
            return move.prevLabel == move.nextLabel;
        }
        void checkSelfSafety() const override
        {
            if (m_graphPriorPtr == nullptr)
                throw SafetyError("LabelProposer: unsafe proposer since `m_graphPriorPtr` is NULL.");
        }
    };

    template <typename Label>
    class GibbsLabelProposer : public LabelProposer<Label>
    {
    protected:
        double m_labelCreationProb;
        using BaseClass = LabelProposer<Label>;
        using BaseClass::m_graphPriorPtr;
        using BaseClass::m_sampleLabelCountProb;
        using BaseClass::m_uniform01;
        using BaseClass::m_vertexDistribution;
        bool isCreatingLabelMove(const LabelMove<Label> &move, bool dummy) const override
        {
            return (move.addedLabels != 0);
        }

    public:
        GibbsLabelProposer(double sampleLabelCountProb = 0.1, double labelCreationProb = 0.5) : LabelProposer<Label>(sampleLabelCountProb), m_labelCreationProb(labelCreationProb) {}
        const LabelMove<Label> proposeNewLabelMove(const BaseGraph::VertexIndex &vertex) const override
        {
            if (m_uniform01(rng) < m_labelCreationProb)
                return {vertex, m_graphPriorPtr->getLabel(vertex), (int)m_graphPriorPtr->getLabelCount(), 1};
            else
                return {vertex, m_graphPriorPtr->getLabel(vertex), m_graphPriorPtr->getLabel(vertex), -1};
        }
    };

    template <typename Label>
    class RestrictedLabelProposer : public LabelProposer<Label>
    {
    protected:
        std::set<Label> m_emptyLabels, m_availableLabels;
        bool creatingNewLabel(const LabelMove<Label> &move) const
        {
            return m_graphPriorPtr->getVertexCounts().get(move.nextLabel) == 0;
        };
        bool destroyingLabel(const LabelMove<Label> &move) const
        {
            return move.prevLabel != move.nextLabel and m_graphPriorPtr->getVertexCounts().get(move.prevLabel) == 1;
        }
        int getAddedLabels(const LabelMove<Label> &move) const
        {
            return (int)creatingNewLabel(move) - (int)destroyingLabel(move);
        }
        bool isCreatingLabelMove(const LabelMove<Label> &move, bool reverse) const override
        {
            if (reverse)
                return move.addedLabels == -1;
            else
                return move.addedLabels == 1;
        }
        using BaseClass = LabelProposer<Label>;
        using BaseClass::m_graphPriorPtr;
        using BaseClass::m_sampleLabelCountProb;
        using BaseClass::m_uniform01;
        using BaseClass::m_vertexDistribution;

    public:
        using LabelProposer<Label>::LabelProposer;
        const LabelMove<Label> proposeNewLabelMove(const BaseGraph::VertexIndex &vertex) const override
        {
            Label prevLabel = m_graphPriorPtr->getLabel(vertex);

            Label nextLabel;
            if (m_emptyLabels.size() == 0)
                nextLabel = *m_availableLabels.rbegin() + 1;
            else
                nextLabel = *sampleUniformlyFrom(m_emptyLabels.begin(), m_emptyLabels.end());
            LabelMove<Label> move = {vertex, prevLabel, nextLabel};
            if (destroyingLabel(move))
                return {vertex, prevLabel, prevLabel};
            move.addedLabels = 1;
            return move;
        }
        void setUpWithPrior(const VertexLabeledRandomGraph<Label> &graphPrior) override
        {
            BaseClass::setUpWithPrior(graphPrior);
            m_emptyLabels.clear();
            m_availableLabels.clear();
            for (Label r = 0; r < m_graphPriorPtr->getLabelCount(); ++r)
            {
                if (m_graphPriorPtr->getVertexCounts().get(r) == 0)
                    m_emptyLabels.insert(r);
                else
                    m_availableLabels.insert(r);
            }
        }

        void applyLabelMove(const LabelMove<Label> &move) override
        {
            if (move.addedLabels == -1)
            {
                m_emptyLabels.insert(move.prevLabel);
                m_availableLabels.erase(move.prevLabel);
            }
            if (move.addedLabels == 1)
            {
                m_availableLabels.insert(move.nextLabel);
                m_emptyLabels.erase(move.nextLabel);
            }
        }
        const std::set<Label> &getAvailableLabels() const
        {
            return m_availableLabels;
        }
        const std::set<Label> &getEmptyLabels() const
        {
            return m_emptyLabels;
        }

        void checkSelfConsistency() const override
        {
            if (m_availableLabels.size() != m_graphPriorPtr->getLabelCount())
                throw ConsistencyError(
                    "RestrictedLabelProposer",
                    "m_availableLabels", "size=" + std::to_string(m_availableLabels.size()),
                    "m_graphPriorPtr->getLabelCount()", "count=" + std::to_string(m_graphPriorPtr->getLabelCount()));
            // if (m_emptyLabels.size() == 0)
            //     throw ConsistencyError(
            //         "RestrictedLabelProposer: `m_emptyLabels` is empty."
            //     );
            for (const auto &b : m_graphPriorPtr->getLabels())
            {
                if (m_availableLabels.count(b) == 0)
                    throw ConsistencyError(
                        "RestrictedLabelProposer", "m_availableLabels", "m_graphPriorPtr->getLabels()");
                if (m_emptyLabels.count(b) != 0)
                    throw ConsistencyError(
                        "RestrictedLabelProposer", "m_emptyLabels", "m_graphPriorPtr->getLabels()");
            }
        }
    };

} // namespace GraphInf

#endif
