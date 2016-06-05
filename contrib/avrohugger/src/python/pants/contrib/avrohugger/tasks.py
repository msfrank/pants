import subprocess
import logging

from pants.backend.jvm.targets.jar_dependency import JarDependency
from pants.backend.codegen.tasks.simple_codegen_task import SimpleCodegenTask
from pants.backend.jvm.targets.scala_library import ScalaLibrary
from pants.backend.jvm.tasks.nailgun_task import NailgunTask
from pants.base.exceptions import TaskError

from pants.contrib.avrohugger.targets import ScalaAvroLibrary


logger = logging.getLogger(__name__)


class AvrohuggerGenTask(SimpleCodegenTask,NailgunTask):
    """
    """

    @classmethod
    def product_types(cls):
        logger.info("AvrohuggerGenTask: product_types")
        return [ 'scala', ]

    @classmethod
    def register_options(cls, register):
        logger.info("AvrohuggerGenTask: register_options")
        super(AvrohuggerGenTask, cls).register_options(register)
        cls.register_jvm_tool(register, 'avrohugger-codegen', classpath=[
            JarDependency(org='com.julianpeeters', name='avrohugger-tools_2.11', rev='0.10.1'),
        ])

    @property
    def avrohugger_classpath(self):
        return self.tool_classpath('avrohugger-codegen')

    @classmethod
    def prepare(cls, options, round_manager):
        logger.info("AvrohuggerGenTask: prepare")
        super(AvrohuggerGenTask, cls).prepare(options, round_manager)

    def execute(self):
        logger.info("AvrohuggerGenTask: execute")
        super(AvrohuggerGenTask, self).execute()

    def __init__(self, *args, **kwargs):
        """
        :param context: inherited parameter from Task
        :param workdir: inherited parameter from Task
        """
        super(AvrohuggerGenTask, self).__init__(*args, **kwargs)
        self.set_distribution(jdk=True)
        self.gen_langs = set()
        lang = 'scala'
        if self.context.products.isrequired(lang):
            self.gen_langs.add(lang)

    def _compile_schema(self, args):
        """
        """
        logger.info("AvrohuggerGenTask: _compile_schema")
        logger.info("AvrohuggerGenTask: invoking avrohugger-tools with args %s", args)
        result = self.runjava(classpath=self.avrohugger_classpath,
                              main='avrohugger.tool.Main',
                              args=args,
                              workunit_name='avrohugger-tools')
        logger.info("avrohugger-tools returns %i", result)
        if result != 0:
            raise TaskError('avrohugger-tools returns {}'.format(result))
        return result

    def synthetic_target_type(self, target):
        """
        """
        return ScalaLibrary

    def is_gentarget(self, target):
        """
        """
        return isinstance(target, ScalaAvroLibrary)

    def execute_codegen(self, target, target_workdir):
        """
        """
        logger.info("AvrohuggerGenTask: execute_codegen")
        if not isinstance(target, ScalaAvroLibrary):
            raise TaskError('Invalid target type "{class_type}" (expected ScalaAvroLibrary)'
                .format(class_type=type(target).__name__))

        definition_type = target.definition_type
        if definition_type == 'standard':
            operation = 'generate'
        elif definition_type == 'specific':
            operation = 'generate-specific'
        elif definition_type == 'scavro':
            operation = 'generate-scavro'
        else:
            raise TaskError('avrohugger unknown definition_type {}'.format(definition_type))

        for source in target.sources_relative_to_buildroot():
            if source.endswith('.avsc'):
                filetype = 'schema'
            else:
                raise TaskError('avrohugger unknown file type for {}'.format(source))
            args = [operation, filetype, source, target_workdir]
            result = self._compile_schema(args)

            if result != 0:
                raise TaskError('avrohugger-tools ... exited non-zero ({code})'.format(code=result))

    @property
    def _copy_target_attributes(self):
        """
        Propagate the provides attribute to the synthetic java_library() target for publishing.
        """
        return ['provides']
