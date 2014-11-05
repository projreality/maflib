from MAF import MAF;
from os import listdir, mkdir;
from os.path import join;
from whoosh.fields import Schema, STORED, TEXT;
from whoosh.index import create_in, EmptyIndexError, open_dir;
from whoosh.qparser import QueryParser;

class MAFIndex:

  def __init__(self, path):
    schema = Schema(id=STORED, url=STORED, date=STORED, title=TEXT(stored=True), content=TEXT);
    try:
      self.index = open_dir(path);
    except IOError:
      mkdir(path);
      self.index = create_in(path, schema);
    except EmptyIndexError:
      self.index = create_in(path, schema);

    self.writer = None;
    self.searcher = None;
    self.parser = QueryParser("content", schema=self.index.schema);

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
    self.writer.add_document(id=fd.filename, url=fd.url, date=fd.date, title=unicode(fd.title), content=unicode(fd.read_index(), fd.charset));
    fd.close();

  def add_path(self, path):
    i = 0;
    for filename in listdir(path):
      if (filename[-5:] == ".maff"):
        print(filename);
        try:
          self.add(join(path,filename));
        except:
          pass;
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

  def search(self, query, limit=10):
    if (self.searcher is None):
      self.searcher = self.index.searcher();

    return self.searcher.search(self.parser.parse(unicode(query)), limit=limit);
