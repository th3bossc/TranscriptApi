import os
import librosa
import soundfile as sf
from pytube import YouTube
import urllib.parse as urlparse
from moviepy.editor import VideoFileClip
import shutil
import whisper
import torch 
from transformers import pipeline
from tqdm.auto import tqdm
from PyPDF2 import PdfReader


device = 'cuda' if torch.cuda.is_available() else 'cpu'
# device = 'cpu'


checkpoint = 'Th3BossC/SummarizationModel_t5-small_opeai_tldr'






############### video queries ###############
def title(video_id):
    return YouTube('https://www.youtube.com/watch?v=' + video_id).title

def get_video_id(video_url):
    url_data = urlparse.urlparse("http://www.youtube.com/watch?v=z_AbfPXTKms&NR=1")
    query = urlparse.parse_qs(url_data.query)
    video = query["v"][0]
    return video

def get_video(video_url, location, filename = 'audio'):
    if not os.path.exists(location):
        os.makedirs(location)
    video_filename = location + filename + '.mp4'
    audio_filename = location + filename + '.mp3'
    print('[INFO] downloading video...')
    video = YouTube(video_url).streams.filter(file_extension = 'mp4').first().download(filename = video_filename)

    print("something")
    video = VideoFileClip(video_filename)
    print('[INFO] extracting audio from video...')
    video.audio.write_audiofile(audio_filename)
    #os.remove(video_filename)

    return audio_filename

############################################################


############### Audio ###############
def chunk_audio(filename, segment_length, output_dir):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    audio, sr = librosa.load(filename, sr = 44100)
    duration = librosa.get_duration(y = audio, sr = sr)
    num_segments = int(duration / segment_length) + 1
    print(f'[INFO] Chunking {num_segments} chunks...')

    audio_files = []

    for i in range(num_segments):
        start = i*segment_length*sr 
        end = (i+1)*segment_length*sr
        segment = audio[start:end]
        sf.write(os.path.join(output_dir, f"segment_{i}.mp3"), segment, sr)
        audio_files.append(output_dir + f'segment_{i}.mp3')
        
    print(audio_files)
    return audio_files

def transcribe_audio(audio_files, output_file = None, model = whisper.load_model('base', device = device)):
    print('[INFO] converting audio to text...')
    transcripts = []
    model.to(device)
    for audio_file in audio_files:
        response = model.transcribe(audio_file)
        transcripts.append(response['text'])
    if output_file is not None:
        with open(output_file, 'w', encoding = 'utf-8') as f:
            for transcript in transcripts:
                f.write(transcript + '\n')
    
    return transcripts

############################################################


############################################################
    
############### Compile all functions ###############
def summarize_youtube_video(video_url, outputs_dir):
    print(f'[INFO] running on {device}')
    raw_audio_dir = f'{outputs_dir}/raw_audio/'
    chunks_dir = f'{outputs_dir}/chunks/'
    transcripts_file = f'{outputs_dir}/transcripts.txt'
    summary_file = f'{outputs_dir}/summary.txt'
    segment_length = 60*10
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
        os.mkdir(outputs_dir)

    audio_filename = get_video(video_url, raw_audio_dir)
    chunked_audio_files = chunk_audio(audio_filename, segment_length, chunks_dir)
    transcriptions = transcribe_audio(chunked_audio_files, transcripts_file)


    # splitting transcription into sentences    
    sentences = [] 
    for transcript in transcriptions:
        sentences += transcript.split('.')

    sentences_len = [len(sentence) for sentence in sentences]
    sentence_mean_length = sum(sentences_len) // len(sentences_len)

    num_sentences_per_step = int(1600 / (sentence_mean_length))
    num_steps = (len(sentences) // num_sentences_per_step) + (len(sentences) % num_sentences_per_step != 0)

    print(f"""
    [INFO] sentences_len : {len(sentences_len)}
    [INFO] sentence_mean_length : {sentence_mean_length},
    [INFO] num_sentences_per_step : {num_sentences_per_step},
    [INFO] num_steps : {num_steps}
    """)

    summarizer = pipeline('summarization', model = checkpoint, tokenizer = checkpoint, max_length = 200, truncation = True)

    summaries = []

    for i in tqdm(range(num_steps)):
        chunk = ' '.join(sentences[num_sentences_per_step*i : num_sentences_per_step*(i+1)])
        summary = summarizer(chunk, do_sample = False)[0]['summary_text']
        summaries.append(summary)

    complete_summary = ' '.join(summaries)
    with open(summary_file, 'w') as f:
        f.write(complete_summary)

    with open(transcripts_file, 'r') as f:
        complete_transcript = f.read()
    # print(complete_transcript)
    print(complete_summary)
    return {'transcript': complete_transcript, 'summary' : complete_summary}
############################################################



############ File Summarize ############

def extract_text_pdf(file_location = 'TranscriptApi/static/files/temp.pdf'):
    reader = PdfReader(file_location)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text;

def extract_text_txt(file_location = 'TranscriptApi/static/files/temp.txt'):
    with open(file_location, "r") as f:
        text = f.read()
    return text




def summarize_string(text : str):
    sentences = text.split('.')

    summarizer = pipeline('summarization', model = checkpoint, tokenizer = checkpoint, max_length = 200, truncation = True, device = 0)

    sentences_len = [len(sentence) for sentence in sentences]
    sentence_mean_length = sum(sentences_len) // len(sentences_len)

    num_sentences_per_step = int(1600 / (sentence_mean_length))
    num_steps = (len(sentences) // num_sentences_per_step) + (len(sentences) % num_sentences_per_step != 0)

    print(f"""
    [INFO] sentences_len : {len(sentences_len)}
    [INFO] sentence_mean_length : {sentence_mean_length},
    [INFO] num_sentences_per_step : {num_sentences_per_step},
    [INFO] num_steps : {num_steps}
    """)


    summaries = []
    for i in tqdm(range(num_steps)):
        chunk = ' '.join(sentences[num_sentences_per_step*i : num_sentences_per_step*(i+1)])
        summary = summarizer(chunk, do_sample = False)[0]['summary_text']
        summaries.append(summary)

    complete_summary = ' '.join(summaries)
    return complete_summary


################################################


def summarize_file(file_location, file_extension, working_dir = "TranscriptApi/static/files"):
    # _, file_extension = os.path.splitext(file_location)
    text = ""
    if file_extension == 'pdf':
        text = extract_text_pdf(file_location)
    elif file_extension == 'txt':
        text = extract_text_txt(file_location)
    else:
        return "[ERROR]"
    
    if os.path.exists(working_dir):
        shutil.rmtree(working_dir)
    os.mkdir(working_dir)
    return [text, summarize_string(text)]


def answer(question: str, context : str):
    qa = pipeline(task = "question-answering", model = "deepset/roberta-base-squad2")
    return qa(question = question, context = context)['answer']