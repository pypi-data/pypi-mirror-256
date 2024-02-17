#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""
Mixin to be used by service sources to dynamically
generate the _run based on their topology.
"""
import traceback
from functools import singledispatchmethod
from typing import Any, Dict, Generic, Iterable, List, TypeVar, Union

from pydantic import BaseModel

from metadata.generated.schema.api.data.createStoredProcedure import (
    CreateStoredProcedureRequest,
)
from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.entity.data.storedProcedure import StoredProcedure
from metadata.ingestion.api.models import Either, Entity
from metadata.ingestion.models.custom_properties import OMetaCustomProperties
from metadata.ingestion.models.ometa_classification import OMetaTagAndClassification
from metadata.ingestion.models.patch_request import PatchRequest
from metadata.ingestion.models.topology import (
    NodeStage,
    ServiceTopology,
    TopologyContext,
    TopologyNode,
    get_ctx_default,
    get_topology_node,
    get_topology_root,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.ingestion.ometa.utils import model_str
from metadata.utils import fqn
from metadata.utils.logger import ingestion_logger
from metadata.utils.source_hash_utils import (
    SOURCE_HASH_EXCLUDE_FIELDS,
    generate_source_hash,
)

logger = ingestion_logger()

C = TypeVar("C", bound=BaseModel)

CACHED_ENTITIES = "cached_entities"


class MissingExpectedEntityAckException(Exception):
    """
    After running the ack to the sink, we got no
    Entity back
    """


class TopologyRunnerMixin(Generic[C]):
    """
    Prepares the _run function
    dynamically based on the source topology
    """

    topology: ServiceTopology
    context: TopologyContext
    metadata: OpenMetadata

    def process_nodes(self, nodes: List[TopologyNode]) -> Iterable[Entity]:
        """
        Given a list of nodes, either roots or children,
        yield from its producers and process the children.

        The execution tree is created in a depth-first fashion.

        :param nodes: Topology Nodes to process
        :return: recursively build the execution tree
        """
        for node in nodes:
            logger.debug(f"Processing node {node}")
            node_producer = getattr(self, node.producer)
            child_nodes = (
                [get_topology_node(child, self.topology) for child in node.children]
                if node.children
                else []
            )

            for element in node_producer() or []:
                for stage in node.stages:
                    logger.debug(f"Processing stage: {stage}")

                    stage_fn = getattr(self, stage.processor)
                    for entity_request in stage_fn(element) or []:
                        try:
                            # yield and make sure the data is updated
                            yield from self.sink_request(
                                stage=stage, entity_request=entity_request
                            )
                        except ValueError as err:
                            logger.debug(traceback.format_exc())
                            logger.warning(
                                f"Unexpected value error when processing stage: [{stage}]: {err}"
                            )

                    # init the cache dict
                    if stage.cache_entities:
                        self._init_cache_dict(stage=stage, child_nodes=child_nodes)

                # processing for all stages completed now cleaning the cache if applicable
                for stage in node.stages:
                    if stage.clear_cache:
                        self.clear_context(stage=stage)

                # process all children from the node being run
                yield from self.process_nodes(child_nodes)

            if node.post_process:
                logger.debug(f"Post processing node {node}")
                for process in node.post_process:
                    try:
                        yield from self.check_context_and_handle(process)
                    except Exception as exc:
                        logger.debug(traceback.format_exc())
                        logger.warning(
                            f"Could not run Post Process `{process}` from Topology Runner -- {exc}"
                        )

    def _init_cache_dict(self, stage: NodeStage, child_nodes: List[TopologyNode]):
        """
        Method to call the API to fill the entities cache
        """

        if not self.context.__dict__.get(CACHED_ENTITIES):
            self.context.__dict__[CACHED_ENTITIES] = {}
        for child_node in child_nodes or []:
            for child_stage in child_node.stages or []:
                if child_stage.use_cache:
                    entity_fqn = self.fqn_from_context(
                        stage=stage,
                        entity_name=self.context.__dict__[stage.context],
                    )

                    if not self.context.__dict__[CACHED_ENTITIES].get(
                        child_stage.type_
                    ):
                        self.context.__dict__[CACHED_ENTITIES][child_stage.type_] = {}

                    self.get_fqn_source_hash_dict(
                        parent_type=stage.type_,
                        child_type=child_stage.type_,
                        entity_fqn=entity_fqn,
                    )

    def get_fqn_source_hash_dict(
        self, parent_type: Entity, child_type: Entity, entity_fqn: str
    ) -> Dict:
        """
        Get all the entities and store them as fqn:sourceHash in a dict
        """
        params = {}
        if parent_type in (Database, DatabaseSchema):
            if child_type == StoredProcedure:
                params = {"databaseSchema": entity_fqn}
            else:
                params = {"database": entity_fqn}
        else:
            params = {"service": entity_fqn}
        entities_list = self.metadata.list_all_entities(
            entity=child_type,
            params=params,
            fields=["sourceHash"],
        )
        for entity in entities_list:
            if entity.sourceHash:
                self.context.__dict__[CACHED_ENTITIES][child_type][
                    model_str(entity.fullyQualifiedName)
                ] = entity.sourceHash

    def check_context_and_handle(self, post_process: str):
        """Based on the post_process step, check context and
        evaluate if we can run it based on available class attributes

        Args:
            post_process: the name of the post_process step
        """
        if post_process == "mark_tables_as_deleted" and not self.context.database:
            raise ValueError("No Database found in  `self.context`")

        node_post_process = getattr(self, post_process)
        for entity_request in node_post_process():
            yield entity_request

    def _iter(self) -> Iterable[Either]:
        """
        This is the implementation for the entrypoint of our Source classes, which
        are an IterStep

        Based on a ServiceTopology, find the root node
        and fetch all source methods in the required order
        to yield data to the sink
        :return: Iterable of the Entities yielded by all nodes in the topology
        """
        yield from self.process_nodes(get_topology_root(self.topology))

    def _replace_context(self, key: str, value: Any) -> None:
        """
        Update the key of the context with the given value
        :param key: element to update from the source context
        :param value: value to use for the update
        """
        self.context.__dict__[key] = value

    def _append_context(self, key: str, value: Any) -> None:
        """
        Update the key of the context with the given value
        :param key: element to update from the source context
        :param value: value to use for the update
        """
        self.context.__dict__[key].append(value)

    def clear_context(self, stage: NodeStage) -> None:
        """
        Clear the available context
        :param key: element to update from the source context
        """
        self.context.__dict__[stage.context] = get_ctx_default(stage)

    def fqn_from_context(self, stage: NodeStage, entity_name: str) -> str:
        """
        Read the context
        :param stage: Topology node being processed
        :param entity_request: Request sent to the sink
        :return: Entity FQN derived from context
        """
        context_names = [
            self.context.__dict__[dependency]
            for dependency in stage.consumer or []  # root nodes do not have consumers
        ]
        return fqn._build(  # pylint: disable=protected-access
            *context_names, entity_name
        )

    def update_context(
        self, stage: NodeStage, context: Union[str, OMetaTagAndClassification]
    ):
        """Append or update context"""
        # We'll store the entity_name in the topology context instead of the entity_fqn
        # and build the fqn on the fly wherever required.
        # This is mainly because we need the context in other places
        if stage.context and not stage.cache_all:
            self._replace_context(key=stage.context, value=context)
        if stage.context and stage.cache_all:
            self._append_context(key=stage.context, value=context)

    def create_patch_request(
        self, original_entity: Entity, create_request: C
    ) -> PatchRequest:
        """
        Method to get the PatchRequest object
        To be overridden by the process if any custom logic is to be applied
        """
        return PatchRequest(
            original_entity=original_entity,
            new_entity=original_entity.copy(update=create_request.__dict__),
        )

    @singledispatchmethod
    def yield_and_update_context(
        self,
        right: C,
        stage: NodeStage,
        entity_request: Either[C],
    ) -> Iterable[Either[Entity]]:
        """
        Handle the process of yielding the request and validating
        that everything was properly updated.

        The default implementation is based on a get_by_name validation
        """
        entity = None
        entity_name = model_str(right.name)
        entity_fqn = self.fqn_from_context(stage=stage, entity_name=entity_name)

        # we get entity from OM if we do not want to overwrite existing data in OM
        # This will be applicable for service entities since we do not want to overwrite the data
        if not stage.overwrite and not self._is_force_overwrite_enabled():
            entity = self.metadata.get_by_name(
                entity=stage.type_,
                fqn=entity_fqn,
                fields=["*"],  # Get all the available data from the Entity
            )
        create_entity_request_hash = generate_source_hash(
            create_request=entity_request.right,
            exclude_fields=SOURCE_HASH_EXCLUDE_FIELDS,
        )

        if hasattr(entity_request.right, "sourceHash"):
            entity_request.right.sourceHash = create_entity_request_hash

        skip_processing_entity = False
        if entity is None and stage.use_cache:
            # check if we find the entity in the entities list
            entity_source_hash = self.context.__dict__[CACHED_ENTITIES][
                stage.type_
            ].get(entity_fqn)
            if entity_source_hash:
                # if the source hash is present, compare it with new hash
                if entity_source_hash != create_entity_request_hash:
                    # the entity has changed, get the entity from server and make a patch request
                    entity = self.metadata.get_by_name(
                        entity=stage.type_,
                        fqn=entity_fqn,
                        fields=["*"],  # Get all the available data from the Entity
                    )

                    # we return the entity for a patch update
                    if entity:
                        patch_entity = self.create_patch_request(
                            original_entity=entity, create_request=entity_request.right
                        )
                        entity_request.right = patch_entity
                else:
                    # nothing has changed on the source skip the API call
                    logger.debug(
                        f"No changes detected for {str(stage.type_.__name__)} '{entity_fqn}'"
                    )
                    skip_processing_entity = True

        if not skip_processing_entity:
            # We store the generated source hash and yield the request

            yield entity_request

        # We have ack the sink waiting for a response, but got nothing back
        if stage.must_return and entity is None:
            # we'll only check the get by name for entities like database service
            # without which we cannot proceed ahead in the ingestion
            tries = 3
            while not entity and tries > 0:
                entity = self.metadata.get_by_name(
                    entity=stage.type_,
                    fqn=entity_fqn,
                    fields=["*"],  # Get all the available data from the Entity
                )
                tries -= 1

            if not entity:
                # Safe access to Entity Request name
                raise MissingExpectedEntityAckException(
                    f"Missing ack back from [{stage.type_.__name__}: {entity_fqn}] - "
                    "Possible causes are changes in the server Fernet key or mismatched JSON Schemas "
                    "for the service connection."
                )

        self.update_context(stage=stage, context=entity_name)

    @yield_and_update_context.register
    def _(
        self,
        right: AddLineageRequest,
        stage: NodeStage,
        entity_request: Either[C],
    ) -> Iterable[Either[Entity]]:
        """
        Lineage Implementation for the context information.

        There is no simple (efficient) validation to make sure that this specific
        lineage has been properly drawn. We'll skip the process for now.
        """
        yield entity_request
        self.update_context(stage=stage, context=right.edge.fromEntity.name.__root__)

    @yield_and_update_context.register
    def _(
        self,
        right: OMetaTagAndClassification,
        stage: NodeStage,
        entity_request: Either[C],
    ) -> Iterable[Either[Entity]]:
        """Tag implementation for the context information"""
        yield entity_request

        # We'll keep the tag fqn in the context and use if required
        self.update_context(stage=stage, context=right)

    @yield_and_update_context.register
    def _(
        self,
        right: OMetaCustomProperties,
        stage: NodeStage,
        entity_request: Either[C],
    ) -> Iterable[Either[Entity]]:
        """Custom Property implementation for the context information"""
        yield entity_request

        # We'll keep the tag fqn in the context and use if required
        self.update_context(stage=stage, context=right)

    @yield_and_update_context.register
    def _(
        self,
        right: CreateStoredProcedureRequest,
        stage: NodeStage,
        entity_request: Either[C],
    ) -> Iterable[Either[Entity]]:
        """Tag implementation for the context information"""
        yield entity_request

        procedure_fqn = fqn.build(
            metadata=self.metadata,
            entity_type=StoredProcedure,
            service_name=self.context.database_service,
            database_name=self.context.database,
            schema_name=self.context.database_schema,
            procedure_name=right.name.__root__,
        )

        # We'll keep the tag fqn in the context and use if required
        self.update_context(stage=stage, context=procedure_fqn)

    def sink_request(
        self, stage: NodeStage, entity_request: Either[C]
    ) -> Iterable[Either[Entity]]:
        """
        Validate that the entity was properly updated or retry if
        ack_sink is flagged.

        If we get the Entity back, update the context with it.

        :param stage: Node stage being processed
        :param entity_request: Request to pass
        :return: Entity generator
        """

        # Either use the received request or the acknowledged Entity
        entity = entity_request.right if entity_request else None

        if not stage.nullable and entity is None and entity_request.left is None:
            raise ValueError("Value unexpectedly None")

        if entity_request is not None:
            # Check that we properly received a Right response to process
            if entity_request.right is not None:
                # We need to acknowledge that the Entity has been properly sent to the server
                # to update the context
                if stage.context:
                    yield from self.yield_and_update_context(
                        entity, stage=stage, entity_request=entity_request
                    )

                else:
                    yield entity_request

            else:
                # if entity_request.right is None, means that we have a Left. We yield the Either and
                # let the step take care of the
                yield entity_request

    def _is_force_overwrite_enabled(self) -> bool:
        return self.metadata.config and self.metadata.config.forceEntityOverwriting
