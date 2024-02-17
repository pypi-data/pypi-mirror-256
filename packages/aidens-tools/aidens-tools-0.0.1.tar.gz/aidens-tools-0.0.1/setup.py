from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Topic :: Utilities'
]
 
setup(
  name='aidens-tools',
  version='0.0.1',
  description='A collection of useful Python functions.',
  long_description='A basic library filled with some useful functions that are tedious to make normally in Python without functions.',
  url='',  
  author='Aiden Fliss',
  author_email='aiden.fliss@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='tools', 
  packages=find_packages(),
  install_requires=['pyttsx3','requests'] 
)