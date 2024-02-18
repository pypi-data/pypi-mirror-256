from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='econometrics01',
  version='1.0.1',
  author='fertic',
  author_email='foxmine852@gmail.com',
  description='This is the simplest modufwle for work with files. v2',
  long_description=readme(),
  long_description_content_type='text/markdown',
  # url='your_url',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  # project_urls={св
  #   'GitHub': 'your_github'
  # },
  # python_requires='>=3.6'
)