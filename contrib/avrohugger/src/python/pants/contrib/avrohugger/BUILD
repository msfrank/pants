contrib_plugin(
    name='plugin',
    dependencies=[
        'contrib/avrohugger/src/python/pants/contrib/avrohugger',
        'src/python/pants/build_graph',
        'src/python/pants/goal:task_registrar',
    ],
    distribution_name='pantsbuild.pants.contrib.avrohugger',
    description='AvroHugger avro -> scala generator pants plugin.',
    additional_classifiers=[
        'Topic :: Software Development :: Code Generators'
    ],
    build_file_aliases=True,
    register_goals=True,
)
