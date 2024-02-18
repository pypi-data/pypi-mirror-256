#ifndef GRAPH_INF_DYNAMICS_TYPES_H
#define GRAPH_INF_DYNAMICS_TYPES_H

#include <vector>

namespace GraphInf
{

    typedef int VertexState;
    typedef std::vector<VertexState> State;
    typedef std::vector<VertexState> VertexStateSequence;
    typedef std::vector<State> StateSequence;

    typedef std::vector<VertexState> VertexNeighborhoodState; // vertexState = [state1, state2, ...]; dim = D
    typedef std::vector<VertexNeighborhoodState> VertexNeighborhoodStateSequence;
    typedef std::vector<VertexNeighborhoodState> NeighborsState; // neighborsState = [vertexState1, vertexState2, ...]; dim = N x D
    typedef std::vector<NeighborsState> NeighborsStateSequence;  // neighborsStateSequence = [neighborsState1, neighborsState2, ...]; dim = T x N x D

}

#endif
