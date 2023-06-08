from transcript_api import db
from datetime import datetime

class VideoSummary(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)
    video_id = db.Column(db.String(10), unique = True, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    summary = db.Column(db.Text(), nullable = False) 

    def __repr__(self):
        print(f'VideoSummary({self.id}, {self.video_id}, {self.title})')


class FileSummary(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)
    title = db.Column(db.String(100), nullable = False)
    summary = db.Column(db.Text(), nullable = False)

    def __repr__(self):
        print(f"FileSummary({self.id}, {self.title})")