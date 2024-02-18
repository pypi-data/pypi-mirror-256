#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple

from mitosheet.code_chunks.code_chunk import CodeChunk
from mitosheet.code_chunks.empty_code_chunk import EmptyCodeChunk
from mitosheet.state import State
from mitosheet.step_performers.step_performer import StepPerformer
from mitosheet.step_performers.utils.utils import get_param
from mitosheet.types import GraphID


class GraphDuplicateStepPerformer(StepPerformer):
    """
    This steps duplicates a graph of a given graphID. 
    """

    @classmethod
    def step_version(cls) -> int:
        return 1

    @classmethod
    def step_type(cls) -> str:
        return 'graph_duplicate'

    @classmethod
    def execute(cls, prev_state: State, params: Dict[str, Any]) -> Tuple[State, Optional[Dict[str, Any]]]:
        old_graph_id: GraphID = get_param(params, 'old_graph_id')
        new_graph_id: GraphID = get_param(params, 'new_graph_id')

        post_state = prev_state.copy()

        graph_copy = deepcopy(post_state.graph_data_dict[old_graph_id])
        # We don't need to insist the the graph names are unique because they are just used in 
        # the sheet tab display. They aren't used in generated code or to identify graphs in the steps
        graph_copy["graphTabName"] = graph_copy["graphTabName"] + '_copy'        
        post_state.graph_data_dict[new_graph_id] = graph_copy
        
        return post_state, {
            'pandas_processing_time': 0 # No time spent on pandas, only metadata changes
        }

    @classmethod
    def transpile(
        cls,
        prev_state: State,
        params: Dict[str, Any],
        execution_data: Optional[Dict[str, Any]],
    ) -> List[CodeChunk]:

        # Graph steps don't add any generated code to the analysis script. 
        return [
            EmptyCodeChunk(
                prev_state, 
                'Duplicated graph',
                'Duplicated a graph',
            )
        ]
    
    @classmethod
    def get_modified_dataframe_indexes(cls, params: Dict[str, Any]) -> Set[int]:
        return {-1}
