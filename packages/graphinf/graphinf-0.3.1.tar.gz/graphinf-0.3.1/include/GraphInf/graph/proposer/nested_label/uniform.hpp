#ifndef GRAPH_INF_NESTED_UNIFORM_PROPOSER_H
#define GRAPH_INF_NESTED_UNIFORM_PROPOSER_H

#include "GraphInf/rng.h"
#include "GraphInf/exceptions.h"
#include "GraphInf/graph/proposer/movetypes.h"
#include "GraphInf/graph/proposer/nested_label/base.hpp"
#include "GraphInf/graph/random_graph.hpp"

namespace GraphInf
{

    template <typename Label>
    class GibbsUniformNestedLabelProposer : public GibbsNestedLabelProposer<Label>
    {
    protected:
        using GibbsNestedLabelProposer<Label>::m_nestedGraphPriorPtr;
        using GibbsNestedLabelProposer<Label>::m_sampleLabelCountProb;
        using GibbsNestedLabelProposer<Label>::sampleLevel;

    public:
        using GibbsNestedLabelProposer<Label>::GibbsNestedLabelProposer;
        const double getLogProposalProbForMove(const LabelMove<Label> &move) const override { return -log(m_nestedGraphPriorPtr->getNestedLabelCount()[move.level]); }
        const double getLogProposalProbForReverseMove(const LabelMove<Label> &move) const override { return -log(m_nestedGraphPriorPtr->getNestedLabelCount()[move.level] + move.addedLabels); }
        const LabelMove<Label> proposeLabelMove(const BaseGraph::VertexIndex &vertex) const override
        {
            Level level = sampleLevel();
            Label nextLabel;
            if (m_nestedGraphPriorPtr->getNestedLabelCount()[level] == 1)
                nextLabel = 0;
            else
                nextLabel = std::uniform_int_distribution<Label>(0, m_nestedGraphPriorPtr->getNestedLabelCount()[level] - 1)(rng);
            return {vertex, m_nestedGraphPriorPtr->getLabel(vertex, level), nextLabel, 0, level};
        }
    };

    using GibbsUniformNestedBlockProposer = GibbsUniformNestedLabelProposer<BlockIndex>;

    template <typename Label>
    class RestrictedUniformNestedLabelProposer : public RestrictedNestedLabelProposer<Label>
    {
    protected:
        using RestrictedNestedLabelProposer<Label>::m_nestedGraphPriorPtr;
        using RestrictedNestedLabelProposer<Label>::m_sampleLabelCountProb;
        using RestrictedNestedLabelProposer<Label>::m_availableLabels;
        using RestrictedNestedLabelProposer<Label>::sampleLevel;

    public:
        using RestrictedNestedLabelProposer<Label>::RestrictedNestedLabelProposer;
        const double getLogProposalProbForMove(const LabelMove<Label> &move) const override
        {
            return -log(m_availableLabels[move.level].size());
        }
        const double getLogProposalProbForReverseMove(const LabelMove<Label> &move) const override
        {
            return -log(m_availableLabels[move.level].size() + move.addedLabels);
        }
        const LabelMove<Label> proposeLabelMove(const BaseGraph::VertexIndex &vertex) const override
        {
            Level level = sampleLevel();
            Label nextLabel = *sampleUniformlyFrom(m_availableLabels[level].begin(), m_availableLabels[level].end());
            LabelMove<Label> move = {vertex, m_nestedGraphPriorPtr->getLabel(vertex, level), nextLabel, 0, level};
            move.addedLabels = -(int)RestrictedNestedLabelProposer<Label>::destroyingLabel(move);
            return move;
        }
    };
    using RestrictedUniformNestedBlockProposer = RestrictedUniformNestedLabelProposer<BlockIndex>;

} // namespace GraphInf

#endif
