from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lokoguard_crashlytic',
    packages=find_packages(),
    version='1.0.0',
    description='This library is to send logs of application to lokoguard crashlytics service',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lokoguard',
    author_email='lokogaurd@gmail.com',
    license='MIT',
    url="https://github.com/lokoguard/lokoguard-crashlytics-python",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='software development crashlytics',
    python_requires='>=3.10',
    install_requires=[
        'requests'
    ],
)