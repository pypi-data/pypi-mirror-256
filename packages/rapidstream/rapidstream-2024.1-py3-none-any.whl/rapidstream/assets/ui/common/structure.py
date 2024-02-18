"""The constants for RapidStream project directory structure."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

import logging
from pathlib import Path

_logger = logging.getLogger(__name__)

D_CREATING_PROJECT = 'Creating project directory structure under "%s"...'


# The directory structure of a RapidStream project
#   - <project_dir>/
#       - generated/
#       - configs/
#           - importer_config.json
#       - passes/
#           - 0-imported.json
#           - <pass_order>-<pass_name>.json
#       - exported/
#           - design/
#           - xdc/
#               - floorplan.xdc
#               - clocks.xdc
#           - impl/
#       - dse/
#           - candidate_<candidate_id>/
#              - add_pipeline.json
#              - add_pipeline.log
#              - ... exported design files
#       - logs/
#           - 0-importer.log
#           - <pass_order>-<pass_name>.log
#           - Z-exporter.log
#           - Z-dse.log

GENERATED_PATH = Path("generated")
GENERATED_XO_DIR = GENERATED_PATH / Path("xo")
GENERATED_PACKAGE_XO_DIR = GENERATED_PATH / Path("package_xo")

CONFIGS_PATH = Path("configs")
IMPORTER_CONFIG_PATH = CONFIGS_PATH / "importer_config.json"
PORT_PREASSIGN_CONFIG_PATH = CONFIGS_PATH / "port_preassign_config.json"
CELL_PREASSIGN_CONFIG_PATH = CONFIGS_PATH / "cell_preassign_config.json"

PASSES_PATH = Path("passes")
IMPORTED_JSON_PATH = PASSES_PATH / "0-imported.json"

EXPORTED_PATH = Path("exported")
EXPORTED_DESIGN_PATH = EXPORTED_PATH / "design"
EXPORTED_XDC_PATH = EXPORTED_PATH / "xdc"
EXPORTER_XDC_FLOORPLAN_PATH = EXPORTED_XDC_PATH / "floorplan.xdc"
EXPORTER_XDC_CLOCKS_PATH = EXPORTED_XDC_PATH / "clocks.xdc"
EXPORTED_IMPL_PATH = EXPORTED_PATH / "impl"

DSE_PATH = Path("dse")
DSE_CANDIDATE_PATH = "candidate_{idx}"
DSE_ADD_PIPELINE_PATH = "add_pipeline.json"
DSE_ADD_PIPELINE_LOG_PATH = "add_pipeline.log"

LOGS_PATH = Path("logs")
IMPORTER_LOG_PATH = LOGS_PATH / "0-importer.log"
EXPORTER_LOG_PATH = LOGS_PATH / "Z-exporter.log"
PBLOCK_GEN_LOG_PATH = LOGS_PATH / "Z-pblock-gen.log"
DSE_LOG_PATH = LOGS_PATH / "Z-dse.log"

GET_AREA_PATH = Path("get_area")

SPLIT_AUX_PATH = Path("split_aux")

ALL_PROJECT_PATHS = (
    CONFIGS_PATH,
    DSE_PATH,
    EXPORTED_DESIGN_PATH,
    EXPORTED_IMPL_PATH,
    EXPORTED_PATH,
    EXPORTED_XDC_PATH,
    GET_AREA_PATH,
    LOGS_PATH,
    PASSES_PATH,
    SPLIT_AUX_PATH,
)


def create_project_dirs(project_dir: Path) -> None:
    """Creates the directory structure of a RapidStream project."""
    _logger.debug(D_CREATING_PROJECT, project_dir)
    for path in ALL_PROJECT_PATHS:
        (project_dir / path).mkdir(parents=True, exist_ok=True)


def get_pass_json_rel_path(pass_id: int, pass_name: str) -> Path:
    """Returns the relative path to the pass json."""
    return PASSES_PATH / f"{pass_id}-{pass_name}.json"


def get_pass_log_rel_path(pass_id: int, pass_name: str) -> Path:
    """Returns the relative path to the pass log."""
    return LOGS_PATH / f"{pass_id}-{pass_name}.log"
