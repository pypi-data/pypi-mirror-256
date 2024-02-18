from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='DB-AAE',
    version='0.0.1',
    description='Adversarial Autoencoder with dynamic batching package',
    author='kyung dae ko',
    author_email='gogoaja70@hotmail.com',
    url='https://github.com/LMSCGR/DB-AAE',
    install_requires=required,
    packages=find_packages(exclude=[]),
    keywords=['DB-AAE', 'Adversarial Autoencoder', 'python single cell', 'scRNA-seq', 'pypi'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    
)