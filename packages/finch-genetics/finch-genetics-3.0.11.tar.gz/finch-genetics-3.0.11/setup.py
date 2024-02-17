from setuptools import setup, find_packages

setup(
    name='finch-genetics',
    version='3.0.11',
    description='The next evolution of evolutionary algorithms.',
    #long_description=str(open('/Users/daniellosey/Desktop/code/Finch/Finch/README.md', "r").read()),
    url='https://github.com/dadukhankevin/Finch',
    packages=find_packages(),
    install_requires=open('/Users/daniellosey/Desktop/code/Finch/Finch/requirements.txt', "r").readlines(),
    # If you have dependencies hosted in a Git repository, you can specify them like this:
    author="Daniel Losey",
    license="MIT",
    include_package_data=True,
)


#pypi-AgEIcHlwaS5vcmcCJDhlMjk4ZTAzLTFlNGQtNDVhOC04ZGIyLTgxOWNmNGE5MTZhZAACFlsxLFsiZmluY2gtZ2VuZXRpY3MiXV0AAixbMixbIjE3ZjdiNzRjLTg0MjItNDAxNi04MDE2LTg0ZjkxNTU4ZTljZiJdXQAABiDKk6SfUFY07Wty-iNAjHYdmJjHE3czOLXb3pLU7zztVg