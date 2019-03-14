from setuptools import find_packages, setup;

fd = open("README");
long_description = fd.read();
fd.close();

setup(name              = "maflib",
      version           = "1.0.0",
      packages          = find_packages(),
      author            = "Samuel Li",
      author_email      = "sam@projreality.com",
      url               = "http://www.projreality.com/maflib",
      description       = "Library for read, manipulating, and indexing Mozilla Archive Format (MAF) files",
      long_description  = long_description,
      license           = "https://www.gnu.org/licenses/lgpl.html"
     );