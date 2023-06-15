from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from TranscriptApi.common.utils import title, summarize_youtube_video, summarize_file, summarize_string, answer
from TranscriptApi.models import VideoSummary, FileSummary
from TranscriptApi import db 
import os
import shutil

resources = Blueprint('resources', __name__)
api = Api(resources) 

class VideoTranscript(Resource):
    def get(self, video_id):
        print(request)
        summaryExist = VideoSummary.query.filter_by(video_id = video_id).first() 
        if summaryExist is not None:
            return {'video_id' : video_id, 'title' : summaryExist.title, 'summary' : summaryExist.summary}, 200
        

        try:
            video_title = title(video_id)
        except:
            return {'error' : 'Video ID not valid'}, 400
        try:
            output = summarize_youtube_video('https://www.youtube.com/watch?v=' + video_id, 'TranscriptApi/common/audio')
            print(output)
            newVideo = VideoSummary(title = video_title, video_id = video_id, transcript = f"The title of the video is {video_title}. {output['transcript']}", summary = output['summary'])
            db.session.add(newVideo)
            db.session.commit()
            return {'video_id' : video_id, 'title' : video_title, 'summary' : output['summary']}, 200
        except Exception as e:
            print(e)
            return 500
        
    
api.add_resource(VideoTranscript, '/video_api/<string:video_id>')


class FileTranscript(Resource):
    
    def post(self, type):
        if type == 'pdf' or type == 'txt':
            print(request.files)
            file = request.files['file']
            file_location = os.path.join(current_app.config.get('UPLOAD_FOLDER'), file.filename)
            file.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), file.filename))
            transcript, summary = summarize_file(file_location = file_location, file_extension = type)
            
            file_name = file.filename
        elif type == 'direct_text':
            transcript, summary = request.json['text'], summarize_string(request.json['text'])
            file_name = "Entered Text"
        if summary == "[ERROR]":
            if os.path.exists(current_app.config.get('UPLOAD_FOLDER')):
                shutil.rmtree(current_app.config.get('UPLOAD_FOLDER'))
            os.mkdir(current_app.config.get('UPLOAD_FOLDER'))
            
            return {'error' : 'We are expreriencing some issues...'}, 500
        else:
            newSummary = FileSummary(title = file_name, transcript = transcript, summary = summary)
            db.session.add(newSummary)
            db.session.commit()
            if os.path.exists(current_app.config.get('UPLOAD_FOLDER')):
                shutil.rmtree(current_app.config.get('UPLOAD_FOLDER'))
            os.mkdir(current_app.config.get('UPLOAD_FOLDER'))
            
            return {'file_id' : newSummary.id, 'title' : file_name, 'summary' : summary}, 200
        
api.add_resource(FileTranscript, '/file_api/<string:type>')


class VideoQuestions(Resource):
    def post(self, video_id):
        print(request.json)
        videoExists = VideoSummary.query.filter_by(video_id = video_id).first()
        if videoExists is None:
            transcript, summary = summarize_youtube_video('https://www.youtube.com/watch?v=' + video_id, 'TranscriptApi/common/audio')
            video_title = title(video_id)
            newVideo = VideoSummary(title = video_title, video_id = video_id, transcript = f"The title of the video is {video_title}. {transcript}", summary = summary)

        VideoExists = VideoSummary.query.filter_by(video_id = video_id).first()
        data = request.json # {question : "blabla"}
        try:
            ans = answer(question = data["question"], context = VideoExists.transcript)
            return {'question' : data['question'], 'answer' : ans}, 200
        except:
            return {'error' : 'something went wrong'}, 500

api.add_resource(VideoQuestions, '/video_question_api/<string:video_id>')


class FileQuestions(Resource):
    def post(self, id):
        transcriptData = FileSummary.query.filter_by(id = id).first()
        print(transcriptData)
        if transcriptData is not None:
            ans = answer(question = request.json['question'], context = transcriptData.transcript)
            return {'question' : request.json['question'], 'answer' : ans}, 200 
        else:
            return {'error' : 'file not found'}, 400


api.add_resource(FileQuestions, '/file_question_api/<int:id>')