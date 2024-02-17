from setuptools import setup, find_packages


setup(
    name='plateFinder_Eneda',
    version='1.0.1',
    author='Eneda Zela',
    description='A package to find the plate',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['openpyxl','pandas'],
    keywords=['plateFinder','plate',''],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

