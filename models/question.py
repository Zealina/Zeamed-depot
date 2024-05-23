#!/usr/bin/env python3
"""Questions Module contains the question class and all related functions"""

from datetime import datetime
from uuid import uuid4
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Boolean, DateTime, ARRAY

Base = declarative_base()


class Question(Base):
    """Class to create questions object"""

    __tablename__ = 'questions'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    question = Column(Text, nullable=False)
    answer = Column(Text)
    options = Column(ARRAY(Text), default=[True, False])
    verified = Column(Boolean, default=False)
    posting = Column(Text)
    pq = Column(Boolean, default=True)
    explanation = Column(Text)
    topic = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
                        DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)


    def __init__(self, question, answer=None, options=None, verified=False,
                 posting=None, pq=True, explanation=None, topic=None,
                 **kwargs) -> None:
        """Initialize the questions class"""
        self.id = str(uuid4())
        self.question = question
        self.__answer = None
        self.options = options if options else [True, False]
        self.answer = answer
        self.posting = posting
        self.topic = topic
        self.pq = pq
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', self.created_at)
        self.explanation = explanation
        self.verified = verified
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def question(self):
        """Getter method"""
        return self.__question

    @question.setter
    def question(self, text):
        """Setter method"""
        if text and type(text) is str:
            self.__question = text
        elif not text:
            raise ValueError("Question must be present")
        else:
            raise ValueError("Question must be a string")

    @property
    def options(self):
        """Getter method"""
        return self.__options

    @options.setter
    def options(self, options):
        """Setter method"""
        if options and isinstance(options, list):
            self.__options = options
        else:
            raise ValueError("Options must be a List")
        if self.answer and self.answer not in options:
            self.answer = None

    @property
    def answer(self):
        """Getter method"""
        return self.__answer

    @answer.setter
    def answer(self, text):
        """Setter method"""
        if self.options:
            if text and text not in self.options:
                raise ValueError("Answer not included in options")
        self.__answer = text

    @property
    def posting(self):
        """Getter method"""
        return self.__posting

    @posting.setter
    def posting(self, text):
        """Setter method"""
        self.__posting = None
        if type(text) is str:
            self.__posting = text

    @property
    def topic(self):
        """Getter method"""
        return self.__topic

    @topic.setter
    def topic(self, text):
        """Setter method"""
        self.__topic = None
        if type(text) is str:
            self.__topic = text

    @property
    def pq(self):
        """Getter method"""
        return self.__pq

    @pq.setter
    def pq(self, value):
        """Setter method"""
        self.__pq = True
        if type(value) is bool:
            self.__pq = value

    @property
    def verified(self):
        """Getter method"""
        return self.__verified

    @verified.setter
    def verified(self, value):
        """Setter method"""
        if type(value) is bool:
            self.__verified = value
        else:
            self.__verified = False

    @property
    def explanation(self):
        """Getter method"""
        return self.__explanation

    @explanation.setter
    def explanation(self, value):
        """Setter method"""
        if type(value) is str:
            self.__explanation = value
        else:
            self.__explanation = None

    def to_dict(self):
        """Convert instance to dictionary"""
        my_dict = {}
        for key, value in self.__dict__.items():
            key = key.replace('_' + self.__class__.__name__ + '__', '')
            if isinstance(value, datetime):
                my_dict[key] = str(value)
            else:
                my_dict[key] = value
        return my_dict

    def update(self, **kwargs) -> None:
        """Update the options of a question"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__updated_at = datetime.now()

    def __repr__(self):
        """String Reprsentation of the instance"""
        return (f"[({self._id}) - ({self.posting}"
                f", {self.topic})] - {self.question}")
