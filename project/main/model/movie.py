from .. import db
import csv


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    cast = db.Column(db.String(100))
    score = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String(100), nullable=False)

    def __init__(self, name, category, cast, score, rank, description, picture, url):
        self.name = name
        self.category = category
        self.cast = cast
        self.score = score
        self.rank = rank
        self.description = description
        self.picture = picture
        self.url = url


def read_movie(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        result = []
        for item in reader:
            if reader.line_num == 1:
                continue
            result.append(item)

    for i in result:
        try:
            movie = Movie(*i)
        except TypeError as e:
            print(e)
        else:
            db.session.add(movie)
        finally:
            db.session.commit()
