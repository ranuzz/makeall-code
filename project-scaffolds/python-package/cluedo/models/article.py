from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence

from cluedo.www import db

class Article(db.Model):
    __tablename__ = 'article'
    id = Column(Integer, Sequence('article_id_seq'), primary_key=True)
    hash = Column(String(512))
    title = Column(String(256))
    uri = Column(String(1024))
    content = Column(String(10240))
    region  = Column(String(32))
    topic = Column(String(512))

    def __repr__(self):
        return "<Article(hash={0}, title={1}, uri={2}, region={3}, topic={4}, content={5})>".format(
            self.hash,
            self.title,
            self.uri,
            self.region,
            self.topic,
            self.content[:100]
        )
        
def is_tracked(session, hash):
    query = session.query(Article).filter(Article.hash == hash)
    try:
        return query.first()
    except:
        return None

def get_distinct_topics(session):
    topics = []
    for topic in session.query(Article.topic).distinct():
        topics.append(topic[0])
    return topics
    
def get_all_articles_for_topic(session, topic):
    articles = []
    for row in session.query(Article).filter(Article.topic == topic).all():
        articles.append(row.content)
    return articles