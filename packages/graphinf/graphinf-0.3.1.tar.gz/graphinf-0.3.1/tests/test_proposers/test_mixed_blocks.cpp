#include "gtest/gtest.h"
#include "GraphInf/graph/proposer/label/mixed.hpp"
#include "GraphInf/types.h"
#include "GraphInf/rng.h"
#include "../fixtures.hpp"

namespace GraphInf
{

    double getGroundTruthMoveProb(
        BaseGraph::VertexIndex vertex,
        BlockIndex s,
        const MultiGraph &graph,
        const BlockSequence &blocks,
        const LabelGraph &labelGraph,
        double shift,
        size_t blockCount)
    {
        double weight, degree;

        for (const auto &neighbor : graph.getOutNeighbours(vertex))
        {
            BlockIndex t = blocks[neighbor];
            size_t m = graph.getEdgeMultiplicity(vertex, neighbor);
            if (vertex == neighbor)
                m *= 2;
            size_t Est = labelGraph.getEdgeMultiplicity(s, t);
            size_t Et = labelGraph.getDegree(t);
            if (s == t)
                Est *= 2;
            weight += m * (Est + shift) / (Et + shift * blockCount);
            degree += m;
        }
        return log(weight) - log(degree);
    }

    class TestGibbsMixedBlockProposer : public ::testing::Test
    {
    public:
        double SAMPLE_LABEL_PROB = 0., LABEL_CREATION_PROB = 0.5, SHIFT = 1;
        size_t numSamples = 100;
        const size_t NUM_VERTICES = 100, NUM_EDGES = 250;
        const bool useHyperPrior = false, canonical = false, stubLabeled = false;

        StochasticBlockModelFamily graphPrior = StochasticBlockModelFamily(100, 250, 3, useHyperPrior, canonical, stubLabeled);
        GibbsMixedBlockProposer proposer = GibbsMixedBlockProposer(SAMPLE_LABEL_PROB, LABEL_CREATION_PROB, SHIFT);
        bool expectConsistencyError = false;
        void SetUp()
        {
            seedWithTime();
            graphPrior.sample();
            proposer.setUpWithPrior(graphPrior);
            proposer.checkSafety();
        }

        void TearDown()
        {
            if (not expectConsistencyError)
                proposer.checkConsistency();
        }
    };

    TEST_F(TestGibbsMixedBlockProposer, proposeLabelMove_returnValidMove)
    {
        for (size_t i = 0; i < numSamples; ++i)
        {
            auto move = proposer.proposeLabelMove(0);
            EXPECT_EQ(move.prevLabel, graphPrior.getLabel(0));
            EXPECT_EQ(move.addedLabels, 0);
        }
    }

    TEST_F(TestGibbsMixedBlockProposer, proposeNewLabelMove_returnValidMove)
    {
        for (size_t i = 0; i < numSamples; ++i)
        {
            auto move = proposer.proposeNewLabelMove(0);
            EXPECT_EQ(move.prevLabel, graphPrior.getLabel(0));
            EXPECT_NE(move.addedLabels, 0);
        }
    }

    TEST_F(TestGibbsMixedBlockProposer, getLogProposalProb_forSomeLabelMove_returnCorrectProb)
    {
        for (size_t i = 0; i < 10; ++i)
        {
            auto move = proposer.proposeLabelMove(0);
            while (move.prevLabel == move.nextLabel)
            {
                graphPrior.sample();
                proposer.setUpWithPrior(graphPrior);
                move = proposer.proposeLabelMove(0);
            }
            LabelMove<BlockIndex> reverseMove = {move.vertexIndex, move.nextLabel, move.prevLabel};
            double logProb = proposer.getLogProposalProb(move, false);
            proposer.applyLabelMove(move);
            graphPrior.applyLabelMove(move);
            double revLogProb = proposer.getLogProposalProb(reverseMove, true);
            EXPECT_EQ(logProb, revLogProb);
        }
    }

    TEST_F(TestGibbsMixedBlockProposer, getLogProposalProb_forSomeLabelMove_returnSampledValue)
    {
        CounterMap<BlockIndex> counter;
        size_t numSamples = 100000;
        double tol = 2e-2;

        while (true)
        {
            if (graphPrior.getState().getDegree(0) == 0)
                SetUp();
            else
                break;
        }

        for (size_t i = 0; i < numSamples; ++i)
        {
            BlockMove move = proposer.proposeMove(0);
            counter.increment(move.nextLabel);
        }

        for (auto s : counter)
        {
            int dB = 0;
            if (graphPrior.getVertexCounts().get(s.first) == 0)
                dB = 1;
            else if (graphPrior.getVertexCounts().get(graphPrior.getLabel(0)) == 1)
                dB = -1;

            BlockMove move = {0, graphPrior.getLabel(0), s.first, dB};
            double expected = exp(proposer.getLogProposalProb(move));
            double actual = (double)s.second / (double)numSamples;
            EXPECT_NEAR(expected, actual, tol);
        }
    }

    TEST_F(TestGibbsMixedBlockProposer, getLogProposalProb_forSomeLabelMoveWithDegreeZeroNode_returnSampledValue)
    {
        CounterMap<BlockIndex> counter;
        size_t numSamples = 100000;
        double tol = 2e-2;

        while (true)
        {
            if (graphPrior.getState().getDegree(0) != 0)
                SetUp();
            else
                break;
        }

        for (size_t i = 0; i < numSamples; ++i)
        {
            BlockMove move = proposer.proposeMove(0);
            counter.increment(move.nextLabel);
        }

        for (auto s : counter)
        {
            int dB = 0;
            if (graphPrior.getVertexCounts().get(s.first) == 0)
                dB = 1;
            else if (graphPrior.getVertexCounts().get(graphPrior.getLabel(0)) == 1)
                dB = -1;

            BlockMove move = {0, graphPrior.getLabel(0), s.first, dB};
            double expected = exp(proposer.getLogProposalProb(move));
            double actual = (double)s.second / (double)numSamples;
            EXPECT_NEAR(expected, actual, tol);
        }
    }

    TEST_F(TestGibbsMixedBlockProposer, getLogProposalProb_forLabelMoveAddingNewLabel_returnCorrectProb)
    {
        auto move = proposer.proposeNewLabelMove(0);
        LabelMove<BlockIndex> reverseMove = {move.vertexIndex, move.nextLabel, move.prevLabel, -move.addedLabels};
        double logProb = proposer.getLogProposalProb(move, false);
        proposer.applyLabelMove(move);
        graphPrior.applyLabelMove(move);
        double revLogProb = proposer.getLogProposalProb(reverseMove, true);
        EXPECT_EQ(logProb, revLogProb);
    }

    class TestRestrictedMixedBlockProposer : public ::testing::Test
    {
    public:
        double SAMPLE_LABEL_PROB = 0.1, LABEL_CREATION_PROB = 0.5, SHIFT = 1;
        size_t numSamples = 100;
        const size_t NUM_VERTICES = 100, NUM_EDGES = 250;
        const bool useHyperPrior = true, canonical = false, stubLabeled = false;

        StochasticBlockModelFamily graphPrior = StochasticBlockModelFamily(100, 250, 3, useHyperPrior, canonical, stubLabeled);
        RestrictedMixedBlockProposer proposer = RestrictedMixedBlockProposer(SAMPLE_LABEL_PROB, SHIFT);

        void SetUp()
        {
            seedWithTime();
            graphPrior.sample();
            proposer.setUpWithPrior(graphPrior);
            proposer.checkSafety();
        }

        void TearDown()
        {
            proposer.checkConsistency();
        }
    };

    TEST_F(TestRestrictedMixedBlockProposer, proposeLabelMove_returnValidMove)
    {
        for (size_t i = 0; i < numSamples; ++i)
        {
            auto move = proposer.proposeLabelMove(0);
            EXPECT_EQ(move.prevLabel, graphPrior.getLabel(0));
            EXPECT_NE(move.addedLabels, 1);
        }
    }

    TEST_F(TestRestrictedMixedBlockProposer, proposeNewLabelMove_returnValidMove)
    {
        for (size_t i = 0; i < numSamples; ++i)
        {
            auto move = proposer.proposeNewLabelMove(0);
            EXPECT_EQ(move.prevLabel, graphPrior.getLabel(0));
            if (move.prevLabel != move.nextLabel)
                EXPECT_EQ(move.addedLabels, 1);
        }
    }

    TEST_F(TestRestrictedMixedBlockProposer, getLogProposalProb_forSomeLabelMove_returnCorrectProb)
    {
        for (size_t i = 0; i < 10; ++i)
        {
            auto move = proposer.proposeLabelMove(0);
            while (move.prevLabel == move.nextLabel or graphPrior.getVertexCounts().get(move.prevLabel) == 1)
            {
                graphPrior.sample();
                proposer.setUpWithPrior(graphPrior);
                move = proposer.proposeLabelMove(0);
            }
            LabelMove<BlockIndex> reverseMove = {move.vertexIndex, move.nextLabel, move.prevLabel};
            double logProb = proposer.getLogProposalProb(move, false);
            proposer.applyLabelMove(move);
            graphPrior.applyLabelMove(move);
            double revLogProb = proposer.getLogProposalProb(reverseMove, true);
            EXPECT_NEAR(logProb, revLogProb, 1e-6);
        }
    }

    TEST_F(TestRestrictedMixedBlockProposer, getLogProposalProb_forSomeLabelMove_returnSampledValue)
    {
        CounterMap<BlockIndex> counter;
        size_t numSamples = 100000;
        double tol = 1e-2;

        for (size_t i = 0; i < numSamples; ++i)
        {
            BlockMove move = proposer.proposeMove(0);
            counter.increment(move.nextLabel);
        }

        for (auto s : counter)
        {
            int dB = 0;
            if (graphPrior.getVertexCounts().get(s.first) == 0)
                dB = 1;
            else if (graphPrior.getVertexCounts().get(graphPrior.getLabel(0)) == 1)
                dB = -1;

            BlockMove move = {0, graphPrior.getLabel(0), s.first, dB};
            double expected = exp(proposer.getLogProposalProb(move));
            double actual = (double)s.second / (double)numSamples;
            EXPECT_NEAR(expected, actual, tol);
        }
    }

    TEST_F(TestRestrictedMixedBlockProposer, getLogProposalProb_forLabelMoveAddingNewLabel_returnCorrectProb)
    {
        auto move = proposer.proposeNewLabelMove(0);
        LabelMove<BlockIndex> reverseMove = {move.vertexIndex, move.nextLabel, move.prevLabel, -move.addedLabels};
        double logProb = proposer.getLogProposalProb(move, false);
        proposer.applyLabelMove(move);
        graphPrior.applyLabelMove(move);
        double revLogProb = proposer.getLogProposalProb(reverseMove, true);
        EXPECT_EQ(logProb, revLogProb);
    }

}
