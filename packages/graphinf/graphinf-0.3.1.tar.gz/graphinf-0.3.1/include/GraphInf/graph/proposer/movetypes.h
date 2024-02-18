#ifndef GRAPH_INF_MOVETYPES_H
#define GRAPH_INF_MOVETYPES_H

#include <vector>
#include <iostream>
#include <sstream>
#include <fstream>
#include "BaseGraph/types.h"
#include "GraphInf/types.h"

namespace GraphInf
{

    struct GraphMove
    {
        GraphMove(std::vector<BaseGraph::Edge> removedEdges, std::vector<BaseGraph::Edge> addedEdges) : removedEdges(removedEdges), addedEdges(addedEdges) {}
        GraphMove() {}
        std::vector<BaseGraph::Edge> removedEdges;
        std::vector<BaseGraph::Edge> addedEdges;

        friend std::ostream &operator<<(std::ostream &os, const GraphMove &move)
        {
            os << move.display();
            return os;
        }

        std::string display() const
        {
            std::stringstream ss;
            ss << "GraphMove(removed=[";
            for (auto e : removedEdges)
            {
                ss << " {" << e.first << ", " << e.second << "}, ";
            }
            ss << "], added=[";
            for (auto e : addedEdges)
            {
                ss << "{" << e.first << ", " << e.second << "}, ";
            }
            ss << "])";
            return ss.str();
        }
        bool operator==(const GraphMove &other)
        {
            return other.removedEdges == removedEdges and other.addedEdges == addedEdges;
        }
    };

    template <typename Label>
    struct LabelMove
    {
        LabelMove(BaseGraph::VertexIndex vertexIndex = 0, Label prevLabel = 0, Label nextLabel = 0, int addedLabels = 0, Level level = 0) : vertexIndex(vertexIndex), prevLabel(prevLabel),
                                                                                                                                            nextLabel(nextLabel), addedLabels(addedLabels),
                                                                                                                                            level(level) {}
        BaseGraph::VertexIndex vertexIndex;
        Label prevLabel;
        Label nextLabel;
        int addedLabels;
        Level level;

        friend std::ostream &operator<<(std::ostream &os, const LabelMove<Label> &move)
        {
            os << move.display();
            return os;
        }

        std::string display() const
        {
            std::stringstream ss;
            ss << "LabelMove(vertex=" << vertexIndex;
            ss << ", prevLabel=" << prevLabel;
            ss << ", nextLabel=" << nextLabel;
            ss << ", addedLabels=" << addedLabels;
            ss << ", level=" << level << ")";
            return ss.str();
        }
        bool operator==(const LabelMove &other)
        {
            return other.vertexIndex == vertexIndex and other.prevLabel == prevLabel and other.nextLabel == nextLabel and other.addedLabels == addedLabels and other.level == level;
        }
    };

    using BlockMove = LabelMove<BlockIndex>;

    // struct NestedBlockMove{
    //     NestedBlockMove(std::vector<BlockMove> blockMoves, int addedLayers=0):
    //         blockMoves(blockMoves), addedLayers(addedLayers){ }
    //     std::vector<BlockMove> blockMoves;
    //     int addedLayers;
    //
    //     std::vector<BlockMove>::iterator begin() { return blockMoves.begin(); }
    //     std::vector<BlockMove>::iterator end() { return blockMoves.end(); }
    //     const BlockMove& operator[](size_t layerIdx) const { return blockMoves[layerIdx]; }
    //
    //     size_t size() const { return blockMoves.size(); }
    //     void display()const{
    //         for(auto m : blockMoves) m.display();
    //     }
    // };

}

#endif
