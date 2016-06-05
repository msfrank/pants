from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants.base.payload import Payload
from pants.base.payload_field import PrimitiveField
from pants.base.exceptions import TargetDefinitionException


import logging
logger = logging.getLogger(__name__)


class ScalaAvroLibrary(JvmTarget):
    """
    """

    def __init__(self, payload=None, definition_type=None, **kwargs):
        """
        """
        logger.info("ScalaAvroLibrary: __init__")
        payload = payload or Payload()
        super(ScalaAvroLibrary, self).__init__(payload=payload, **kwargs)
        self.add_labels('codegen', 'avro')

        if not definition_type in ('standard', 'specific', 'scavro'):
            raise TargetDefinitionException(self, 'unknown definition_type {}'.format(definition_type))
        self._definition_type = definition_type

    @property
    def definition_type(self):
        return self._definition_type
