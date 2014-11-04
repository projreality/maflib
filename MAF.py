from dateutil import parser;
import xml.etree.ElementTree as et;
import zipfile;

class MAF:

  namespace = "{http://maf.mozdev.org/metadata/rdf#}";

  def __init__(self, filename):
    self.fd = zipfile.ZipFile(filename);
    fdi = self.fd.open("index.rdf", mode="r");
    root = et.fromstring(fdi.read().replace("&","&amp;"));
    fdi.close();
    rdfns = root.tag[:-3];
    descr = root.find(rdfns + "Description");
    self.url = descr.find(self.namespace + "originalurl").attrib[rdfns + "resource"];
    self.title = descr.find(self.namespace + "title").attrib[rdfns + "resource"];
    self.date = parser.parse(descr.find(self.namespace + "archivetime").attrib[rdfns + "resource"]);
    self.index = descr.find(self.namespace + "indexfilename").attrib[rdfns + "resource"];
    self.charset = descr.find(self.namespace + "charset").attrib[rdfns + "resource"];

  def __del__(self):
    self.fd.close();

  def filelist(self):
    files = [ x.orig_filename for x in self.fd.filelist ];
    try:
      files.remove("index.dat");
    except ValueError:
      pass;
    try:
      files.remove("index.rdf");
    except ValueError:
      pass;
    return files;
