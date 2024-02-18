// #include "gtest/gtest.h"
//
// #include "fixtures.hpp"
// #include "GraphInf/random_graph/proposer/edge_proposer/labeled_double_edge_swap.h"
// #include "GraphInf/rng.h"
//
// namespace GraphInf{
//
//     class DummyLabeledDoubleEdgeSwapProposer: public LabeledDoubleEdgeSwapProposer{
//     public:
//         LabelPairSampler getLabelSampler() { return m_labelSampler;}
//         std::unordered_map<LabelPair, EdgeSampler*> getEdgeSamplers(){ return m_labeledEdgeSampler; }
//     };
//
// class TestLabeledDoubleEdgeSwapProposer: public ::testing::Test{
// public:
//     DummySBMGraph randomGraph = DummySBMGraph();
//     DummyLabeledDoubleEdgeSwapProposer proposer = DummyLabeledDoubleEdgeSwapProposer();
//     void SetUp(){
//         randomGraph.sample();
//         proposer.setUp(randomGraph);
//         proposer.checkSafety();
//     }
//     void TearDown() {
//         proposer.checkConsistency();
//     }
// };
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, proposeMove){
//     auto move = proposer.proposeMove();
//     LabelPair rs = {10, 10};
//     for (auto edge : move.removedEdges){
//         EXPECT_GT(randomGraph.getGraph().getEdgeMultiplicityIdx(edge), 0);
//         if (rs.first == 10 and rs.second == 10)
//             rs = proposer.getLabelSampler().getLabelOfIdx(edge);
//         EXPECT_EQ(rs, proposer.getLabelSampler().getLabelOfIdx(edge));
//     }
//     for (auto edge : move.addedEdges){
//         EXPECT_GE(randomGraph.getGraph().getEdgeMultiplicityIdx(edge), 0);
//         EXPECT_EQ(rs, proposer.getLabelSampler().getLabelOfIdx(edge));
//     }
// }
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, onLabelCreation_doNothing){
//     BlockMove move = {0, 0, 0};
//     proposer.onLabelCreation(move);
// }
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, onLabelDeletion_doNothing){
//     BlockMove move = {0, 0, 0};
//     proposer.onLabelDeletion(move);
// }
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, getLogProposalProbRatio_return0){
//     auto move = proposer.proposeMove();
//     EXPECT_EQ(proposer.getLogProposalProbRatio(move), 0);
// }
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, applyGraphMove_forEdgeAdded){
//     size_t totalEdgeCountBefore = proposer.getTotalEdgeCount();
//     proposer.applyGraphMove({{}, {{0,1}}});
//     EXPECT_EQ(totalEdgeCountBefore + 1, proposer.getTotalEdgeCount());
//
// }
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, applyGraphMove_forSelfLoopAdded){
//     size_t totalEdgeCountBefore = proposer.getTotalEdgeCount();
//     proposer.applyGraphMove({{}, {{0,0}}});
//     EXPECT_EQ(totalEdgeCountBefore + 1, proposer.getTotalEdgeCount());
// }
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, applyGraphMove_forSomeGraphMove){
//     size_t totalEdgeCountBefore = proposer.getTotalEdgeCount();
//     auto move = proposer.proposeMove();
//     proposer.applyGraphMove(move);
//     EXPECT_EQ(totalEdgeCountBefore, proposer.getTotalEdgeCount());
// }
//
// TEST_F(TestLabeledDoubleEdgeSwapProposer, applyBlockMove_forSomeBlockMove){
//     for (auto vertex : randomGraph.getGraph()){
//         BlockIndex prevBlockIdx = randomGraph.getBlockOfIdx(vertex);
//         BlockIndex nextBlockIdx = (prevBlockIdx == randomGraph.getBlockCount()-1) ? prevBlockIdx - 1 : prevBlockIdx + 1;
//         BlockMove move = {vertex, prevBlockIdx, nextBlockIdx};
//         proposer.applyBlockMove(move);
//         randomGraph.applyBlockMove(move);
//     }
// }
//
//
// }
