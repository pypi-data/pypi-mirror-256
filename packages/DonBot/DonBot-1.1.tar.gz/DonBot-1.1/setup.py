from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='DonBot',
    version='1.1',
    author='Juan David Alvis Sanchez',
    author_email='',
    description='Una biblioteca para automatizar pruebas con Selenium, Allure y Behave con python',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    # use the URL to the github repo
    url='https://github.com/jdas7/DonBot',
    download_url='https://github.com/jdas7/DonBot/tree/1.1',
    keywords=['testing', 'logging', 'example'],
    classifiers=[],
    license='MIT',
    include_package_data=True
)
