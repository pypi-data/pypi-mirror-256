from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='gesys',
  version='1.1.6',
  author='Gesys',
  author_email='a.letyagin1@gmail.com',
  description='Control your computer with gestures.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/ArtemLetyagin/Gesys',
  packages=find_packages(),
  install_requires=['mediapipe', 'opencv-python', 'onnxruntime', 'pycryptodome'],
  classifiers=[
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='gesture gestures control',
  project_urls={
    'GitHub': 'https://github.com/ArtemLetyagin/Gesys'
  },
  include_package_data=True,
  python_requires='>=3.8'
)