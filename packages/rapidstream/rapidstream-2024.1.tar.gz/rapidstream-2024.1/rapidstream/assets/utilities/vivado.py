"""Internal utilities for Vivado-related operations."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging
import shutil
import tempfile
from glob import glob
from pathlib import Path

import pandas as pd

from rapidstream.assets.cluster.tasks.vivado import run_vivado_xci_generation
from rapidstream.assets.cluster.util import check_async_command

_logger = logging.getLogger().getChild(__name__)


def generate_xci_from_tcl(tcl_files: list[str], part_num: str, output_dir: str) -> None:
    """Source the tcls and get the corresponding IP .xci files."""
    _logger.info("Generating xci files from HLS tcl files with Vivado")

    # check that "create_ip" command is in the tcl files
    for tcl_file in tcl_files:
        with open(tcl_file, "r", encoding="utf-8") as fp:
            if "create_ip" not in fp.read():
                raise ValueError(f"{tcl_file} does not contain create_ip command")

    # generate the xci files from the tcl files
    with tempfile.TemporaryDirectory() as temp_dir:
        tcl = []

        tcl += [f"create_project {temp_dir}/project -part {part_num}"]
        for tcl_file in tcl_files:
            tcl += [f"source {tcl_file}"]

        tcl_path = f"{temp_dir}/vivado.tcl"
        with open(tcl_path, "w", encoding="utf-8") as fp:
            fp.write("\n".join(tcl))

        # call vivado to instantiate the xci files
        check_async_command(
            run_vivado_xci_generation.submit(Path(tcl_path), Path(temp_dir))
        )

        # copy the generated xci files to the output directory
        xci_files = glob(f"{temp_dir}/**/*.xci", recursive=True)
        for xci_file in xci_files:
            shutil.move(xci_file, output_dir)

    _logger.info("Finished generating xci files")


def get_clocks_max_frequency(timing_report_path: str) -> dict[str, float]:
    """Parse the timing report and return the frequency values for each clock.

    Args:
        timing_report_path (str): The path to the timing report.

    Returns:
        dict[str, float]: The frequency values for each clock.

    Examples:
        >>> path = (
        ...     "tests/thirdparty/vivado/timing_report_parser/impl_timing_summary.rpt"
        ... )
        >>> frequency_values = get_clocks_max_frequency(path)
        >>> round(frequency_values["ap_clk"], 2)
        374.11
    """
    _, clock_table = parse_timing_report(timing_report_path)
    clocks = clock_table[clock_table["Clock_x"].notna()]
    # Period(ns) = 1000 / Frequency(MHz)
    # Minimum period(ns) = Period(ns) - WNS(ns)
    # Maximum operating frequency(MHz) = 1000 / Minimum period(ns)
    return {
        # Compute the maximum frequency from the wns and the target frequency
        clock: 1000 / (1000 / float(frequency) - float(wns))
        for clock, frequency, wns in zip(
            clocks["Clock_x"],
            clocks["Frequency(MHz)_x"],
            clocks["WNS(ns)"],
            strict=True,
        )
    }


def parse_timing_report(
    timing_report_path: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse the timing report.

    Args:
        timing_report_path: The path to the timing report.

    Returns:
        The timing report as a pandas dataframe.
    >>> path = "tests/thirdparty/vivado/timing_report_parser/impl_timing_summary.rpt"
    >>> design_timing_summary, clock_table = parse_timing_report(path)
    >>> design_timing_summary_expected = pd.read_csv(
    ...     "tests/thirdparty/vivado/timing_report_parser/design_timing_summary.csv",
    ...     dtype=str,
    ... )
    >>> clock_table_expected = pd.read_csv(
    ...     "tests/thirdparty/vivado/timing_report_parser/clock_table.csv",
    ...     dtype=str,
    ... )
    >>> pd.testing.assert_frame_equal(
    ...     design_timing_summary,
    ...     design_timing_summary_expected,
    ... )
    >>> pd.testing.assert_frame_equal(clock_table, clock_table_expected)
    """
    with open(timing_report_path, "r", encoding="utf-8") as timing_report_file:
        timing_report_lines = timing_report_file.readlines()

    timing_report_lines = [line.strip() for line in timing_report_lines]
    design_timing_summary = parse_report_content(
        timing_report_lines, "Design Timing Summary"
    )
    clock_summary = parse_report_content(timing_report_lines, "Clock Summary")
    inter_clock_table = parse_report_content(timing_report_lines, "Inter Clock Table")
    intra_clock_table = parse_report_content(timing_report_lines, "Intra Clock Table")
    other_path_groups_table = parse_report_content(
        timing_report_lines, "Other Path Groups Table"
    )
    clock_table = pd.concat(
        [intra_clock_table, inter_clock_table, other_path_groups_table],
        ignore_index=True,
    )
    clock_table = pd.merge(clock_table, clock_summary, on="Clock", how="left")
    clock_table = pd.merge(
        clock_table,
        clock_summary,
        left_on="From Clock",
        right_on="Clock",
        how="left",
    )
    clock_table = pd.merge(
        clock_table,
        clock_summary,
        left_on="To Clock",
        right_on="Clock",
        how="left",
    )

    return design_timing_summary, clock_table


def parse_report_content(timing_report_lines: list[str], title: str) -> pd.DataFrame:
    """Parse the report content.

    Args:
        timing_report_lines: The lines of the timing report.
        title: The subtitle in the report to parse.

    Returns:
        The report content of the title as a dataframe.

    example:
    >>> path = "tests/thirdparty/vivado/timing_report_parser/impl_timing_summary.rpt"
    >>> with open(path, "r") as timing_report_file:
    ...     timing_report_lines = timing_report_file.readlines()
    ...
    >>> timing_report_lines = [line.strip() for line in timing_report_lines]
    >>> report_content = parse_report_content(timing_report_lines, "Clock Summary")
    >>> print(report_content)  # doctest: +NORMALIZE_WHITESPACE
        Clock   Waveform(ns) Period(ns) Frequency(MHz)
    0  ap_clk  {0.000 1.250}      2.500        400.000
    1    clk1  {0.000 0.000}          0              0
    2    clk2  {0.000 0.000}          0              0
    """
    start_index = timing_report_lines.index("| " + title)
    columns_titles = [
        column.strip()
        # use double space to split the columns to deal with space in the column name
        for column in (timing_report_lines[start_index + 4]).split("  ")
        if column != ""
    ]
    end_index = timing_report_lines.index("", start_index + 6)
    if end_index == start_index + 6:
        return pd.DataFrame(columns=columns_titles)
    data_list = []
    for i in range(start_index + 6, end_index):
        data_list.append(
            [data for data in timing_report_lines[i].split("  ") if data != ""]
        )
    data_list_transpose = [list(column) for column in zip(*data_list, strict=True)]
    assert len(columns_titles) == len(data_list_transpose)
    return pd.DataFrame(
        {title: data_list_transpose[i] for i, title in enumerate(columns_titles)}
    )
