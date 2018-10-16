import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
path = 'sqlite:///iotbroker.db'

class AccountEntity(Base):
    __tablename__ = 'accountentity'
    id =            Column(Integer, primary_key=True)
    protocol =      Column(Integer, nullable=False)
    username =      Column(String(250), nullable=False)
    password =      Column(String(250), nullable=False)
    clientID =      Column(String(250), nullable=False)
    serverHost =    Column(String(250), nullable=False)
    port =          Column(Integer, nullable=False)
    cleanSession =  Column(Boolean, unique=False)
    keepAlive =     Column(Integer, nullable=False)
    will =          Column(String(250), nullable=False)
    willTopic =     Column(String(250), nullable=False)
    isRetain =      Column(Boolean, unique=False)
    qos =           Column(Integer, nullable=False)
    isDefault =     Column(Boolean, unique=False)

class TopicEntity(Base):
    __tablename__ = 'topicentity'
    id =                Column(Integer, primary_key=True)
    topicName =         Column(String(250), nullable=False)
    qos =               Column(Integer, nullable=False)
    accountentity_id =  Column(Integer, ForeignKey('accountentity.id'))
    accountentity = relationship(AccountEntity)

class MessageEntity(Base):
    __tablename__ = 'messageentity'
    id =        Column(Integer, primary_key=True)
    content =   Column(LargeBinary)
    qos =       Column(Integer, nullable=False)
    topicName = Column(String(250), nullable=False)
    incoming =  Column(Boolean, unique=False)
    isRetain =  Column(Boolean, unique=False)
    isDub =     Column(Boolean, unique=False)
    accountentity_id = Column(Integer, ForeignKey('accountentity.id'))
    accountentity = relationship(AccountEntity)

class datamanager():
    def __init__(self):
        self.path = 'sqlite:///iotbroker.db'

    def create_db(self):
        engine = create_engine(self.path)
        try:
            Base.metadata.create_all(engine)
        except OperationalError:
            print('DB already exist')

    def add_entity(self,newrecord):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(newrecord)
        session.commit()
        session.close()

    def update_message(self, id, content):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(MessageEntity).filter(MessageEntity.id==id).update({"content": content})
        session.commit()

    def delete_account(self,clientID):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(AccountEntity).filter(AccountEntity.clientID==clientID).delete()
        session.commit()
        session.close()

    def delete_topic(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(TopicEntity).filter(TopicEntity.id==id).delete()
        session.commit()
        session.close()

    def delete_topic_name(self,name):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(TopicEntity).filter(TopicEntity.topicName==name).delete()
        session.commit()
        session.close()

    def delete_message(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(MessageEntity).filter(MessageEntity.id==id).delete()
        session.commit()
        session.close()

    def delete_message_nameTopic(self,name):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(MessageEntity).filter(MessageEntity.topicName==name).delete()
        session.commit()
        session.close()

    def get_account(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(AccountEntity).filter(AccountEntity.id==id).first()
        return result

    def get_default_account_clientID(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(AccountEntity).filter(AccountEntity.isDefault == True and AccountEntity.clientID == id).first()
        return result

    def get_account_clientID(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(AccountEntity).filter(AccountEntity.clientID == id).first()
        return result

    def get_default_account(self):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(AccountEntity).filter(
            AccountEntity.isDefault == True).first()
        return result

    def uncheck_default_account_clientID(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(AccountEntity).filter(AccountEntity.isDefault == True and AccountEntity.clientID == id).update({"isDefault": False})
        session.commit()
        session.close()

    def set_default_account_clientID(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(AccountEntity).filter(AccountEntity.clientID == id).update({"isDefault": True})
        session.query(AccountEntity).filter(AccountEntity.clientID != id).update({"isDefault": False})
        session.commit()
        session.close()

    def clear_default_account(self):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(AccountEntity).filter(AccountEntity.clientID != '').update({"isDefault": False})
        session.commit()
        session.close()

    def get_topic(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(TopicEntity).filter(TopicEntity.id==id).first()
        return result

    def get_message(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(MessageEntity).filter(MessageEntity.id==id).first()
        return result

    def get_accounts_all(self):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(AccountEntity).all()
        return result

    def get_topics_all_accountID(self,id):
        engine = create_engine(path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(TopicEntity).filter( TopicEntity.accountentity_id == id).all()
        return result

    def get_topic_by_name(self,name):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(TopicEntity).filter( TopicEntity.topicName == name).first()
        return result

    def get_messages_all_accountID(self,id):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        result = session.query(MessageEntity).filter(MessageEntity.accountentity_id == id).all()
        return result

    def clear(self):
        engine = create_engine(self.path)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(AccountEntity).update({"isDefault": False})
        session.query(TopicEntity).delete()
        session.query(MessageEntity).delete()
        session.commit()
        session.close()