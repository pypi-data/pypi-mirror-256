from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='lineoaxpnck',
    version='0.1',
    description='lineoa pnck lnw',
    long_description=readme(),
    url='https://github.com/avfreex24',
    author='PNCKDEVAPP',
    author_email='pnckdevapps@gmail.com',
    license='PNCKDEVAPP',
    install_requires=[
        'requests',
        'opencv-python',
    ],
   # scripts=['bin/'],
    keywords='line oa',
    packages=['pnckdevapp'],
    package_dir={'pnckdevapp': 'bin'},
    package_data={'pnckdevapp': ['bin/*.py']
    },
)