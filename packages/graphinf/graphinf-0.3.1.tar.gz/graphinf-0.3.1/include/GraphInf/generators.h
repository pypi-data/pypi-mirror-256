#ifndef GRAPH_INF_GENERATORS_H
#define GRAPH_INF_GENERATORS_H

#include <random>
#include <vector>
#include <list>
#include <algorithm>

#include "BaseGraph/undirected_multigraph.hpp"
#include "BaseGraph/types.h"

#include "GraphInf/types.h"
#include "GraphInf/generators.h"
#include "GraphInf/rng.h"

namespace GraphInf
{

    template <typename InType, typename OutType>
    OutType generateCategorical(const std::vector<InType> &probs)
    {
        std::discrete_distribution<OutType> dist(probs.begin(), probs.end());
        return dist(rng);
    };
    std::vector<size_t> sampleUniformlySequenceWithoutReplacement(size_t n, size_t k);
    std::list<size_t> sampleRandomComposition(size_t n, size_t k);
    std::list<size_t> sampleRandomWeakComposition(size_t n, size_t k);
    std::list<size_t> sampleRandomRestrictedPartition(size_t n, size_t k, size_t numberOfSteps = 0);
    std::vector<size_t> sampleRandomPermutation(const std::vector<size_t> &nk);
    std::vector<size_t> sampleMultinomial(const size_t n, const std::vector<double> &p);
    std::vector<size_t> sampleUniformMultinomial(const size_t n, const size_t k);

    BaseGraph::VertexIndex sampleRandomNeighbor(
        const MultiGraph &graph, const BaseGraph::VertexIndex vertex, bool withMultiplicity = true);

    template <typename T>
    T sampleUniformly(T min, T max)
    {
        std::uniform_int_distribution<> dist(min, max);
        return dist(rng);
    }

    template <typename T, typename out>
    out sampleUniformlyFrom(T sequence)
    {
        return *sampleUniformlyFrom<T>(sequence.begin(), sequence.end());
    }

    template <typename Iterator>
    Iterator sampleUniformlyFrom(Iterator start, Iterator end)
    {
        std::uniform_int_distribution<> dist(0, std::distance(start, end) - 1);
        std::advance(start, dist(rng));
        return start;
    }

    template <typename T>
    std::vector<size_t> argsortVector(const std::vector<T> &v)
    {
        std::vector<size_t> idx(v.size());
        std::iota(idx.begin(), idx.end(), 0);
        std::stable_sort(idx.begin(), idx.end(), [&v](size_t i1, size_t i2)
                         { return v[i1] < v[i2]; });
        return idx;
    }

    template <typename T>
    std::vector<T> sortVector(const std::vector<T> &v)
    {
        std::vector<T> values(v);
        std::sort(values.begin(), values.end());
        return values;
    }

    BaseGraph::UndirectedMultigraph generateDCSBM(const BlockSequence &vertexBlocks, const LabelGraph &blockEdgeMatrix, const DegreeSequence &degrees);
    BaseGraph::UndirectedMultigraph generateStubLabeledSBM(const BlockSequence &vertexBlocks, const LabelGraph &labelGraph, bool withSelfLoops = true);
    BaseGraph::UndirectedMultigraph generateMultiGraphSBM(const BlockSequence &vertexBlocks, const LabelGraph &labelGraph, bool withSelfLoops = true);
    BaseGraph::UndirectedMultigraph generateSBM(const BlockSequence &vertexBlocks, const LabelGraph &labelGraph, bool withSelfLoops = true);
    MultiGraph generateCM(const DegreeSequence &degrees);

    MultiGraph generateErdosRenyi(size_t size, size_t edgeCount, bool withSelfLoops = true);
    MultiGraph generateStubLabeledErdosRenyi(size_t size, size_t edgeCount, bool withSelfLoops = true);
    MultiGraph generateMultiGraphErdosRenyi(size_t size, size_t edgeCount, bool withSelfLoops = true);

    template <typename T>
    T pickElementUniformly(const std::vector<T> &sequence)
    {
        return sequence[std::uniform_int_distribution<size_t>(0, sequence.size() - 1)(rng)];
    }

} // namespace GraphInf

#endif
