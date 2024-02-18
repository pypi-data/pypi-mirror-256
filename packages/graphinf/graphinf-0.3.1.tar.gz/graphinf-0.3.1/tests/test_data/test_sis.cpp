#include "gtest/gtest.h"
#include <list>
#include <cmath>

#include "GraphInf/data/dynamics/sis.h"
#include "GraphInf/graph/erdosrenyi.h"
#include "GraphInf/graph/proposer/edge/hinge_flip.h"
#include "../fixtures.hpp"

namespace GraphInf
{

    class TestSISDynamics : public ::testing::Test
    {
    public:
        const double INFECTION_PROB = 0.7, RECOVERY_PROB = 0.3, AUTO_ACTIVATION_PROB = 1e-6, AUTO_DEACTIVATION_PROB = 1e-6;
        const size_t NUM_INITIAL_ACTIVE = 3;
        const bool NORMALIZE_COUPLING = false, ASYNC = false;
        const std::list<std::vector<VertexState>> neighbor_states = {{1, 3}, {2, 2}, {3, 1}};
        const size_t NUM_STEPS = 20;
        ErdosRenyiModel randomGraph = ErdosRenyiModel(10, 10);

        GraphInf::SISDynamics dynamics = GraphInf::SISDynamics(
            randomGraph, NUM_STEPS, INFECTION_PROB, RECOVERY_PROB);
    };

    TEST_F(TestSISDynamics, getRandomState_forGivenInitialActives_returnCorrectState)
    {
        for (size_t numActive = 1; numActive < 10; numActive++)
        {
            auto state = dynamics.getRandomState(numActive);
            size_t expectedNumActive = 0;
            for (auto s : state)
                expectedNumActive += s;
            EXPECT_EQ(expectedNumActive, numActive);
        }
    }

    TEST_F(TestSISDynamics, getActivationProb_forEachStateTransition_returnCorrectProbability)
    {
        for (auto neighbor_state : neighbor_states)
            EXPECT_EQ(1 - std::pow(1 - INFECTION_PROB, neighbor_state[1]),
                      dynamics.getActivationProb(neighbor_state));
    }

    TEST_F(TestSISDynamics, getDeactivationProb_forEachStateTransition_returnCorrectProbability)
    {
        for (auto neighbor_state : neighbor_states)
            EXPECT_EQ(RECOVERY_PROB, dynamics.getDeactivationProb(neighbor_state));
    }

    TEST_F(TestSISDynamics, afterSample_getCorrectNeighborState)
    {
        dynamics.sample();
        dynamics.checkConsistency();
    }

    TEST_F(TestSISDynamics, getLogLikelihood_returnCorrectLogLikelikehood)
    {
        dynamics.sample();
        auto past = dynamics.getPastStates();
        auto future = dynamics.getFutureStates();
        auto neighborState = dynamics.getNeighborsPastStates();

        double expected = dynamics.getLogLikelihood();
        double actual = 0;
        for (size_t t = 0; t < dynamics.getLength(); ++t)
        {
            for (auto vertex : dynamics.getGraph())
            {
                actual += log(dynamics.getTransitionProb(past[vertex][t], future[vertex][t], neighborState[vertex][t]));
            }
        }
        EXPECT_NEAR(expected, actual, 1E-6);
    }

    TEST_F(TestSISDynamics, getLogLikelihoodRatio_forSomeGraphMove_returnLogJointRatio)
    {
        dynamics.sample();
        auto graphMove = randomGraph.proposeGraphMove();
        double ratio = dynamics.getLogLikelihoodRatioFromGraphMove(graphMove);
        double logLikelihoodBefore = dynamics.getLogLikelihood();
        dynamics.applyGraphMove(graphMove);
        double logLikelihoodAfter = dynamics.getLogLikelihood();

        EXPECT_NEAR(ratio, logLikelihoodAfter - logLikelihoodBefore, 1e-6);
    }
    TEST_F(TestSISDynamics, metropolisGraphStep_forAcceptedMove_noConsistencyError)
    {
        dynamics.sample();
        MCMCSummary summary = {"none", 0, false};
        while (not summary.isAccepted)
            summary = dynamics.metropolisGraphStep();
        dynamics.checkConsistency();
    }

    TEST_F(TestSISDynamics, metropolisParamStep_noConsistencyError)
    {
        dynamics.sample();
        MCMCSummary summary = {"none", 0, false};
        while (not summary.isAccepted)
            summary = dynamics.metropolisParamStep();
        dynamics.checkConsistency();
    }

}
