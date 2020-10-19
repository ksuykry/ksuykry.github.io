from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    playlist = Playlist.query.get(playlist_id)
    songs_in_playlist = [s.song_id for s in playlist.song]
    songs = Song.query.filter(Song.id.in_(songs_in_playlist)).all()
    return render_template("playlist.html", playlist=playlist, songs=songs)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    form = PlaylistForm()

    if form.validate_on_submit():
        new_playlist = Playlist(
                      name=form.name.data,
                      description=form.description.data,
                      )
        db.session.add(new_playlist)
        db.session.commit()
        return redirect("/playlists")
    else:
        return render_template("new_playlist.html", form=form)


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    song = Song.query.get(song_id)
    playlists_with_song = [p.playlist_id for p in song.playlist]
    playlists = Playlist.query.filter(Playlist.id.in_(playlists_with_song)).all()
    return render_template("song.html",song = song, playlists = playlists)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    form = SongForm()
    if form.validate_on_submit():
        # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
        new_song = Song(
                        title=form.title.data,
                        artist=form.artist.data,
                      )
        db.session.add(new_song)
        db.session.commit()
        return redirect("/songs")
    else:
        return render_template("new_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS
    playlist = Playlist.query.get(playlist_id)
    song = Song.query.all()
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [p.song_id for p in playlist.song]
    form.song.choices = (
    db.session.query(Song.id, Song.title)
          .filter(Song.id.notin_(curr_on_playlist))
          .all())

    if form.validate_on_submit():
        add_song = PlaylistSong(
            song_id = form.song.data,
            playlist_id = playlist_id
        )
        playlist.song.append(add_song)
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")
    return render_template('add_song_to_playlist.html',
                           playlist=playlist,
                           form=form)