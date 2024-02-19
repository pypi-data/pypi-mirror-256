from setuptools import setup, find_packages

print(find_packages(exclude=["test*", "test_*", "*_test*"]))

setup(
    name='zaber_motion_bindings_darwin',
    version='5.1.1',
    packages=find_packages(exclude=["test*", "test_*", "*_test*"]),
    package_data={
        '': ['*.dylib']
    },
    description='Mac OS bindings for Zaber Motion Library',
    long_description='Mac OS bindings for Zaber Motion Library',
    url='https://gitlab.com/ZaberTech/zaber-motion-lib',
    author='Zaber Technologies Inc.',
    author_email='contact@zaber.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='',
    install_requires=[],
    extras_require={'build':['invoke']}
)
