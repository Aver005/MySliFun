from sqlalchemy import Column, Integer, Text
from app import db
from .utils import *


class Releases(db.Model):
    id = Column(Integer(), nullable=False, primary_key=True, unique=True)
    release_id = Column(Text(), nullable=False)
    path = Column(Text(), nullable=False, default="", unique=True)
    name = Column(Text(), nullable=False)
    description = Column(Text(), nullable=False, default="")
    type = Column(Text(), nullable=False, default="SINGLE")
    cover_url = Column(Text(), nullable=False, default="/static/images/default/Release.png")
    release_date = Column(Text(), nullable=False, default=time_now())
    create_date = Column(Text(), nullable=False, default=time_now())
    last_edit_date = Column(Text(), nullable=False, default=time_now())
    views = Column(Integer(), nullable=False, default=0)
    streams = Column(Integer(), nullable=False, default=0)
    listeners = Column(Integer(), nullable=False, default=0)

    def __init__(self, release_id, name):
        self.release_id = release_id
        self.name = name

    @property
    def get_icon_picture_key(self):
        """
        :return: Icon key for updating file
        """
        return "cover_url"


class Artists(db.Model):
    id = Column(Integer(), nullable=False, primary_key=True, unique=True)
    artist_id = Column(Text(), nullable=False)
    name = Column(Text(), nullable=False)
    description = Column(Text(), nullable=False, default="")
    profile_name = Column(Text(), nullable=False, default="")
    avatar_url = Column(Text(), nullable=False, default="/static/images/default/Artist.png")
    background_url = Column(Text(), nullable=False, default="https://vk.cc/cfVx4Q")
    views = Column(Integer(), nullable=False, default=0)
    streams = Column(Integer(), nullable=False, default=0)
    listeners = Column(Integer(), nullable=False, default=0)

    def __init__(self, artist_id, name):
        self.artist_id = artist_id
        self.name = name

    @property
    def get_icon_picture_key(self):
        """
        :return: Icon key for updating file
        """
        return "avatar_url"


class Platforms(db.Model):
    id = Column(Integer(), nullable=False, primary_key=True, unique=True)
    platform_id = Column(Text(), nullable=False)
    name = Column(Text(), nullable=False)
    icon_url = Column(Text(), nullable=False, default="/static/images/icon/Default.png")
    url = Column(Text(), nullable=False, default="")

    def __init__(self, platform_id, name):
        self.platform_id = platform_id
        self.name = name

    @property
    def get_icon_picture_key(self):
        """
        :return: Icon key for updating file
        """
        return "icon_url"


class ReleasePlatforms(db.Model):
    id = Column(Integer(), nullable=False, primary_key=True, unique=True)
    release_id = Column(Text(), nullable=False)  # db.ForeignKey("Releases.release_id"),
    platform_id = Column(Text(), nullable=False)  # db.ForeignKey("Platforms.platform_id"),
    url = Column(Text(), nullable=False, default="")
    button_text = Column(Text(), nullable=False, default="Перейти")

    def __init__(self, release_id, platform_id, url):
        self.release_id = release_id
        self.platform_id = platform_id
        self.url = url


class ArtistPlatforms(db.Model):
    id = Column(Integer(), nullable=False, primary_key=True, unique=True)
    artist_id = Column(Text(), nullable=False)  # db.ForeignKey("Artists.artist_id"),
    platform_id = Column(Text(), nullable=False)  # db.ForeignKey("Platforms.platform_id"),
    url = Column(Text(), nullable=False, default="")
    button_text = Column(Text(), nullable=False, default="Перейти")


class ReleaseArtists(db.Model):
    id = Column(Integer(), nullable=False, primary_key=True, unique=True)
    release_id = Column(Text(), nullable=False)  # db.ForeignKey("Releases.release_id"),
    artist_id = Column(Text(), nullable=False)  # db.ForeignKey("Artists.artist_id"),
    type = Column(Text(), nullable=False, default="AUTHOR")
