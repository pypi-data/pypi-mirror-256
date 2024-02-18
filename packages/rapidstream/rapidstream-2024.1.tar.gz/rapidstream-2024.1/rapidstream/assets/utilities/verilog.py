"""Internal utilities for simple Verilog code parsing."""

__copyright__ = """
Copyright 2024 RapidStream Design Automation, Inc.
All Rights Reserved.
"""

from collections import defaultdict
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor, as_completed

import pyslang as sl
from pyslang import SyntaxKind as sk


def get_call_graph(src_files: list[str]) -> dict[str, set[str]]:
    """Get the call graph of the design."""
    final_call_graph = defaultdict(set)

    with ProcessPoolExecutor() as executor:
        # Obtain the call graph for each file in parallel
        future_to_file = {
            executor.submit(get_call_graph_single_file, file): file
            for file in src_files
        }

        for future in as_completed(future_to_file):
            file_call_graph = future.result()
            # Merge the individual file call graphs into the final call graph
            for module, submodules in file_call_graph.items():
                final_call_graph[module].update(submodules)

    return dict(final_call_graph)


def get_call_graph_single_file(file_path: str) -> dict[str, set[str]]:
    """Process a single file to contribute to the call graph."""
    call_graph = defaultdict(set)
    tree = sl.SyntaxTree.fromFile(file_path)
    for node in traverse_preorder(tree.root):
        if node.kind == sk.ModuleDeclaration:
            module_name = str(node.header.name.value)
            for submodule_name in get_submodule_names(node):
                call_graph[module_name].add(submodule_name)
    return dict(call_graph)


def get_submodule_names(module: sl.ModuleDeclarationSyntax) -> set[str]:
    """Return the names of the child modules of a module contains submodules."""
    names = set()
    for node in traverse_preorder(module):
        if node.kind == sk.HierarchyInstantiation:
            names.add(str(node.type.value))
    return names


def traverse_preorder(node: sl.SyntaxNode) -> Iterator[sl.SyntaxNode | sl.Token]:
    """Traverse the syntax tree and yield visited nodes preorder."""
    yield node
    if isinstance(node, sl.SyntaxNode):
        for child in node:
            yield from traverse_preorder(child)
