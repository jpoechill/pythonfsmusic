from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Artist

engine = create_engine('sqlite:///fsmusic.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
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

# Clean database
# User.__table__.drop()
# Category.__table__.drop()
# Artist.__table__.drop()

# session.rollback()

# Delete Artists
session.query(User).delete()
session.commit()

# Delete Artists
session.query(Artist).delete()
session.commit()

# Delete Categories
session.query(Category).delete()
session.commit()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Add Category
category1 = Category(
    user_id=1,
    name = "Pop",
    shortname = "pop")
session.add(category1)
session.commit()
#
# Add Category
category2 = Category(
    user_id=1,
    name = "Electro",
    shortname = "electro")
session.add(category2)
session.commit()

# Add Category
category3 = Category(
    user_id=1,
    name = "Rap",
    shortname = "rap")
session.add(category3)
session.commit()

# Add Category
category4 = Category(
    user_id=1,
    name = "Rock",
    shortname = "rock")
session.add(category4)
session.commit()


# Add Artist
artist1 = Artist(
    user_id=1,
    name="Taylor Swift",
    image="https://tgm-liveweb-prod.s3.amazonaws.com/assets/article/2016/12/14/taylor_swift_big_announcements_feature.jpg",
    shortname="taylorswift",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category1)
session.add(artist1)
session.commit()

artist2 = Artist(
    user_id=1,
    name="Calvin Harris",
    shortname="calvinharris",
    image="http://www.billboard.com/files/media/calvin-harris-2017-press-billboard-1548.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category2)
session.add(artist2)
session.commit()

artist3 = Artist(
    user_id=1,
    name="SOB x RBE",
    shortname="sobxrbe",
    image="https://lastfm-img2.akamaized.net/i/u/ar0/58d3fdebeea3c36ae05ff4bd3e3d2731.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category3)
session.add(artist3)
session.commit()

artist4 = Artist(
    user_id=1,
    name="Red Hot Chili Peppers",
    shortname="redhotchilipeppers",
    image="http://mushroom.com/wp-content/uploads/2016/06/red-hot-chili-peppers.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category4)
session.add(artist4)
session.commit()


artist4 = Artist(
    user_id=1,
    name="Marshmellow",
    shortname="marshmellow",
    image="http://www.billboard.com/files/media/Marshmello-2016-Bellnjerry-billboard-1548-650-2.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category2)
session.add(artist4)
session.commit()

artist5 = Artist(
    user_id=1,
    name="Dua Lipa",
    shortname="dualipa",
    image="http://www.billboard.com/files/media/Dua-Lipa-bb6-6auwh-beat-2017-billboard-1548.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category1)
session.add(artist5)
session.commit()

artist6 = Artist(
    user_id=1,
    name="Slushii",
    shortname="slushii",
    image="http://cdn.globaldanceelectronic.com/wp-content/uploads/2016/10/Slushii.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category2)
session.add(artist6)
session.commit()

artist7 = Artist(
    user_id=1,
    name="Kamaiyah",
    shortname="kamaiyah",
    image="http://thefader-res.cloudinary.com/images/w_1440,c_limit,f_auto,q_auto:best/_KS__5544_qbynss/kamaiyah.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category3)
session.add(artist7)
session.commit()

artist8 = Artist(
    user_id=1,
    name="G Eazy",
    shortname="kamaiyah",
    image="http://www.billboard.com/files/media/g-eazy-endless-summer-tour-2016-billboard-1548.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category3)
session.add(artist8)
session.commit()

artist9 = Artist(
    user_id=1,
    name="Bruno Mars",
    shortname="brunomars",
    image="http://brunomars.us/wp-content/uploads/2015/01/Bruno-Mars-Lifestyle.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category1)
session.add(artist9)
session.commit()

artist10 = Artist(
    user_id=1,
    name="Cold Play",
    shortname="coldplay",
    image="http://www.kiss925.com/wp-content/blogs.dir/7/files/2015/11/Coldplay.png",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category4)
session.add(artist7)
session.commit()

artist11 = Artist(
    user_id=1,
    name="Twenty One Pilots",
    shortname="twentyonepilots",
    image="http://www.upsetmagazine.com/wp-content/uploads/2015/05/Twenty-One-Pilots_May-2015_Upset_SLB_006.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category4)
session.add(artist11)
session.commit()

artist12 = Artist(
    user_id=1,
    name="Linkin Park",
    shortname="linkinpark",
    image="http://img.wennermedia.com/featured-promo-724/linkin-park-statement-chester-bennington-death-e8ece413-5051-4107-b55a-c6fc511bf9d0.jpg",
    description="Juicy grilled veggie patty with tomato mayo and lettuce",
    category=category4)
session.add(artist12)
session.commit()


# Read
# obj =  session.query(Category).all()

# for x in obj:
#     print x

# session.commit()

# theCategory = "Pop"
#
# allCategories =  session.query(Category).all()
# for category in allCategories:
#     print category.name
#     # if theCategory == artist.category.name:
#     #     print artist.name
#
# allArtists =  session.query(Artist).all()
#
# for artist in allArtists:
#     if theCategory == artist.category.name:
#         print artist.name

# Delete
# session.query(Category).delete()

# print "added menu items!"
