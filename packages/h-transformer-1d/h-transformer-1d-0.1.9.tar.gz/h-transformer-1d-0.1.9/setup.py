from setuptools import setup, find_packages

setup(
  name = 'h-transformer-1d',
  packages = find_packages(),
  version = '0.1.9',
  license='MIT',
  description = 'H-Transformer 1D - Pytorch',
  long_description_content_type = 'text/markdown',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/h-transformer-1d',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'efficient attention'
  ],
  install_requires=[
    'einops>=0.3',
    'rotary-embedding-torch>=0.5.3',
    'torch>=1.6'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
