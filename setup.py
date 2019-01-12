from setuptools import setup, find_packages

setup(
    name='mpzmq',
    packages=['mpzmq'],
    version='0.1.1',
    license='MIT',
    author='Josh Liburdi @jshlbrd',
    author_email='liburdi.joshua@gmail.com',
    description='minimalist library for building scalable, distributed python applications',
    long_description='This is a minimalist library for building scalable, distributed Python applications using multiprocessing and ZeroMQ (ZMQ). See project homepage for more details.',
    url='https://github.com/jshlbrd/mpzmq',
    keywords=[
        'zmq',
        'pyzmq',
        'mp',
        'multiprocessing',
        'distributed'
    ],
    install_requires=[
        'pyzmq'
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
