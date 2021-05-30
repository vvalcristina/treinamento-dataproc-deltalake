from setuptools import setup

setup(
    name='treinamento-dataproc-deltalke',
    version='0.0.1',
    author='Valeria Silva',
    author_email='silvvaleria@gmail.com',
    packages=['jobs'],
    namespace_packages=['jobs'],
    install_requires=open('requirements.txt').readlines(),
    zip_safe=False
)
