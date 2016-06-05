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
    def register_options(cls, register):
        logger.info("AvrohuggerGenTask: register_options")
        super(AvrohuggerGenTask, cls).register_options(register)

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
        #classpath = self.dist.find_libs(['avrohugger-tools.jar'])
        #logger.info("AvrohuggerGenTask: classpath is %s", classpath)
        #java_main = 'com.sun.tools.internal.xjc.Driver'
        #return self.runjava(classpath=classpath, main=java_main, args=args, workunit_name='avrohugger-tools')
        _args = ['/usr/bin/java','-jar','/Users/msfrank/src/fathom/avrohugger-tools_2.11-0.10.1-assembly.jar'] + args
        logger.info("AvrohuggerGenTask: invoking %s", _args)
        try:
            exitstatus = subprocess.call(_args)
            logger.info("avrohugger process returns %i", exitstatus)
        except Exception, e:
            logger.error("avrohugger subprocess failed: %s", str(e))
            exitstatus = 1
        return exitstatus

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

        for source in target.sources_relative_to_buildroot():
            #output_package = target.package
            #if output_package is None:
            #    raise TaskError('No output package specified')

            args = ['generate', 'schema', source, target_workdir]
            result = self._compile_schema(args)

            if result != 0:
                raise TaskError('avrohugger-tools ... exited non-zero ({code})'.format(code=result))

    @property
    def _copy_target_attributes(self):
        """
        Propagate the provides attribute to the synthetic java_library() target for publishing.
        """
        return ['provides']
