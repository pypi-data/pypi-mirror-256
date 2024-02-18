#ifndef FASTMIDYNET_EDGE_SAMPLER_H
#define FASTMIDYNET_EDGE_SAMPLER_H

#include <unordered_set>
#include <unordered_map>
#include "SamplableSet.hpp"
#include "hash_specialization.hpp"
#include "BaseGraph/types.h"
#include "GraphInf/rng.h"
#include "GraphInf/graph/proposer/movetypes.h"
#include "GraphInf/utility/maps.hpp"
#include "GraphInf/utility/functions.h"

namespace GraphInf
{

    class EdgeSampler
    {
    private:
        double m_minWeight, m_maxWeight;
        sset::SamplableSet<BaseGraph::Edge> m_edgeSampler;
        std::unordered_map<BaseGraph::Edge, double> m_hiddenWeights;
        const MultiGraph *m_graphPtr = nullptr;

    public:
        EdgeSampler(double minWeight = 1, double maxWeight = 100) : m_minWeight(minWeight), m_maxWeight(maxWeight),
                                                                    m_edgeSampler(minWeight, maxWeight) {}
        EdgeSampler(const EdgeSampler &other) : m_edgeSampler(other.m_edgeSampler), m_hiddenWeights(other.m_hiddenWeights) {}
        virtual ~EdgeSampler() {}

        BaseGraph::Edge sample() const
        {
            return m_edgeSampler.sample_ext_RNG(rng).first;
        }
        bool contains(const BaseGraph::Edge &edge) const
        {
            return m_edgeSampler.count(edge) > 0;
        };

        void onEdgeAddition(const BaseGraph::Edge &);
        void onEdgeRemoval(const BaseGraph::Edge &);
        void onEdgeInsertion(const BaseGraph::Edge &, double);
        double onEdgeErasure(const BaseGraph::Edge &);
        const double getEdgeWeight(const BaseGraph::Edge &edge) const
        {
            // auto orderedEdge = getOrderedEdge(edge);
            return (contains(edge)) ? m_edgeSampler.get_weight(edge) : 0.;
        }

        std::unordered_set<BaseGraph::Edge> enumerateEdges()
        {
            std::unordered_set<BaseGraph::Edge> edges;
            m_edgeSampler.init_iterator();
            for (size_t i = 0; i < m_edgeSampler.size(); i++)
            {
                edges.insert(m_edgeSampler.get_at_iterator().first);
                m_edgeSampler.next();
            }
            return edges;
        }

        const double getTotalWeight() const { return m_edgeSampler.total_weight(); }
        const double getSize() const { return m_edgeSampler.size(); }
        void setUpWithGraph(const MultiGraph &graph);

        void clear() { m_edgeSampler.clear(); }
        void checkSafety() const {}
    };

}

#endif
