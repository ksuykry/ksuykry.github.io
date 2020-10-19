"""Forms for playlist app."""

from wtforms import SelectField
from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import InputRequired


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    # Add the necessary code to use this form
    name = StringField("Playlist Name",[InputRequired()])
    description = StringField("Description")


class SongForm(FlaskForm):
    """Form for adding songs."""

    # Add the necessary code to use this form
    title = StringField("Song Title",[InputRequired()])
    artist = StringField("Artist",[InputRequired()])

# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
