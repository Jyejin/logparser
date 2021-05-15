from setuptools import setup, find_packages

install_requires = [
    'python-dateutil',
    'pytz',
    'urllib3'
]

setup(
    name='logparser',
    version='1.0',
    description='AWS ELB log parser',
    auther='Jyejin',
    url='https://github.com/Jyejin/logparser',
    install_requires=install_requires,
    python_requires='>=3.5',
    packages=['logparser'],
    find_packages=find_packages(exclude=('test',)),
)