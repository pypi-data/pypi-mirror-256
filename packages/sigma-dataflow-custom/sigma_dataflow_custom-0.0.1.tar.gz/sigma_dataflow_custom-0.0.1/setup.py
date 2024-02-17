import setuptools

REQUIRED_PACKAGES = [
    "google-cloud-storage==2.14.0",
    "apache_beam[gcp]==2.48.0"
]

setuptools.setup(
    name="sigma_dataflow_custom",
    version="0.0.1",
    author="sigma",
    author_email="",
    install_requires=REQUIRED_PACKAGES,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)