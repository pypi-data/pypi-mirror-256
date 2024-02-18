from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='windoweasy',
  version='0.0.1',
  author='INTERJL',
  author_email='arapov.makar.real@gmail.com',
  description='windoweasy is a simple and user-friendly library built on top of Pygame, providing easy window creation and basic drawing functions for game development and graphical applications',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://pypi.org/user/INTERJL/',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='window screen games game ',
  project_urls={
    'GitHub': 'https://github.com/INTERJL'
  },
  python_requires='>=3.6'
)