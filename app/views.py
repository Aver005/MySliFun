from flask import render_template, request, redirect
from app import app
from . import api


@app.route("/artist/<string:profile_name>")
@app.route("/profile/<string:profile_name>/")
def page_artist_profile(profile_name):
    artist = api.get_artist_by_profile_name(profile_name)
    if artist is None:
        return redirect("/404")
    return render_template("pages/artist_profile.html", artist=artist)


@app.route("/admin")
@app.route("/admin/")
def page_admin_index():
    return render_template("pages/admin/index.html")


@app.route("/admin/<string:path>")
@app.route("/admin/<string:path>/")
def page_admin_object(path):

    if path == "releases":
        releases = api.get_releases()
        return render_template("pages/admin/releases.html", releases=releases)
    elif path == "artists":
        artists = api.get_artists()
        return render_template("pages/admin/artists.html", artists=artists)
    elif path == "platforms":
        platforms = api.get_platforms()
        return render_template("pages/admin/platforms.html", platforms=platforms)

    if "id" in request.values:
        object_id = request.values["id"]
        if path == "release":
            data = {
                "artists": api.get_artists(),
                "platforms": api.get_platforms_with_release_urls(object_id),
                "release": api.get_release_by_id(object_id),
                "authors": api.get_release_authors_by_id(object_id),
                "feats": api.get_release_feats_by_id(object_id)
            }
            return render_template("pages/admin/release.html", **data)
        elif path == "artist":
            return render_template("pages/admin/artist.html",
                                   artist=api.get_artist_by_id(object_id))
        elif path == "platform":
            return render_template("pages/admin/platform.html",
                                   platform=api.get_platform_by_id(object_id))

    return redirect("/404?back=/admin")


@app.route("/admin/<string:path>/new", methods=["GET", "POST"])
@app.route("/admin/<string:path>/add", methods=["GET", "POST"])
@app.route("/admin/new/<string:path>", methods=["GET", "POST"])
@app.route("/admin/add/<string:path>", methods=["GET", "POST"])
def page_admin_add_platform(path):
    if path == "release":
        return render_template("pages/admin/release.html",
                               release=api.get_temp_new_release(),
                               artists=api.get_artists(),
                               platforms=api.get_platforms())
    elif path == "platform":
        return render_template("pages/admin/platform.html",
                               platform=api.get_temp_new_platform())
    elif path == "artist":
        return render_template("pages/admin/artist.html",
                               artist=api.get_temp_new_artist())
    return redirect("/404?back=/admin")


@app.route("/<string:path>")
def page_release_links(path):
    release = api.get_release_by_path(path)
    if release is None:
        return redirect("/404?back=/admin")
    return render_template("pages/release_links.html",
                           release=release,
                           platforms=api.get_release_platforms_by_id(release.release_id),
                           artists=api.get_release_formatted_artists_by_id(release.release_id))


@app.route("/api/<string:command>", methods=["GET", "POST"])
def page_api(command):
    if "redirect" in request.values:
        api.run_api_function(command, request.values)
        return redirect(request.values["redirect"])
    return api.run_api_function(command, request.values)


@app.route("/404")
def page_404_error():
    name = "Ошибка 404: Страница не найдена"
    description = "Кажется, вы что-то перепутали..."
    back_url = request.values["back"] if "back" in request.values else "/"

    if "name" in request.values:
        name = request.values["name"]
    if "description" in request.values:
        description = request.values["description"]

    return render_template("pages/error/404.html",
                           name=name,
                           description=description,
                           back_url=back_url)
