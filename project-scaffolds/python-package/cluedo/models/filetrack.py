from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence

from cluedo.www import db

class Filetrack(db.Model):
    __tablename__ = 'filetrack'
    id = Column(Integer, Sequence('filetrack_id_seq'), primary_key=True)
    filename = Column(String(512))

    def __repr__(self):
        return "<Filetrack(filename={0})>".format(
            self.filename
        )

def is_tracked(session, filename):
    query = session.query(Filetrack).filter(Filetrack.filename == filename)
    return len(query.all()) != 0

def mark_tracked(session, filename):
    filetrack = Filetrack(filename=filename)
    session.add(filetrack)
    session.commit()