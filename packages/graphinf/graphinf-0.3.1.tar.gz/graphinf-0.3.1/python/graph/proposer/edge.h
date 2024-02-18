#ifndef GRAPH_INF_PYWRAPPER_INIT_EDGEPROPOSER_H
#define GRAPH_INF_PYWRAPPER_INIT_EDGEPROPOSER_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "GraphInf/graph/proposer/python/edge_proposer.hpp"

#include "GraphInf/graph/proposer/movetypes.h"
#include "GraphInf/graph/proposer/proposer.hpp"
#include "GraphInf/graph/proposer/edge/edge_proposer.h"
#include "GraphInf/graph/proposer/edge/double_edge_swap.h"
#include "GraphInf/graph/proposer/edge/hinge_flip.h"
#include "GraphInf/graph/proposer/edge/single_edge.h"
// #include "GraphInf/graph/proposer/edge/labeled_edge_proposer.h"
// #include "GraphInf/graph/proposer/edge/labeled_double_edge_swap.h"
// #include "GraphInf/graph/proposer/edge/labeled_hinge_flip.h"

namespace py = pybind11;
namespace GraphInf
{

    void initEdgeProposer(py::module &m)
    {
        py::class_<EdgeProposer, Proposer<GraphMove>, PyEdgeProposer<>>(m, "EdgeProposer")
            .def(py::init<bool, bool>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true)
            .def("set_up_with_graph", &EdgeProposer::setUpWithGraph, py::arg("graph"))
            .def("set_up_with_prior", &EdgeProposer::setUpWithPrior, py::arg("graph"))
            .def("allow_self_loops", &EdgeProposer::allowSelfLoops)
            .def("allow_multiedges", &EdgeProposer::allowMultiEdges)
            .def("get_log_proposal_ratio", &EdgeProposer::getLogProposalProbRatio, py::arg("move"))
            .def("apply_graph_move", &EdgeProposer::applyGraphMove, py::arg("move"));

        /* Double edge swap proposers */
        py::class_<DoubleEdgeSwapProposer, EdgeProposer>(m, "DoubleEdgeSwapProposer")
            .def(py::init<bool, bool>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true);

        /* Hinge flip proposers */
        py::class_<HingeFlipProposer, EdgeProposer, PyHingeFlipProposer<>>(m, "HingeFlipProposer")
            .def(py::init<bool, bool>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true)
            .def("set_vertex_sampler", &HingeFlipProposer::setVertexSampler, py::arg("vertex_sampler"))
            .def("get_edge_proposal_counts", &HingeFlipProposer::getEdgeProposalCounts)
            .def("get_vertex_proposal_counts", &HingeFlipProposer::getVertexProposalCounts);

        py::class_<HingeFlipUniformProposer, HingeFlipProposer>(m, "HingeFlipUniformProposer")
            .def(py::init<bool, bool>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true);

        py::class_<HingeFlipDegreeProposer, HingeFlipProposer>(m, "HingeFlipDegreeProposer")
            .def(py::init<bool, bool, double>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true, py::arg("shift") = 1);

        /* Single edge proposers */
        py::class_<SingleEdgeProposer, EdgeProposer, PySingleEdgeProposer<>>(m, "SingleEdgeProposer")
            .def(py::init<bool, bool>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true)
            .def("set_vertex_sampler", &SingleEdgeProposer::setVertexSampler, py::arg("vertex_sampler"));

        py::class_<SingleEdgeUniformProposer, SingleEdgeProposer>(m, "SingleEdgeUniformProposer")
            .def(py::init<bool, bool>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true);

        py::class_<SingleEdgeDegreeProposer, SingleEdgeProposer>(m, "SingleEdgeDegreeProposer")
            .def(py::init<bool, bool, double>(), py::arg("allow_self_loops") = true, py::arg("allow_multiedges") = true, py::arg("shift") = 1);

        // /* Labeled edge proposers */
        // py::class_<LabeledEdgeProposer, EdgeProposer, PyLabeledEdgeProposer<>>(m, "LabeledEdgeProposer")
        //     .def(py::init<bool, bool, double>(), py::arg("allow_self_loops")=true, py::arg("allow_multiedges")=true,
        //          py::arg("label_pair_shift")=1)
        //     .def("on_label_creation", &LabeledEdgeProposer::onLabelCreation, py::arg("move"))
        //     .def("on_label_deletion", &LabeledEdgeProposer::onLabelDeletion, py::arg("move"));
        //
        // py::class_<LabeledDoubleEdgeSwapProposer, LabeledEdgeProposer>(m, "LabeledDoubleEdgeSwapProposer")
        //     .def(py::init<bool, bool, double>(), py::arg("allow_self_loops")=true, py::arg("allow_multiedges")=true,
        //          py::arg("label_pair_shift")=1);
        //
        // py::class_<LabeledHingeFlipProposer, LabeledEdgeProposer, PyLabeledHingeFlipProposer<>>(m, "LabeledHingeFlipProposer")
        //     .def(py::init<bool, bool, double>(), py::arg("allow_self_loops")=true, py::arg("allow_multiedges")=true,
        //          py::arg("label_pair_shift")=1);
        //
        // py::class_<LabeledHingeFlipUniformProposer, LabeledHingeFlipProposer>(m, "LabeledHingeFlipUniformProposer")
        //     .def(py::init<bool, bool, double>(), py::arg("allow_self_loops")=true, py::arg("allow_multiedges")=true,
        //          py::arg("label_pair_shift")=1);
        //
        // py::class_<LabeledHingeFlipDegreeProposer, LabeledHingeFlipProposer>(m, "LabeledHingeFlipDegreeProposer")
        //     .def(py::init<bool, bool, double, double>(), py::arg("allow_self_loops")=true, py::arg("allow_multiedges")=true,
        //          py::arg("label_pair_shift")=1, py::arg("vertex_shift")=1);
    }

}

#endif
