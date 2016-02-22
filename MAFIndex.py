from MAF import MAF;
from os import listdir, mkdir;
from os.path import join;
from tld import get_tld;
from urlparse import urlsplit;
from whoosh.fields import DATETIME, ID, Schema, TEXT;
from whoosh.index import create_in, EmptyIndexError, open_dir;
from whoosh.qparser import QueryParser;
from whoosh.qparser.dateparse import DateParserPlugin;

class MAFIndex:

  def __init__(self, path):
    schema = Schema(id=STORED, url=ID, fqdn=ID, dn=ID, date=DATETIME, title=TEXT(stored=True), content=TEXT);
    try:
      self.index = open_dir(path);
    except IOError:
      mkdir(path);
      self.index = create_in(path, schema);
    except EmptyIndexError:
      self.index = create_in(path, schema);

    self.writer = None;
    self.searcher = None;
    self.parser = None;
    self.default_field = "content";

  def __del__(self):
    if (self.writer is not None):
      self.writer.cancel();
    if (self.searcher is not None):
      self.searcher.close();
    self.index.close();

  def add(self, filename):
    if (self.writer is None):
      self.writer = self.index.writer();

    fd = MAF(filename);
    url = fd.url;
    fqdn = urlsplit(url).netloc;
    dn = get_tld(url);

    self.writer.add_document(id=unicode(fd.filename, "UTF-8"), url=unicode(url, "UTF-8"), fqdn=unicode(fqdn, "UTF-8"), dn=unicode(dn, "UTF-8"), date=fd.date, title=fd.title, content=unicode(fd.read_index(), "UTF-8"));

    fd.close();

  def add_path(self, path):
    i = 0;
    for filename in listdir(path):
      if (filename[-5:] == ".maff"):
        print(filename);
        self.add(join(path,filename));
        i = i + 1;
        if (i % 1000 == 0):
          self.commit();

  def commit(self):
    if (self.writer is not None):
      self.writer.commit();
      self.writer = None;
      if (self.searcher is not None):
        self.searcher.close();
        self.searcher = None;

  def cancel(self):
    if (self.writer is not None):
      self.writer.cancel();
      self.writer = None;

  def search(self, query, limit=10, default_field=None):
    if (self.searcher is None):
      self.searcher = self.index.searcher();

    if ((self.parser is None) or ((default_field is not None) and (self.default_field != default_field))):
      if (default_field is not None):
        self.default_field = default_field;
      self.parser = QueryParser(default_field, schema=self.index.schema);
      self.parser.add_plugin(DateParserPlugin(free=True));

    return self.searcher.search(self.parser.parse(unicode(query)), limit=limit);
