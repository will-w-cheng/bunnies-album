from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://newjeans_user:password@localhost/newjeans_albums'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Album Model
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    total_tracks = db.Column(db.Integer, nullable=False)

    def __init__(self, title, release_date, total_tracks):
        self.title = title
        self.release_date = release_date
        self.total_tracks = total_tracks

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.isoformat(),
            'total_tracks': self.total_tracks
        }

# Create an album
@app.route('/album', methods=['POST'])
def add_album():
    data = request.json
    new_album = Album(
        title=data['title'],
        release_date=datetime.strptime(data['release_date'], '%Y-%m-%d').date(),
        total_tracks=data['total_tracks']
    )
    db.session.add(new_album)
    db.session.commit()
    return jsonify(new_album.to_dict()), 201

# Get all albums
@app.route('/albums', methods=['GET'])
def get_albums():
    albums = Album.query.all()
    return jsonify([album.to_dict() for album in albums])

# Get single album
@app.route('/album/<int:id>', methods=['GET'])
def get_album(id):
    album = Album.query.get_or_404(id)
    return jsonify(album.to_dict())

# Update an album
@app.route('/album/<int:id>', methods=['PUT'])
def update_album(id):
    album = Album.query.get_or_404(id)
    data = request.json
    album.title = data.get('title', album.title)
    album.release_date = datetime.strptime(data.get('release_date', album.release_date.isoformat()), '%Y-%m-%d').date()
    album.total_tracks = data.get('total_tracks', album.total_tracks)
    db.session.commit()
    return jsonify(album.to_dict())

# Delete Album
@app.route('/album/<int:id>', methods=['DELETE'])
def delete_album(id):
    album = Album.query.get_or_404(id)
    db.session.delete(album)
    db.session.commit()
    return '', 204

# Run server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)