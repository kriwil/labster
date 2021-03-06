import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='labster',
    version='0.1.1',
    packages=['labster'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Labster utils',
    long_description=README,
    url='http://www.labster.com/',
    author='Labster',
    author_email='developer@labster.com',
    install_requires=[
        'django-cors-headers==0.12',
        'django-live-profiler==0.0.9',
        'django-widget-tweaks==1.3',
        'html2text==2014.7.3',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
