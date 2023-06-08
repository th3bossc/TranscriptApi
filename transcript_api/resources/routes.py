from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from transcript_api.common.utils import title, summarize_youtube_video, summarize_file, summarize_string
from transcript_api.models import VideoSummary, FileSummary
from transcript_api import db 
import os

resources = Blueprint('resources', __name__)
api = Api(resources) 

class VideoTranscript(Resource):
    def get(self, video_id):
        print(request)
        summaryExist = VideoSummary.query.filter_by(video_id = video_id).first() 
        if summaryExist is not None:
            return {'title' : summaryExist.title, 'summary' : summaryExist.summary}, 200
        

        try:
            video_title = title(video_id)
        except:
            return {'error' : 'Video ID not valid'}, 400
        try:
            summary = summarize_youtube_video('https://www.youtube.com/watch?v=' + video_id, 'transcript_api/common/audio')
            newVideo = VideoSummary(title = video_title, video_id = video_id, summary = summary)
            db.session.add(newVideo)
            db.session.commit()
            return {'title' : video_title, 'summary' : summary}, 200
        except Exception as e:
            return 500
        
    
api.add_resource(VideoTranscript, '/video_api/<string:video_id>')


class FileTranscript(Resource):
    
    def post(self, type):


        if type == 'pdf' or type == 'txt':
            print(request.files)
            file = request.files['file']
            file_location = os.path.join(current_app.config.get('UPLOAD_FOLDER'), file.filename)
            file.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), file.filename))
            summary = summarize_file(file_location = file_location, file_extension = type)
            file_name = file.filename
        elif type == 'direct_text':
            summary = summarize_string(request.json['text'])
            file_name = "Entered Text"
        if summary == "[ERROR]":
            return {'error' : 'We are expreriencing some issues...'}, 500
        else:
            newSummary = FileSummary(title = file_name, summary = summary)
            db.session.add(newSummary)
            db.session.commit()
            return {'title' : file_name, 'summary' : summary}, 200
        print(file)

             
        
api.add_resource(FileTranscript, '/file_api/<string:type>')