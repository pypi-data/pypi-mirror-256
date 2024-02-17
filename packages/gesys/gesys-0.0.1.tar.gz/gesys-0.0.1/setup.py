from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
  name='gesys',
  version='0.0.1',
  author='Gesys',
  author_email='a.letyagin1@gmail.com',
  description='Control your computer with gestures',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/ArtemLetyagin/PDFViewer',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='gesys ',
  project_urls={
    'GitHub': 'https://github.com/ArtemLetyagin/PDFViewer'
  },
  python_requires='>=3.6'
)