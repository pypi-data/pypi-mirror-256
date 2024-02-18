from setuptools import setup, find_packages
setup(
    name='hrsd-django-chunkator',
    version='2.2.1',
    author='Julien Miotte',
    author_email='j.miotte@majerti.fr',
    description='Fake Django Chunkator for POC purposes',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
