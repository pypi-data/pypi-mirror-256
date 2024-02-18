from setuptools import setup
import versioneer

print(versioneer.get_version())

setup(version=versioneer.get_version(), cmdclass=versioneer.get_cmdclass())
