from setuptools import setup

setup(
    name='single-file-sync',
    version='1.0',
    description='A simple tool to automatically download a single file and merge private changes.',
    author='kuwii',
    url='https://github.com/kuwii/single-file-sync',
    license='MIT',
    packages=['single_file_sync'],
    install_requires=[
        'PyYAML>=6.0',
        'requests>=2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'sfsync=single_file_sync.sfsync:sfsync'
        ]
    }
)
