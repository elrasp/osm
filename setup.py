from setuptools import setup

setup(
    name='osm',
    version='1.0.0.0',
    packages=['osm', 'osm.data_streams', 'osm.data_streams.oracle', 'osm.data_streams.windows',
              'osm.data_streams.windows.forgetting_strategy', 'osm.data_streams.algorithm',
              'osm.data_streams.evaluation', 'osm.data_streams.evaluation.strategy', 'osm.data_streams.active_learner',
              'osm.data_streams.active_learner.measures', 'osm.data_streams.active_learner.strategy',
              'osm.data_streams.active_learner.strategy.pool_based', 'osm.transformers', 'snippets'],
    url='',
    license='MIT License',
    author='elson',
    author_email='elson.serrao@ovgu.de',
    description='Opinion Stream Mining'
)
