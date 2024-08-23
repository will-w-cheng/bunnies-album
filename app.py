from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os 
from flask_migrate import Migrate
import base64

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'album_images')
ALLOWED_EXTENSIONS = {}
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

password = os.getenv("NJ_ALBUM_PASSWORD", "password")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://newjeans_user:{password}@localhost/newjeans_albums"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Album Model
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    total_tracks = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255))  # Local file path for the image
    def __init__(self, title, release_date, total_tracks, image_path):
        self.title = title
        self.release_date = release_date
        self.total_tracks = total_tracks
        self.image_path = image_path    

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.isoformat(),
            'total_tracks': self.total_tracks,
            'image_path': self.image_path,
        }
# def allowed_file(filename):
#     for i in filename.split('.'):
#         if i in ALLOWED_EXTENSIONS:
#             return '.'

# Create an album
@app.route('/album', methods=['POST'])
def add_album():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    print(file.filename)
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)        
        data = request.form
        print(file.__dict__)
        print(data['title'],data['release_date'], int(data['total_tracks']), file_path)

        new_album = Album(
            title=data['title'],
            release_date=datetime.strptime(data['release_date'], '%Y-%m-%d').date(),
            total_tracks=int(data['total_tracks']),
            image_path=file_path
        )
        db.session.add(new_album)
        db.session.commit()
        return jsonify(new_album.to_dict()), 201

    return jsonify(new_album.to_dict()), 201
    
# Get all albums
@app.route('/albums', methods=['GET'])
def get_albums():
    albums = Album.query.all()
    albumDicts = []
    for album in albums:
        with open(album.image_path, 'rb') as image:
            albumDict = album.to_dict()
            albumDict["image_data"] = base64.b64encode(image.read()).decode('utf-8')
            albumDicts.append(albumDict)
    return jsonify(albumDicts)
    

# Get single album
@app.route('/album/<int:id>', methods=['GET'])
def get_album(id):
    album = Album.query.get_or_404(id)
    with open(album.image_path, 'rb') as image:
        albumDict = album.to_dict()
        albumDict["image_data"] = base64.b64encode(image.read()).decode('utf-8')
        return jsonify(albumDict)

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

@app.route('/')
def index():
    return render_template('albums.html')

# Run server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
