from setuptools import setup, find_packages



install_requires = [
    "wagtail==2.12",
]


setup(name='ceotr_web_common',
      version='1.0.0',
      description="Common web assets",
      author="CEOTR",
      author_email="support@ceotr.ca",
      url="https://gitlab.oceantrack.org/ceotr/web-common.git",
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True
      )
