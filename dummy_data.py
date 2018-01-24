#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import User, Role, UserRoles, Item, Category

engine = create_engine('sqlite:///item_catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base = declarative_base()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Role 1
role1 = (Role(name='admin', label='Administrator'))
role2 = (Role(name='user', label='Basic User'))
session.add(role1)
session.add(role2)
session.commit()

# User 1
user1 = User(public_id='kdla239423dasldfjaldjla', name='Nate', email='najens@gmail.com', picture='https://scontent.fmkc1-1.fna.fbcdn.net/v/t1.0-1/p240x240/22228162_10209924202565056_2038620253250255968_n.jpg?oh=f610fe480ea1ca3474e4fe6efbc45fdc&oe=5AE095A8', roles=[role1, role2])
session.add(user1)
session.commit()

# Category 1
category1 = Category(name='Soccer')
session.add(category1)
session.commit()

# Item 1
item1 = Item(name='Soccer Cleats', description='Awesome cleats', category_id=1)
session.add(item1)
session.commit()
print('Added menu items!')
