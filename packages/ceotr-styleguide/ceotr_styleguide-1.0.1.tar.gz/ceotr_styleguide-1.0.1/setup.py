from setuptools import setup, find_packages

setup(name='ceotr_styleguide',
      version='1.0.1',
      description="CEOTR styleguide",
      author="CEOTR",
      author_email="support@ceotr.ca",
      url="https://gitlab.oceantrack.org/ceotr/styleguide.git",
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=True
      )
