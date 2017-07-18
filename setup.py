import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='precessor',
        version='0.1.0',
        url='https://github.com/valohai/precessor',
        author='Aarni Koskela',
        author_email='akx@iki.fi',
        maintainer='Aarni Koskela',
        maintainer_email='akx@iki.fi',
        license='MIT',
        install_requires=['requests', 'Pillow', 'pylibmc'],
        extras_require={'dev': ['pytest', 'pytest-cov', 'pytest-xdist', 'requests-mock']},
        packages=['precessor', 'precessor.ops'],
        include_package_data=True,
    )
