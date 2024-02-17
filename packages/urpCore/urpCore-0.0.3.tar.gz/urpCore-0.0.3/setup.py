from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='urpCore',
  version='0.0.3',
  author='Rashing_pro',
  author_email='urpc.official@gmail.com',
  description='Here is nothing. Just nothing',
  long_description="You can find it on GitHub",
  long_description_content_type='text/markdown',
  url='https://github.com/Universal-Rashing-s-Python-Core/urpc',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='urpc python core',
  project_urls={
    'GitHub': 'https://github.com/Universal-Rashing-s-Python-Core/urpc'
  },
  python_requires='>=3.6'
)