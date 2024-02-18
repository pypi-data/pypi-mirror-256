from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='distprop',
    version='0.1.0',
    author='Felix Petersen',
    author_email='ads0800@felix-petersen.de',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Felix-Petersen/distprop',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir={'distprop': 'distprop'},
    packages=['distprop'],
    python_requires='>=3.6',
    install_requires=[
        'torch>=1.6.0',
        'numpy',
    ],
)
