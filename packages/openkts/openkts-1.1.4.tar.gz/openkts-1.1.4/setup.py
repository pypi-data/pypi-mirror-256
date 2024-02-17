from pathlib import Path
from setuptools import find_packages, setup
import openkts

setup(
  author='Anthony Kruger',
  author_email='devadmin@impression.cloud',
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Information Technology',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'],
  description='Open Keyshare Threshold Scheme',
  install_requires=[''],
  keywords='keyshare',
  license='MIT',
  long_description=(Path(__file__).parent / "README.md").read_text(),
  long_description_content_type='text/markdown',
  name='openkts',
  package_data={'openkts': ['__init__.py', '__main__.py', 'common.py', 'sss.py']},
  packages=find_packages(),
  version=openkts.Version()
)