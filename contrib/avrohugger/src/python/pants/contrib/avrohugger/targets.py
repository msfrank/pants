from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants.base.payload import Payload
from pants.base.payload_field import PrimitiveField


import logging
logger = logging.getLogger(__name__)


class ScalaAvroLibrary(JvmTarget):
    """
    """

    def __init__(self, payload=None, buildflags=None, imports=None, **kwargs):
        """
        """
        logger.info("ScalaAvroLibrary: __init__")
        payload = payload or Payload()
        super(ScalaAvroLibrary, self).__init__(payload=payload, **kwargs)
        self.add_labels('codegen')
        self.add_labels('avro')
