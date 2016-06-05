from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.task_registrar import TaskRegistrar as task

from pants.contrib.avrohugger.targets import ScalaAvroLibrary
from pants.contrib.avrohugger.tasks import AvrohuggerGenTask


import logging
logger = logging.getLogger(__name__)


def build_file_aliases():
    logger.info("avrohugger.register: build_file_aliases")
    return BuildFileAliases(
        targets={
            'scala_avro_library': ScalaAvroLibrary,
        }
    )


def register_goals():
    logger.info("avrohugger.register: register_goals")
    task(name='avrohugger', action=AvrohuggerGenTask).install('gen')
