#include "gtest/gtest.h"

#include "GraphInf/graph/proposer/multiplemoves.hpp"

typedef bool DummyMove;
class DummyProposer0 : public GraphInf::Proposer<DummyMove>
{
public:
    bool updated = false;

    const DummyMove proposeMove() const override { return false; }
    const double getLogProposalProbRatio(const DummyMove &) const { return 0.; }
    void updateProbabilities(const DummyMove &) { updated = true; }
};
class DummyProposer1 : public GraphInf::Proposer<DummyMove>
{
public:
    bool updated = false;

    const DummyMove proposeMove() const override { return true; }
    const double getLogProposalProbRatio(const DummyMove &) const { return 1.; }
    void updateProbabilities(const DummyMove &) { updated = true; }
};
static const size_t randomGenerationsNumber = 10000;

class TestMultipleMoveProposer : public ::testing::Test
{
public:
    DummyProposer0 dummyProposer0;
    DummyProposer1 dummyProposer1;
    std::vector<GraphInf::Proposer<DummyMove> *> proposers = {&dummyProposer0, &dummyProposer1};
    double p = .3;
    GraphInf::MultipleMovesProposer<DummyMove> proposer =
        GraphInf::MultipleMovesProposer<DummyMove>(proposers, {1 - p, p});
};

TEST_F(TestMultipleMoveProposer, constructor_noProposers_throwLogicError)
{
    std::vector<GraphInf::Proposer<DummyMove> *> _proposers = {};
    std::vector<double> moveWeights = {};
    EXPECT_THROW(
        GraphInf::MultipleMovesProposer<DummyMove>(_proposers, moveWeights),
        std::invalid_argument);
}

TEST_F(TestMultipleMoveProposer, constructor_moreWeights_throwLogicError)
{
    std::vector<GraphInf::Proposer<DummyMove> *> _proposers = {};
    std::vector<double> moveWeights = {1.};
    EXPECT_THROW(
        GraphInf::MultipleMovesProposer<DummyMove>(_proposers, moveWeights),
        std::invalid_argument);
}

TEST_F(TestMultipleMoveProposer, constructor_moreProposers_throwLogicError)
{
    std::vector<GraphInf::Proposer<DummyMove> *> _proposers = {&dummyProposer0};
    std::vector<double> moveWeights = {};
    EXPECT_THROW(
        GraphInf::MultipleMovesProposer<DummyMove>(_proposers, moveWeights),
        std::invalid_argument);
}

TEST_F(TestMultipleMoveProposer, proposeMove_biasedMoveChoice_averageMoveChoiceIsBiased)
{
    GraphInf::rng.seed(3012);
    double averageMoveChoice = 0;

    for (size_t i = 0; i < randomGenerationsNumber; i++)
        averageMoveChoice += proposer.proposeMove();

    EXPECT_NEAR(averageMoveChoice / randomGenerationsNumber, p, 1e-2);
}

// TEST_F(TestMultipleMoveProposer, getProposalProb_biasedMoveChoice_averageProbabilityIsBiased) {
//     GraphInf::rng.seed(3012);
//     double averageProbability=0;
//
//     for (size_t i=0; i<randomGenerationsNumber; i++) {
//         proposer.proposeMove();
//         averageProbability += proposer.getLogProposalProbRatio(true);
//     }
//
//     EXPECT_NEAR(averageProbability/randomGenerationsNumber, p, 1e-2);
// }
//
// TEST_F(TestMultipleMoveProposer, updateProbabilities_twoProposers_probabilitiesUpdated) {
//     proposer.updateProbabilities(true);
//     EXPECT_TRUE(dummyProposer0.updated);
//     EXPECT_TRUE(dummyProposer1.updated);
// }
