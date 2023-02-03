import os.path
import uuid

import flask
from werkzeug.utils import secure_filename

from .models import *
from .utils import *


def drop_error(desc):
    return {
        "result": "ERROR",
        "description": desc
    }


def drop_success(desc, data=None):
    return {
        "result": "SUCCESS",
        "description": desc,
        "data": data if data is not None else ""
    }


def get_releases():
    return Releases.query.all()


def get_artists():
    return Artists.query.all()


def get_platforms():
    return Platforms.query.all()


def get_release_by_id(release_id=None):
    if release_id is None:
        return release_id
    return Releases.query.filter_by(release_id=release_id).first()


def get_artist_by_id(artist_id=None):
    if artist_id is None:
        return artist_id
    return Artists.query.filter_by(artist_id=artist_id).first()


def get_platform_by_id(platform_id=None):
    if platform_id is None:
        return platform_id
    return Platforms.query.filter_by(platform_id=platform_id).first()


def get_temp_new_release():
    return {
        "name": "Новый релиз",
        "cover_url": "/static/images/default/Release.png",
        "release_id": "NEW",
        "path": generate_string(),
        "release_time": time_now(False, True),
    }


def get_temp_new_artist():
    return {
        "name": "Новый артист",
        "avatar_url": "/static/images/default/Artist.png",
        "artist_id": "NEW",
        "profile_name": generate_string(8)
    }


def get_temp_new_platform():
    return {
        "name": "Новая площадка",
        "icon_url": "/static/images/default/Platform.png",
        "platform_id": "NEW"
    }


def get_release_authors_by_id(release_id=None):
    authors = []
    if release_id is None:
        return authors
    releases = ReleaseArtists.query.filter_by(release_id=release_id, type="AUTHOR").all()
    for release in releases:
        artist_id = release.artist_id
        artist = Artists.query.filter_by(artist_id=artist_id).first()
        if artist is not None:
            authors.append(artist)
    return authors


def get_release_feats_by_id(release_id=None):
    feats = []
    if release_id is None:
        return feats
    releases = ReleaseArtists.query.filter_by(release_id=release_id, type="FEAT").all()
    for release in releases:
        artist_id = release.artist_id
        artist = Artists.query.filter_by(artist_id=artist_id).first()
        if artist is not None:
            feats.append(artist)
    return feats


def get_release_by_path(path=None):
    if path is None:
        return path
    return Releases.query.filter_by(path=path).first()


def get_release_platforms_by_id(release_id=None):
    if release_id is None:
        return release_id
    platforms = []
    release_platforms = ReleasePlatforms.query.filter_by(release_id=release_id).all()
    for release_platform in release_platforms:
        platform = Platforms.query.filter_by(platform_id=release_platform.platform_id).first()
        if platform is not None:
            platforms.append({
                "name": platform.name,
                "icon": platform.icon_url,
                "url": release_platform.url,
                "button_text": release_platform.button_text
            })
    return platforms


def get_platforms_with_release_urls(release_id=None):
    if release_id is None:
        return release_id
    platforms = []
    all_platforms = get_platforms()
    for platform in all_platforms:
        release_platform = ReleasePlatforms.query.filter_by(
            release_id=release_id,
            platform_id=platform.platform_id).first()
        platforms.append({
            "name": platform.name,
            "icon": platform.icon_url,
            "url": release_platform.url if release_platform is not None else "",
            "button_text": release_platform.url if release_platform is not None else "Перейти",
        })
    return platforms


def get_release_formatted_artists_by_id(release_id=None):
    if release_id is None:
        return release_id
    authors = get_release_authors_by_id(release_id)
    feats = get_release_feats_by_id(release_id)
    result = ""
    if len(authors) == 0:
        return result
    result += authors[0].name
    for i in range(1, len(authors)):
        result += f", {authors[i].name}"
    if len(feats) == 0:
        return result
    result = " feat."
    result += feats[0].name
    for i in range(1, len(feats)):
        result += f", {feats[i].name}"
    return result


def get_artists_in_release_select_element(release_id=None):
    if release_id is None:
        return release_id
    artists = get_artists()

    # release_authors = get_release_authors_by_id(release_id)
    # release_feats = get_release_feats_by_id(release_id)
    #
    # artists_names = []
    # artists_id = []
    # for arist in artists:
    #     artists_id.append(arist.artist_id)
    #     artists_names.append(arist.name)
    #
    # for release_list in [release_authors, release_feats]:
    #     for artist in release_list:
    #         if artist.artist_id in artists_id:
    #             index = artists_id.index(artist.artist_id)
    #             artists_id.pop(index)
    #             artists_names.pop(index)

    select = f"<select name='%name%' onchange='on_select_change(this);'><option selected></option>"
    for artist in artists:
        select += f"<option>{artist.name}</option>"
    select += '</select>'

    return select


def get_field_list_from_class(obj):
    return [attr for attr in dir(obj) if attr[:2] + attr[-2:] != '____' and not callable(getattr(obj, attr))]


def convert_to_dict(obj):
    if obj is None:
        return obj
    if isinstance(obj, db.Model):
        return str(obj.__dict__)
    if isinstance(obj, list):
        result = ""
        for el in obj:
            result += str(el.__dict__)
        return result
    return obj


def run_api_function(command_name, args):
    func = globals().get(command_name)
    if func is None:
        return drop_error("Unknown command")
    return convert_to_dict(func(**args))


def create_object(obj_name=None, obj_class=None, **args):
    new_id = str(uuid.uuid4())

    if obj_name is None:
        if "release_id" in args.keys():
            obj_name = "Release"
            obj_class = Releases
            args["release_id"] = new_id
        if "artist_id" in args.keys():
            obj_name = "Artist"
            obj_class = Artists
            args["artist_id"] = new_id
        if "platform_id" in args.keys():
            obj_name = "Platform"
            obj_class = Platforms
            args["platform_id"] = new_id

    if obj_class is None:
        return drop_error("Unknown object type")

    obj = obj_class(new_id, obj_name)
    new_data = {}
    for key in args.keys():
        value = args.get(key)
        if key in obj.__dict__:
            setattr(obj, key, value)
            new_data[key] = value
        elif "platform-" in key and len(value) > 0:
            platform_name = key.replace("platform-", "")
            platform = Platforms.query.filter_by(name=platform_name).first()
            if platform is None:
                continue
            release_platform = ReleasePlatforms.query.filter_by(
                release_id=obj.release_id,
                platform_id=platform.platform_id).first()
            if release_platform is not None:
                if release_platform.url == value:
                    continue
                release_platform.url = value
            else:
                release_platform = ReleasePlatforms(
                    obj.release_id,
                    platform.platform_id,
                    value
                )
                db.session.add(release_platform)
            new_data[key] = value

    db.session.add(obj)
    db.session.commit()
    return drop_success(f"{obj_name} data was created!", new_data)


def create_release():
    pass


def create_artist():
    pass


def create_platform():
    pass


def _proceed_icon_url(args, icon_key):
    picture_static_path = os.path.join("images/user_images", f"{args['photo_name']}.png")
    output_icon_key = os.path.join('/static', picture_static_path)

    if 'photo_url' in args:
        get_picture(args['photo_url'], os.path.join(flask.current_app.static_folder, picture_static_path))

        args[icon_key] = output_icon_key
        return
    if len(flask.request.files) > 0:
        file = flask.request.files['file']

        if file and is_file_allowed(file.filename):
            file.save(os.path.join(flask.current_app.static_folder, picture_static_path))
            args[icon_key] = output_icon_key


def change_data(obj=None, obj_name=None, **args):
    if obj_name is None or obj is None:
        if "release_id" in args:
            obj = Releases.query.filter_by(release_id=args["release_id"]).first()
            obj_name = "Release"
        if "artist_id" in args:
            obj = Artists.query.filter_by(artist_id=args["artist_id"]).first()
            obj_name = "Artist"
        if "platform_id" in args:
            obj = Platforms.query.filter_by(platform_id=args["platform_id"]).first()
            obj_name = "Platform"

    if obj is None:
        return drop_error(f"Unknown {obj_name}")

    if hasattr(obj, "get_icon_picture_key") and "photo_name" in args:
        _proceed_icon_url(args, obj.get_icon_picture_key)

    updated_data = {}
    for key, value in args.items():
        # Обновление платформы
        if key in obj.__dict__ and getattr(obj, key) != value:
            setattr(obj, key, value)
            updated_data[key] = value

        # Обновление всех платформ-релизов
        elif "platform-" in key and len(value) > 0:
            platform_name = key.replace("platform-", "")
            platform = Platforms.query.filter_by(name=platform_name).first()
            if platform is None:
                continue
            release_platform = ReleasePlatforms.query.filter_by(
                release_id=obj.release_id,
                platform_id=platform.platform_id).first()
            if release_platform is not None:
                if release_platform.url == value:
                    continue
                release_platform.url = value
            else:
                release_platform = ReleasePlatforms(
                    obj.release_id,
                    platform.platform_id,
                    value
                )
                db.session.add(release_platform)
            updated_data[key] = value

    if len(updated_data) > 0:
        if "last_edit_date" in obj.__dict__:
            obj.last_edit_date = time_now()
        db.session.commit()
        return drop_success(f"{obj_name} data was updated!", updated_data)

    return drop_success("No changes have occurred", updated_data)


def change_release_data(release_id=None, **args):
    return change_data(Releases.query.filter_by(release_id=release_id), "Release", **args)


def change_artist_data(artist_id=None, **args):
    return change_data(Artists.query.filter_by(artist_id=artist_id), "Artist", **args)


def change_platform_data(platform_id=None, **args):
    return change_data(Platforms.query.filter_by(platform_id=platform_id), "Platform", **args)


def get_artist_by_profile_name(profile_name):
    return Artists.query.filter_by(profile_name=profile_name).first()
