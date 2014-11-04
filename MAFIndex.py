from MAF import MAF;
from os import mkdir;
from whoosh.fields import Schema, STORED, TEXT;
from whoosh.index import create_in, EmptyIndexError, open_dir;

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

  def add(self, filename):
    if (self.writer is None):
      self.writer = self.index.writer();

    fd = MAF(filename);
    self.writer.add_document(id=fd.filename, url=fd.url, date=fd.date, title=unicode(fd.title), content=unicode(fd.read_index(), fd.charset));
    fd.close();

  def commit(self):
    if (self.writer is not None):
      self.writer.commit();
      self.writer = None;
