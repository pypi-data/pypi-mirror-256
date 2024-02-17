from kishu.jupyter.namespace import Namespace
from kishu.planning.planner import CheckpointRestorePlanner, ChangedVariables


def test_checkpoint_restore_planner():
    """
        Test running a few cell updates.
    """
    user_ns = Namespace({})
    planner = CheckpointRestorePlanner(user_ns)

    # Pre run cell 1
    planner.pre_run_cell_update()

    # Post run cell 1
    user_ns["x"] = 1
    planner.post_run_cell_update("x = 1", 1.0)

    # Pre run cell 2
    planner.pre_run_cell_update()

    # Post run cell 2
    user_ns["y"] = 2
    planner.post_run_cell_update("y = x + 1", 1.0)

    variable_snapshots = planner.get_ahg().get_variable_snapshots()
    cell_executions = planner.get_ahg().get_cell_executions()

    # Assert correct contents of AHG.
    assert variable_snapshots.keys() == {"x", "y"}
    assert len(variable_snapshots["x"]) == 1
    assert len(variable_snapshots["y"]) == 1
    assert len(cell_executions) == 2

    # Assert ID graphs are creaated.
    assert len(planner.get_id_graph_map().keys()) == 2

    # Create checkpoint and restore plans.
    checkpoint_plan, restore_plan = planner.generate_checkpoint_restore_plans("fake_path", "fake_commit_id")

    # Assert the plans have appropriate actions.
    assert len(checkpoint_plan.actions) == 1
    assert len(restore_plan.actions) == 2


def test_checkpoint_restore_planner_with_existing_items():
    """
        Test running a few cell updates.
    """
    user_ns = Namespace({"x": 1, "y": 2, "In": ["x = 1", "y = 2"]})

    planner = CheckpointRestorePlanner.from_existing(user_ns)

    variable_snapshots = planner.get_ahg().get_variable_snapshots()
    cell_executions = planner.get_ahg().get_cell_executions()

    # Assert correct contents of AHG. x and y are pessimistically assumed to be modified twice each.
    assert variable_snapshots.keys() == {"x", "y"}
    assert len(variable_snapshots["x"]) == 2
    assert len(variable_snapshots["y"]) == 2
    assert len(cell_executions) == 2

    # Pre run cell 3
    planner.pre_run_cell_update()

    # Pre-running should fill in missing ID graph entries for x and y.
    assert len(planner.get_id_graph_map().keys()) == 2

    # Post run cell 3; x is incremented by 1.
    user_ns["x"] = 2
    planner.post_run_cell_update("x += 1", 1.0)

    # Assert correct contents of AHG is maintained after initializing the planner in a non-empty namespace.
    assert variable_snapshots.keys() == {"x", "y"}
    assert len(variable_snapshots["x"]) == 3
    assert len(variable_snapshots["y"]) == 2
    assert len(cell_executions) == 3


def test_post_run_cell_update_return():
    user_ns = Namespace({})
    planner = CheckpointRestorePlanner(user_ns)

    # Pre run cell 1
    planner.pre_run_cell_update()

    # Post run cell 1
    user_ns["x"] = 1
    changed_vars = planner.post_run_cell_update("x = 1", 1.0)

    assert changed_vars == ChangedVariables(
        created_vars={"x"},
        modified_vars_value=set(),
        modified_vars_structure=set(),
        deleted_vars=set()
    )

    # Pre run cell 2
    planner.pre_run_cell_update()

    # Post run cell 2
    user_ns["z"] = [1, 2]
    user_ns["y"] = 2
    user_ns["x"] = 5
    changed_vars = planner.post_run_cell_update("z = [1, 2]\ny = x + 1\nx = 5", 1.0)

    assert changed_vars == ChangedVariables(
        created_vars={"y", "z"},
        modified_vars_value={"x"},
        modified_vars_structure={"x"},
        deleted_vars=set()
    )

    # Pre run cell 3
    planner.pre_run_cell_update()

    # Post run cell 3
    user_ns["z"] = [1, 2]
    del user_ns["x"]
    changed_vars = planner.post_run_cell_update("z = [1, 2]\ndel x", 1.0)

    assert changed_vars == ChangedVariables(
        created_vars=set(),
        modified_vars_value=set(),
        modified_vars_structure={"z"},
        deleted_vars={"x"},
    )
