#ifndef GRAPH_INF_PYWRAPPER_INIT_RANDOM_GRAPH_BASECLASS_H
#define GRAPH_INF_PYWRAPPER_INIT_RANDOM_GRAPH_BASECLASS_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "GraphInf/python/rv.hpp"
#include "GraphInf/graph/random_graph.hpp"
#include "GraphInf/graph/delta.h"
#include "GraphInf/graph/python/randomgraph.hpp"

namespace py = pybind11;
namespace GraphInf
{

     template <typename Label>
     py::class_<VertexLabeledRandomGraph<Label>, RandomGraph, PyVertexLabeledRandomGraph<Label>> declareVertexLabeledRandomGraph(py::module &m, std::string pyName)
     {
          return py::class_<VertexLabeledRandomGraph<Label>, RandomGraph, PyVertexLabeledRandomGraph<Label>>(m, pyName.c_str())
              .def(py::init<size_t, bool, bool>(), py::arg("size"), py::arg("with_self_loops") = true, py::arg("with_parallel_edges") = true)
              .def("label_proposer", &VertexLabeledRandomGraph<Label>::getLabelProposer, py::return_value_policy::reference_internal)
              .def("set_label_proposer", &VertexLabeledRandomGraph<Label>::setLabelProposer, py::arg("proposer"))
              .def("labels", &VertexLabeledRandomGraph<Label>::getLabels, py::return_value_policy::reference_internal)
              .def("labels_copy", &VertexLabeledRandomGraph<Label>::getLabels, py::return_value_policy::copy)
              .def("label_count", &VertexLabeledRandomGraph<Label>::getLabelCount)
              .def("vertex_counts", &VertexLabeledRandomGraph<Label>::getVertexCounts, py::return_value_policy::reference_internal)
              .def("edge_label_counts", &VertexLabeledRandomGraph<Label>::getEdgeLabelCounts, py::return_value_policy::reference_internal)
              .def("label_graph", &VertexLabeledRandomGraph<Label>::getLabelGraph, py::return_value_policy::reference_internal)
              .def(
                  "label", [](const VertexLabeledRandomGraph<Label> &self, BaseGraph::VertexIndex vertex)
                  { return self.getLabel(vertex); },
                  py::arg("vertex"))
              .def("set_labels", &VertexLabeledRandomGraph<Label>::setLabels, py::arg("labels"), py::arg("reduce") = false)
              .def("sample_only_labels", &VertexLabeledRandomGraph<Label>::sampleOnlyLabels)
              .def("sample_with_labels", &VertexLabeledRandomGraph<Label>::sampleWithLabels)
              .def("label_log_joint", &VertexLabeledRandomGraph<Label>::getLabelLogJoint)
              .def("log_likelihood_ratio_from_label_move", &VertexLabeledRandomGraph<Label>::getLogLikelihoodRatioFromLabelMove, py::arg("move"))
              .def("log_prior_ratio_from_label_move", &VertexLabeledRandomGraph<Label>::getLogPriorRatioFromLabelMove, py::arg("move"))
              .def("log_joint_ratio_from_label_move", &VertexLabeledRandomGraph<Label>::getLogJointRatioFromLabelMove, py::arg("move"))
              .def("log_proposal_ratio_from_label_move", &VertexLabeledRandomGraph<Label>::getLogProposalRatioFromLabelMove, py::arg("move"))
              .def("apply_label_move", &VertexLabeledRandomGraph<Label>::applyLabelMove, py::arg("move"))
              .def("propose_label_move", &VertexLabeledRandomGraph<Label>::proposeLabelMove)
              .def("is_valid_label_move", &VertexLabeledRandomGraph<Label>::isValidLabelMove, py::arg("move"))
              .def("reduce_labels", &VertexLabeledRandomGraph<Label>::reduceLabels);
     }

     template <typename Label>
     py::class_<NestedVertexLabeledRandomGraph<Label>, VertexLabeledRandomGraph<Label>, PyNestedVertexLabeledRandomGraph<Label>> declareNestedVertexLabeledRandomGraph(py::module &m, std::string pyName)
     {
          return py::class_<NestedVertexLabeledRandomGraph<Label>, VertexLabeledRandomGraph<Label>, PyNestedVertexLabeledRandomGraph<Label>>(m, pyName.c_str())
              .def(py::init<size_t, bool, bool>(), py::arg("size"), py::arg("with_self_loops") = true, py::arg("with_parallel_edges") = true)
              .def("get_nested_label_proposer", &NestedVertexLabeledRandomGraph<Label>::getNestedLabelProposer, py::return_value_policy::reference_internal)
              .def("set_nested_label_proposer", &NestedVertexLabeledRandomGraph<Label>::setNestedLabelProposer, py::arg("proposer"))
              .def("set_nested_labels", &NestedVertexLabeledRandomGraph<Label>::setNestedLabels, py::arg("nested_labels"), py::arg("reduce") = false)
              .def("get_depth", &NestedVertexLabeledRandomGraph<Label>::getDepth)
              .def(
                  "get_label", [](const NestedVertexLabeledRandomGraph<Label> &self, BaseGraph::VertexIndex vertex, Level level)
                  { return self.getLabel(vertex, level); },
                  py::arg("vertex"), py::arg("level"))
              .def("get_nested_label", &NestedVertexLabeledRandomGraph<Label>::getNestedLabel, py::arg("vertex"), py::arg("level"))
              .def("get_nested_labels", [](const NestedVertexLabeledRandomGraph<Label> &self)
                   { return self.getNestedLabels(); })
              .def("get_nested_labels", [](const NestedVertexLabeledRandomGraph<Label> &self, Level level)
                   { return self.getNestedLabels(level); })
              .def("get_nested_label_count", [](const NestedVertexLabeledRandomGraph<Label> &self)
                   { return self.getNestedLabelCount(); })
              .def("get_nested_label_count", [](const NestedVertexLabeledRandomGraph<Label> &self, Level level)
                   { return self.getNestedLabelCount(level); })
              .def("get_nested_vertex_counts", [](const NestedVertexLabeledRandomGraph<Label> &self)
                   { return self.getNestedVertexCounts(); })
              .def("get_nested_vertex_counts", [](const NestedVertexLabeledRandomGraph<Label> &self, Level level)
                   { return self.getNestedVertexCounts(level); })
              .def("get_nested_edge_label_counts", [](const NestedVertexLabeledRandomGraph<Label> &self)
                   { return self.getNestedEdgeLabelCounts(); })
              .def("get_nested_edge_label_counts", [](const NestedVertexLabeledRandomGraph<Label> &self, Level level)
                   { return self.getNestedEdgeLabelCounts(level); })
              .def("get_nested_label_graph", [](const NestedVertexLabeledRandomGraph<Label> &self)
                   { return self.getNestedLabelGraph(); })
              .def("get_nested_label_graph", [](const NestedVertexLabeledRandomGraph<Label> &self, Level level)
                   { return self.getNestedLabelGraph(level); });
     }

     void initRandomGraphBaseClass(py::module &m)
     {
          py::class_<RandomGraph, NestedRandomVariable, PyRandomGraph<>>(m, "RandomGraph")
              .def(py::init<size_t, bool, bool>(), py::arg("size"), py::arg("with_self_loops") = true, py::arg("with_parallel_edges") = true)
              .def("state", &RandomGraph::getState, py::return_value_policy::reference_internal)
              .def("state_copy", &RandomGraph::getState, py::return_value_policy::copy)
              .def("set_state", &RandomGraph::setState, py::arg("state"))
              .def("size", &RandomGraph::getSize)
              .def("set_size", &RandomGraph::setSize)
              .def("edge_count", &RandomGraph::getEdgeCount)
              .def("average_degree", &RandomGraph::getAverageDegree)
              .def("edge_proposer", &RandomGraph::getEdgeProposer, py::return_value_policy::reference_internal)
              .def("set_edge_proposer", &RandomGraph::setEdgeProposer, py::arg("proposer"))
              .def("with_self_loops", [](const RandomGraph &self)
                   { return self.withSelfLoops(); })
              .def("with_self_loops", [](RandomGraph &self, bool condition)
                   { return self.withSelfLoops(condition); })
              .def("with_parallel_edges", [](const RandomGraph &self)
                   { return self.withParallelEdges(); })
              .def("with_parallel_edges", [](RandomGraph &self, bool condition)
                   { return self.withParallelEdges(condition); })
              .def("sample", &RandomGraph::sample)
              .def("sample_state", &RandomGraph::sampleState)
              .def("sample_prior", &RandomGraph::samplePrior)
              .def("log_likelihood", &RandomGraph::getLogLikelihood)
              .def("log_prior", &RandomGraph::getLogPrior)
              .def("log_joint", &RandomGraph::getLogJoint)
              .def("log_likelihood_ratio_from_graph_move", &RandomGraph::getLogLikelihoodRatioFromGraphMove, py::arg("move"))
              .def("log_prior_ratio_from_graph_move", &RandomGraph::getLogPriorRatioFromGraphMove, py::arg("move"))
              .def("log_joint_ratio_from_graph_move", &RandomGraph::getLogJointRatioFromGraphMove, py::arg("move"))
              .def("log_proposal_ratio_from_graph_move", &RandomGraph::getLogProposalRatioFromGraphMove, py::arg("move"))
              .def("apply_graph_move", &RandomGraph::applyGraphMove, py::arg("move"))
              .def("propose_graph_move", &RandomGraph::proposeGraphMove)
              .def("is_compatible", &RandomGraph::isCompatible)
              .def("is_valid_graph_move", &RandomGraph::isValidGraphMove, py::arg("move"));

          py::class_<DeltaGraph, RandomGraph>(m, "DeltaGraph")
              .def(py::init<const MultiGraph>(), py::arg("graph"));
          declareVertexLabeledRandomGraph<BlockIndex>(m, "BlockLabeledRandomGraph");
          declareNestedVertexLabeledRandomGraph<BlockIndex>(m, "NestedBlockLabeledRandomGraph");
     }

}
#endif
