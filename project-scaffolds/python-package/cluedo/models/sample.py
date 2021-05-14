from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence

from cluedo.www import db

class Sample(db.Model):
    __tablename__ = 'sample'
    id = Column(Integer, Sequence('article_id_seq'), primary_key=True)
    name = Column(String(256))

    def __repr__(self):
        return "<Sample(name={0})>".format(
            self.name
        )

def get_all(session):
    samples = []
    for row in session.query(Sample).all():
        samples.append(row.name)
    return samples