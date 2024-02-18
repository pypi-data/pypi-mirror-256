"""Objects encoding how to partition the root PNode."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from pydantic import BaseModel, ConfigDict

from rapidstream.assets.device.common import RESOURCES, Coor, get_coor

DEFAULT_USAGE_LIMIT = {rtype: 0.7 for rtype in RESOURCES}


class ChildConfig(BaseModel):
    """A partition operation records the parameter of a child node."""

    model_config = ConfigDict(frozen=True)

    coor: Coor
    usage_limit: dict[str, float]

    def __hash__(self) -> int:
        """Hash."""
        return hash((self.coor, frozenset(self.usage_limit.items())))


class PartitionOp(BaseModel):
    """A partition operation splits a device one more time."""

    model_config = ConfigDict(frozen=True)

    target_node: Coor
    children_configs: tuple[ChildConfig, ...]


class PartitionSchedule(BaseModel):
    """In what order and what shape do we do the partitions."""

    model_config = ConfigDict(frozen=True)

    op_groups: tuple[tuple[PartitionOp, ...], ...]


class PartitionOpFactory:
    """A factory to create partition operations."""

    def __init__(
        self,
        target_node: Coor,
        default_usage_limit: dict[str, float],
    ) -> None:
        """Initialize a partition operation factory."""
        self.target_node = target_node
        self.coor_to_child_config: dict[Coor, ChildConfig] = {}
        self.default_usage_limit = default_usage_limit

    def add_child_config(
        self, coor: Coor, usage_limit: dict[str, float] | None = None
    ) -> None:
        """Add a child config."""
        if usage_limit is None:
            usage_limit = self.default_usage_limit
        self.coor_to_child_config[coor] = ChildConfig(
            coor=coor, usage_limit=usage_limit
        )

    def drc_check(self) -> None:
        """Check if the children configs perfectly cover the target node."""
        child_coors = [
            child_config.coor for child_config in self.coor_to_child_config.values()
        ]
        if not self.target_node.is_perfectly_covered_by(child_coors):
            raise ValueError("Children configs do not perfectly cover the target node")

    def get_partition_op(self) -> PartitionOp:
        """Get the partition operation."""
        self.drc_check()
        return PartitionOp(
            target_node=self.target_node,
            children_configs=tuple(self.coor_to_child_config.values()),
        )

    def update_child_usage_limit(
        self, coor: Coor, usage_limit: dict[str, float]
    ) -> None:
        """Update the usage limit of a child."""
        for key, value in usage_limit.items():
            if value > 1.0:
                raise ValueError(f"Usage limit {value} for resource {key} exceeds 1.0")
        self.coor_to_child_config[coor] = self.coor_to_child_config[coor].model_copy(
            update={"usage_limit": usage_limit}
        )

    def incr_child_usage_limit(self, coor: Coor, incr: float) -> None:
        """Increase the usage limit of a child."""
        curr_limit = self.coor_to_child_config[coor].usage_limit
        updated_limit = {rtype: limit + incr for rtype, limit in curr_limit.items()}
        for key, value in updated_limit.items():
            if value > 1.00001:  # floating point error
                raise ValueError(f"Usage limit {value} for resource {key} exceeds 1.0")
        self.coor_to_child_config[coor] = self.coor_to_child_config[coor].model_copy(
            update={"usage_limit": updated_limit}
        )

    def update_all_child_usage_limit(self, usage_limit: dict[str, float]) -> None:
        """Update the usage limit of all children."""
        for coor in self.coor_to_child_config:
            self.update_child_usage_limit(coor, usage_limit)


class ScheduleFactory:
    """A factory to create partition schedules."""

    def __init__(self) -> None:
        """Initialize a schedule factory."""
        self.op_group_factories: list[list[PartitionOpFactory]] = []

    def add_op_group(self, op_group: list[PartitionOpFactory]) -> None:
        """Add an operation group."""
        # check for overlaps
        for f1 in op_group:
            for f2 in op_group:
                if f1.target_node == f2.target_node:
                    continue

                if f1.target_node.has_overlap(f2.target_node):
                    raise ValueError("Operation groups have overlapping target nodes")

        self.op_group_factories.append(op_group)

    def set_all_child_slot_usage_limit(self, usage_limit: dict[str, float]) -> None:
        """Set the usage limit of all child slots."""
        for op_group_factory in self.op_group_factories:
            for factory in op_group_factory:
                factory.update_all_child_usage_limit(usage_limit)

    def set_all_child_slot_all_type_limit(self, limit: float) -> None:
        """Set the usage limit of all child slots for all resource types."""
        usage_limit = {rtype: limit for rtype in RESOURCES}
        self.set_all_child_slot_usage_limit(usage_limit)

    def incr_all_child_slot_usage_limit(self, incr: float) -> None:
        """Increase the usage limit of all child slots."""
        for op_group_factory in self.op_group_factories:
            for factory in op_group_factory:
                for coor in factory.coor_to_child_config:
                    factory.incr_child_usage_limit(coor, incr)

    def generate_schedule(self, output_path: str | None = None) -> PartitionSchedule:
        """Generate the schedule."""
        op_groups: list[tuple[PartitionOp, ...]] = []
        for op_group_factory in self.op_group_factories:
            op_groups.append(
                tuple(factory.get_partition_op() for factory in op_group_factory)
            )

        schedule = PartitionSchedule(op_groups=tuple(op_groups))
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(schedule.model_dump_json(indent=2))

        return schedule


def get_grid_one_iter_factory(num_row: int, num_col: int) -> ScheduleFactory:
    """Get a default one-iteration partition schedule."""
    op_fac = PartitionOpFactory(
        get_coor(0, 0, num_col - 1, num_row - 1), DEFAULT_USAGE_LIMIT
    )
    for x in range(num_col):
        for y in range(num_row):
            op_fac.add_child_config(get_coor(x, y, x, y))

    sche_fac = ScheduleFactory()
    sche_fac.add_op_group([op_fac])
    return sche_fac


def get_grid_two_iter_factory(num_row: int, num_col: int) -> ScheduleFactory:
    """Get a first-row-then-col two-iteration partition schedule."""
    sche_fac = ScheduleFactory()

    # level 1, split into SLR-level slot
    op_fac1 = PartitionOpFactory(
        get_coor(0, 0, num_col - 1, num_row - 1), DEFAULT_USAGE_LIMIT
    )
    for y in range(num_row):
        op_fac1.add_child_config(get_coor(0, y, num_col - 1, y))
    sche_fac.add_op_group([op_fac1])

    # level 2, split each SLR-level slot
    op_fac_l2 = []
    for y in range(num_row):
        fac = PartitionOpFactory(get_coor(0, y, num_col - 1, y), DEFAULT_USAGE_LIMIT)
        for x in range(num_col):
            fac.add_child_config(get_coor(x, y, x, y))
        op_fac_l2.append(fac)
    sche_fac.add_op_group(op_fac_l2)

    return sche_fac


def get_schedule_factory(num_row: int, num_col: int) -> ScheduleFactory:
    """Get a partition schedule factory."""
    if num_row * num_col <= 6:
        return get_grid_one_iter_factory(num_row, num_col)
    elif num_row * num_col <= 12:
        return get_grid_two_iter_factory(num_row, num_col)
    else:
        raise NotImplementedError("Partition schedule for >12 slots not implemented")
