from setuptools import setup, find_packages

setup(
    name='minimal_project',
    version='0.1.1',
    packages=find_packages(),
    author='Chandra Prakash',
    author_email='chandra.pr.158@gmail.com',
    description='A minimal Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Chandra158/minimal-project',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
