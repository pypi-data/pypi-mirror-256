"""Importing Vitis HLS reports into graph IR interfaces."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import json
import logging
import os
import re
import xml.etree.ElementTree as et
from glob import glob
from typing import Any

_logger = logging.getLogger().getChild(__name__)

REPORT_SFX = "_csynth.xml"


class AutoPilotParser:
    """Module to extract metadata from the HLS project."""

    def __init__(self, solution_dir: str) -> None:
        """Get the top module of the project."""
        self.solution_dir = solution_dir

        meta_files = glob(f"{solution_dir}/*_data.json")
        if len(meta_files) != 1:
            raise ValueError(
                f"Found {len(meta_files)} metadata files in {solution_dir}, expected 1."
            )
        meta_path = meta_files[0]
        with open(meta_path, "r", encoding="utf-8") as fp:
            self.meta: dict[str, Any] = json.load(fp)

        self.safety_check()

    def safety_check(self) -> None:
        """Check that the design satisfies requirements."""
        df_modules = self._get_dataflow_modules_no_prefix()
        parent_to_children = self.get_call_graph()

        # When the function itself is not pipelined, ap_ready will be equivalent to
        # ap_done and we can treat it as a feedforward interface. However they are
        # not interchangeable for pipelined functions. See Vitis HLS manual.
        # Currently we do not handle pipelined functions.
        for df_module in df_modules:
            children = parent_to_children[df_module]
            for child in children:
                pp_type = self.get_pipeline_type(child)
                if pp_type == "yes":
                    raise NotImplementedError(
                        f"Found pipelined function {child}, pipelining of ap_ready"
                        " signal might be incorrect"
                    )

    def get_call_graph(self) -> dict[str, list[str]]:
        """Get the call graph of the HLS design.

        Return a map from parent module name to a list of child modules names.
        The module names do not include the prefix.
        """

        def _chatgpt_traverse_tree(
            node: dict[str, Any], module_dict: dict[str, list[str]]
        ) -> None:
            """Build a dictionary that maps each module to its direct children.

            Args:
                node: Current node in the tree.
                module_dict: Dictionary to store the module-child mappings.
            """
            module_name = node["ModuleName"]
            instances = node.get("Instances", [])
            children = []
            for instance in instances:
                child_module = instance["ModuleName"]
                children.append(child_module)
                _chatgpt_traverse_tree(instance, module_dict)
            module_dict[module_name] = children

        parent_to_children: dict[str, list[str]] = {}
        _chatgpt_traverse_tree(self.meta["ModuleInfo"]["Hierarchy"], parent_to_children)

        return parent_to_children

    def get_top_module(self) -> str:
        """Get the top RTL module name."""
        top_module = self.meta["RtlPrefix"] + self.meta["RtlTop"]
        assert isinstance(top_module, str)
        return top_module

    def get_rtl_module_prefix(self) -> str:
        """Get the prefix attached to RTL modules."""
        prefix = self.meta["RtlSubPrefix"]
        assert isinstance(prefix, str)
        return prefix

    def _get_dataflow_modules_no_prefix(self) -> list[str]:
        """Get all dataflow module names without the prefix."""
        df_modules: list[str] = []
        for module in self.meta["ModuleInfo"]["Metrics"]:
            pp_type = self.get_pipeline_type(module)
            if pp_type == "dataflow":
                df_modules.append(module)
            else:
                # Pipeline type can be "loop rewind(delay=... clock cycles(s))"
                match = re.search(
                    r"loop rewind\(delay=.*? clock cycles\(s\)\)", pp_type
                )
                if pp_type not in {"yes", "no"} and not match:
                    raise NotImplementedError(f"Unseen pipeline type {pp_type}")
        return df_modules

    def _get_module_with_prefix(self, mod: str) -> str:
        """Get module name including the prefix."""
        if mod == self.meta["RtlTop"]:
            return self.get_top_module()
        else:
            return f"{self.get_rtl_module_prefix()}{mod}"

    def get_dataflow_modules(self) -> list[str]:
        """Get all dataflow module names including the prefix."""
        # the actual rtl modules may have a prefix.
        # the top module might not have a prefix
        df_modules_with_prefix = [
            self._get_module_with_prefix(mod)
            for mod in self._get_dataflow_modules_no_prefix()
        ]

        if self.get_top_module() not in df_modules_with_prefix:
            raise ValueError(
                f"Top module of solution {self.solution_dir} is not a dataflow module."
                " Check if the dataflow pragma is properly added to the top module."
                " Non-dataflow design is not supported. For the dataflow-in-loop"
                " style, the dataflow pragma needs to be added both inside and outside"
                " the loop."
            )

        return df_modules_with_prefix

    def get_pipeline_type(self, module: str) -> str:
        """Get the pipeline type of a module."""
        ptype = self.meta["ModuleInfo"]["Metrics"][module]["Latency"]["PipelineType"]
        assert isinstance(ptype, str)
        return ptype

    def get_rtl_dir(self) -> str:
        """Get the directory for RTL files."""
        return f"{self.solution_dir}/syn/verilog/"

    def get_report_dir(self) -> str:
        """Get the directory for report files."""
        return f"{self.solution_dir}/syn/report/"

    def get_rtl_files(self) -> list[str]:
        """Get all RTL files."""
        return glob(f"{self.get_rtl_dir()}/*.v")

    def get_tcl_files(self) -> list[str]:
        """Get all tcl files."""
        return glob(f"{self.get_rtl_dir()}/*.tcl")

    def get_module_to_rpt_file(self) -> dict[str, str]:
        """Get a map from rtl module name (with prefix) to report file path."""
        modules_no_prefix = self.meta["ModuleInfo"]["Metrics"].keys()

        prefix = self.get_rtl_module_prefix()
        module_to_rpt = {
            f"{prefix}{mod}": f"{self.solution_dir}/syn/report/{mod}_csynth.xml"
            for mod in modules_no_prefix
        }

        return module_to_rpt

    def get_modules_with_prefix(self) -> list[str]:
        """Get all module names including the prefix."""
        return list(self.get_module_to_rpt_file().keys())

    def get_part_num(self) -> str:
        """Get the target part number."""
        target = self.meta["Target"]
        part_num = target["Device"] + target["Package"] + target["Speed"]
        assert isinstance(part_num, str)
        return part_num

    def get_clock(self) -> tuple[str, float]:
        """Get the clock name and clock period in ns."""
        return self.meta["ClockInfo"]["ClockName"], float(
            self.meta["ClockInfo"]["ClockPeriod"]
        )


def is_dataflow_module(module_name: str, hls_report_dir: str) -> bool:
    """Check if a module is an HLS dataflow module.

    Check the PipelineType field in the HLS report.

    Only report as dataflow if the HLS estimated area percentage is above the
    threshold.

    Examples:
    >>> is_dataflow_module(
    ...     "kernel3_entry14", "tests/thirdparty/vitis_hls/cnn_13x2_report"
    ... )
    False
    >>> is_dataflow_module("kernel3", "tests/thirdparty/vitis_hls/cnn_13x2_report")
    True
    """
    report_path = get_report_path(hls_report_dir, module_name)
    if not report_path:
        return False

    tree = et.parse(report_path)
    pipeline_type_element = tree.find(".//PipelineType")
    if pipeline_type_element is None:
        raise NotImplementedError(f"Cannot find PipelineType in {report_path}.")
    pipeline_type = pipeline_type_element.text

    # check if the pipeline type is dataflow. Match loop rewind pipeline type pattern
    assert isinstance(pipeline_type, str)
    match = re.search(r"loop rewind.*?\(delay=.*? clock cycles\(s\)\)", pipeline_type)
    assert pipeline_type in {"dataflow", "no", "yes", "none"} or match, pipeline_type
    return pipeline_type == "dataflow"


def is_dataflow_module_above_area(
    module_name: str, hls_report_dir: str, area_threshold_pcnt: float
) -> bool:
    """Check if a module is an HLS dataflow module that is not too small.

    Args:
        module_name (str): The name of the module.
        hls_report_dir (str): The directory of HLS reports.
        area_threshold_pcnt (float): The threshold percentage of area. At least one type
            of resource must exceed this percentage.

    Examples:
    >>> is_dataflow_module_above_area(
    ...     "kernel3", "tests/thirdparty/vitis_hls/cnn_13x2_report", 0
    ... )
    True
    >>> is_dataflow_module_above_area(
    ...     "kernel3", "tests/thirdparty/vitis_hls/cnn_13x2_report", 100
    ... )
    False
    """
    if is_dataflow_module(module_name, hls_report_dir):
        area, avail = get_estimated_area(module_name, hls_report_dir)
        if any(used / avail[k] * 100 > area_threshold_pcnt for k, used in area.items()):
            return True

        _logger.info(
            f"Module {module_name} is not marked as dataflow as its area is"
            f" below the threshold percentage of {area_threshold_pcnt}."
        )

    return False


def get_estimated_area(
    module_name: str, hls_report_dir: str
) -> tuple[dict[str, int], dict[str, int]]:
    """Parse HLS report and extract the estimated area.

    Returns two dicts: the estimated usage and total available.

    Examples:
    >>> area = {"BRAM_18K": 507, "DSP48E": 1040, "FF": 166612, "LUT": 143445, "URAM": 0}
    >>> avail = {
    ...     "BRAM_18K": 5376,
    ...     "DSP48E": 12288,
    ...     "FF": 3456000,
    ...     "LUT": 1728000,
    ...     "URAM": 1280,
    ... }
    """
    report_path = get_report_path(hls_report_dir, module_name)
    if not report_path:
        raise ValueError(f"Cannot find report for {module_name} in {hls_report_dir}.")

    tree = et.parse(report_path)
    root = tree.getroot()

    area_section = root.find("AreaEstimates")
    assert area_section is not None

    resources = {}
    available_resources = {}
    for child in area_section:
        if child.tag == "Resources":
            for prop in child:
                assert prop.text
                resources[prop.tag] = int(prop.text)
        elif child.tag == "AvailableResources":
            for prop in child:
                assert prop.text
                available_resources[prop.tag] = int(prop.text)

    assert resources
    assert available_resources
    assert set(resources.keys()) == set(available_resources.keys())

    return resources, available_resources


def get_report_path(
    hls_report_dir: str,
    module_name: str,
) -> str | None:
    """Try to look for the associated report file.

    Examples:
        >>> get_report_path("examples/tapa_vec_add/hls_reports", "VecAdd")
        'examples/tapa_vec_add/hls_reports/VecAdd_csynth.xml'
        >>> get_report_path("examples/tapa_vec_add/hls_reports", "VecAdd_VecAdd")
        'examples/tapa_vec_add/hls_reports/VecAdd_csynth.xml'
        >>> get_report_path("examples/tapa_vec_add/hls_reports", "Add")
        'examples/tapa_vec_add/hls_reports/Add_csynth.xml'
        >>> get_report_path("examples/tapa_vec_add/hls_reports", "VecAdd_Add")
        'examples/tapa_vec_add/hls_reports/Add_csynth.xml'
        >>> get_report_path("examples/tapa_vec_add/hls_reports", "Add_VecAdd")
        'examples/tapa_vec_add/hls_reports/VecAdd_csynth.xml'
        >>> get_report_path("examples/tapa_vec_add/hls_reports", "foo_Add")
        'examples/tapa_vec_add/hls_reports/Add_csynth.xml'
        >>> get_report_path("examples/tapa_vec_add/hls_reports", "foo")

        >>> get_report_path(
        ...     "tests/thirdparty/vitis_hls/cnn_13x2_report", "kernel3_kernel3"
        ... )
        'tests/thirdparty/vitis_hls/cnn_13x2_report/kernel3_csynth.xml'
        >>> get_report_path("tests/thirdparty/vitis_hls/cnn_13x2_report", "kernel3")
        'tests/thirdparty/vitis_hls/cnn_13x2_report/kernel3_csynth.xml'
        >>> get_report_path(
        ...     "tests/thirdparty/vitis_hls/cnn_13x2_report", "kernel3_entry14"
        ... )
        'tests/thirdparty/vitis_hls/cnn_13x2_report/kernel3_entry14_csynth.xml'
        >>> get_report_path("tests/thirdparty/vitis_hls/cnn_13x2_report", "entry14")
        'tests/thirdparty/vitis_hls/cnn_13x2_report/kernel3_entry14_csynth.xml'
    """
    # (1) ideal case
    report_path = f"{hls_report_dir}/{module_name}{REPORT_SFX}"
    if os.path.isfile(report_path):
        _logger.debug("Report path case 1 hit.")
        return report_path

    selected_paths = []

    # (2) needs to remove something from modulename
    for i in range(1, len(module_name)):
        if module_name[i - 1] == "_":
            report_path = f"{hls_report_dir}/{module_name[i:]}{REPORT_SFX}"
            if os.path.isfile(report_path):
                selected_paths.append(report_path)
                _logger.debug("Report path case 2 hit.")
                break

    # (3) needs to add a prefix to modulename
    # select the one with the minimal prefix
    # if there are prefix_foo_bar.xml and prefix_bar.xml, we should select the latter
    report_paths = glob(f"{hls_report_dir}/*_{module_name}{REPORT_SFX}")
    if report_paths:
        selected_paths.append(min(report_paths, key=len))
        _logger.debug("Report path case 3 hit.")

    if len(selected_paths) > 1:
        raise NotImplementedError(
            f"Multiple potential reports for {module_name}: {selected_paths}"
        )

    if not selected_paths:
        _logger.debug("No report found for %s", module_name)
        return None

    return selected_paths[0]
