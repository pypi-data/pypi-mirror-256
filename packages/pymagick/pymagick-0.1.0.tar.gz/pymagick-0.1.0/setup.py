from setuptools import setup, find_packages

setup(
    name='pymagick',
    version='0.1.0',
    description='A Python module for file "rwe", manipulation, formatting and usage in various formats.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SergioLKG/py-magick',
    author='SergioLKG',
    author_email='sergiodp.dev@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='file manipulation format usage csv json xml',
    packages=find_packages(),
    install_requires=[
        # NO NEED
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
