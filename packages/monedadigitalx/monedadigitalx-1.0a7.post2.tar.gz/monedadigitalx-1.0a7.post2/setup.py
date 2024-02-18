from setuptools import setup, find_packages


version = '1.0a7r2'

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="monedadigitalx",
    version=version,

    author="federico123579",
    author_email="federico123579@gmail.com",

    url="https://github.com/AmadoRamos/XTBApi.git",
    download_url=f"https://github.com/AmadoRamos/XTBApi/archive/refs/tags/v{version}.zip",

    description="A python based API for XTB trading using websocket_client.",

    packages=['XTBApi'],
    install_requires=['requests', 'websocket-client'],

    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True, # for MANIFEST.in
    python_requires='>=3.6.0',

    package_data={package: ["py.typed", "*.pyi", "**/*.pyi"] for package in find_packages()},
    zip_safe=False,
)