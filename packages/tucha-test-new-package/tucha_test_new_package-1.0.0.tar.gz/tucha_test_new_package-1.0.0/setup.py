from setuptools import setup, find_packages

setup(
    name='tucha_test_new_package',
    version='1.0.0',
    author='Tucha',
    author_email='beztfake@yandex.ru',
    description='Test tucha package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maloi56/tucha_test_new_package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ]
)
