#ifndef GRAPH_INF_NESTED_LABELPROPOSER_H
#define GRAPH_INF_NESTED_LABELPROPOSER_H

#include "GraphInf/graph/proposer/movetypes.h"
#include "GraphInf/graph/proposer/label/base.hpp"
#include "GraphInf/rng.h"
#include "GraphInf/exceptions.h"

namespace GraphInf
{

    template <typename Label>
    class NestedVertexLabeledRandomGraph;

    template <typename Label>
    class NestedLabelProposer : public LabelProposer<Label>
    {
    protected:
        const NestedVertexLabeledRandomGraph<Label> *m_nestedGraphPriorPtr = nullptr;
        using LabelProposer<Label>::m_sampleLabelCountProb;
        using LabelProposer<Label>::isCreatingLabelMove;
        using LabelProposer<Label>::getLogProposalProbForReverseMove;
        using LabelProposer<Label>::getLogProposalProbForMove;

    public:
        NestedLabelProposer(double sampleLabelCountProb = 0.1) : LabelProposer<Label>(sampleLabelCountProb) {}
        virtual void setUpWithNestedPrior(const NestedVertexLabeledRandomGraph<Label> &graphPrior)
        {
            LabelProposer<Label>::setUpWithPrior(graphPrior);
            m_nestedGraphPriorPtr = &graphPrior;
        }
        const Level sampleLevel() const
        {
            std::uniform_int_distribution<Level> dist(0, m_nestedGraphPriorPtr->getDepth() - 1);
            return dist(rng);
        }

        const double getLogProposalProb(const LabelMove<Label> &move, bool reverse = false) const override
        {
            int dL = 0;
            if (isCreatingLabelMove(move, reverse))
            {
                if (reverse and move.level == m_nestedGraphPriorPtr->getDepth() - 2 and m_nestedGraphPriorPtr->getNestedVertexCounts(move.level).size() == 2)
                    dL = -1;
                return log(m_sampleLabelCountProb) - log(m_nestedGraphPriorPtr->getDepth() + dL);
            }
            if (reverse and move.level == m_nestedGraphPriorPtr->getDepth() - 1 and move.addedLabels == 1)
                dL = 1;
            double dS = log(1 - m_sampleLabelCountProb) - log(m_nestedGraphPriorPtr->getDepth() + dL);
            if (reverse)
                dS += getLogProposalProbForReverseMove(move);
            else
                dS += getLogProposalProbForMove(move);
            return dS;
        }

        void checkSelfSafety() const override
        {
            LabelProposer<Label>::checkSelfSafety();
            if (m_nestedGraphPriorPtr == nullptr)
                throw SafetyError("NestedLabelProposer: unsafe proposer since `m_nestedGraphPriorPtr` is `nullptr`.");
        }
    };

    template <typename Label>
    class GibbsNestedLabelProposer : public NestedLabelProposer<Label>
    {
    protected:
        double m_labelCreationProb;
        using BaseClass = LabelProposer<Label>;
        using NestedBaseClass = NestedLabelProposer<Label>;
        using BaseClass::m_sampleLabelCountProb;
        using BaseClass::m_uniform01;
        using BaseClass::m_vertexDistribution;
        using NestedBaseClass::m_nestedGraphPriorPtr;
        bool creatingNewLevel(const LabelMove<Label> &move) const
        {
            return move.addedLabels == 1 and move.level == m_nestedGraphPriorPtr->getDepth() - 1;
        }
        bool destroyingLevel(const LabelMove<Label> &move) const
        {
            return move.addedLabels == -1 and move.level == m_nestedGraphPriorPtr->getDepth() - 1;
        }
        bool isCreatingLabelMove(const LabelMove<Label> &move, bool reverse) const override
        {
            return move.addedLabels != 0;
        }

    public:
        GibbsNestedLabelProposer(double sampleLabelCountProb = 0.1, double labelCreationProb = 0.5) : NestedLabelProposer<Label>(sampleLabelCountProb), m_labelCreationProb(labelCreationProb) {}
        const LabelMove<Label> proposeNewLabelMove(const BaseGraph::VertexIndex &vertex) const override
        {
            Level level = NestedBaseClass::sampleLevel();
            if (m_uniform01(rng) < m_labelCreationProb)
                return {vertex, m_nestedGraphPriorPtr->getLabel(vertex, level), (int)m_nestedGraphPriorPtr->getNestedLabelCount()[level], 1, level};
            else
                return {vertex, m_nestedGraphPriorPtr->getLabel(vertex, level), m_nestedGraphPriorPtr->getLabel(vertex, level), -1, level};
        }
    };

    template <typename Label>
    class RestrictedNestedLabelProposer : public NestedLabelProposer<Label>
    {
    protected:
        std::vector<std::set<Label>> m_emptyLabels, m_availableLabels;
        bool creatingNewLevel(const LabelMove<Label> &move) const
        {
            return creatingNewLabel(move) and move.level == m_nestedGraphPriorPtr->getDepth() - 1;
        }
        bool destroyingLevel(const LabelMove<Label> &move) const
        {
            return destroyingLabel(move) and move.level == m_nestedGraphPriorPtr->getDepth() - 1;
        }

        bool creatingNewLabel(const LabelMove<Label> &move) const
        {
            return m_nestedGraphPriorPtr->getNestedVertexCounts()[move.level].get(move.nextLabel) == 0;
        };
        bool destroyingLabel(const LabelMove<Label> &move) const
        {
            return move.prevLabel != move.nextLabel and m_nestedGraphPriorPtr->getNestedVertexCounts()[move.level].get(move.prevLabel) == 1;
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
        using NestedBaseClass = NestedLabelProposer<Label>;
        using BaseClass::m_sampleLabelCountProb;
        using BaseClass::m_uniform01;
        using BaseClass::m_vertexDistribution;
        using NestedBaseClass::m_nestedGraphPriorPtr;
        using NestedBaseClass::sampleLevel;
        //
    public:
        using NestedLabelProposer<Label>::NestedLabelProposer;
        const LabelMove<Label> proposeNewLabelMove(const BaseGraph::VertexIndex &vertex) const override
        {
            Level level = sampleLevel();
            Label prevLabel = m_nestedGraphPriorPtr->getLabel(vertex, level);
            Label nextLabel;
            if (m_emptyLabels[level].size() == 0)
                nextLabel = *m_availableLabels[level].rbegin() + 1;
            else
                nextLabel = *sampleUniformlyFrom(m_emptyLabels[level].begin(), m_emptyLabels[level].end());
            LabelMove<Label> move = {vertex, prevLabel, nextLabel, 1, level};
            if (destroyingLabel(move))
                return {vertex, prevLabel, prevLabel, 0, level};
            return move;
        }
        void setUpWithNestedPrior(const NestedVertexLabeledRandomGraph<Label> &graphPrior) override
        {
            NestedBaseClass::setUpWithNestedPrior(graphPrior);
            m_emptyLabels.clear();
            m_availableLabels.clear();
            for (Level l = 0; l < m_nestedGraphPriorPtr->getDepth(); ++l)
            {
                m_emptyLabels.push_back({});
                m_availableLabels.push_back({});
                for (Label r = 0; r < m_nestedGraphPriorPtr->getNestedLabelCount(l); ++r)
                {
                    if (graphPrior.getNestedVertexCounts(l).get(r) == 0)
                        m_emptyLabels[l].insert(r);
                    else
                        m_availableLabels[l].insert(r);
                }
            }
        }

        void applyLabelMove(const LabelMove<Label> &move) override
        {
            if (move.addedLabels == -1)
            {
                m_emptyLabels[move.level].insert(move.prevLabel);
                m_availableLabels[move.level].erase(move.prevLabel);
            }
            if (move.addedLabels == 1)
            {
                m_availableLabels[move.level].insert(move.nextLabel);
                m_emptyLabels[move.level].erase(move.nextLabel);
                if (move.level == m_availableLabels.size() - 1)
                {
                    m_emptyLabels.push_back({1});
                    m_availableLabels.push_back({0});
                }
            }
            // if (m_emptyLabels[move.level].size() == 0)
            //     m_emptyLabels[move.level].insert(
            //         *max_element(m_availableLabels[move.level].begin(), m_availableLabels[move.level].end()) + 1
            //     );
        }
    };

} // namespace GraphInf

#endif
