from setuptools import setup

setup(name='DSSE',
      version='0.1.14',
      description='An environment to train drones to search and find a shipwrecked person lost in the ocean using reinforcement learning.',
      url='https://github.com/pfeinsper/drone-swarm-search',
      license='MIT',
      packages=['DSSE'],
      install_requires=[
          'numpy',
          'gymnasium',
          'pygame',
          'pettingzoo',
          'matplotlib',
      ],
      zip_safe=False)
