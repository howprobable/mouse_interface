from setuptools import setup, find_packages

setup(
    name='mouse_interface',
    version='1.0.0',
    packages=find_packages(),
    description='Interface for interactions with the users mouse',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jannik Eggert',
    author_email='eggertjannik@gmail.com',
    url='https://github.com/howprobable/mouse_interface',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)