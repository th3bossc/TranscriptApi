---
title: TranscriptApi
emoji: ⚡
colorFrom: pink
colorTo: green
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference



# TranscriptApi

TranscriptApi is a backend service written in Flask that provides a RESTful API for summarizing YouTube videos or uploaded files using deep learning models. It allows users to extract and summarize the textual content from video or audio files, enabling easy access to key information.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Extract and summarize textual content from YouTube videos or uploaded files.
- Utilizes deep learning models for accurate and efficient summarization.
- Provides a RESTful API for easy integration with other applications.
- Supports customization and configuration options to meet specific requirements.

## Installation

1. Clone the repository:

```
git clone https://github.com/th3bossc/TranscriptApi.git
```

2. Navigate to the project directory:

```
cd TranscriptApi
```

3. Install the required dependencies using pip:

```
pip install -r requirements.txt
```

4. Set up the necessary configuration variables, such as API keys, in the `.env` file.

5. Run the Flask development server:

```
python app.py
```

The server should now be running locally at `http://localhost:5000`.

## Usage

To utilize the TranscriptApi service, you can make requests to the provided API endpoints. Here's an example using cURL:

```bash and python requet examples

# summarizing video
curl -X GET http://localhost:5000/video_api/your-video-id 
requests.get("http://localhost:5000/video_api/your-video-id")

# summaring pdf file
curl -X POST -H "Content-type : application/pdf" -F "files=@yourfile.pdf" http://localhost:5000/file_api/pdf
requests.post("http://localhost:5000/file_api/pdf", headers = {'Content-Type' : 'application/pdf'}, files = {'file' : open('yourfile.pdf', 'rb')})

# summaring text file
curl -X POST -H "Content-type : text/plain" -F "files=@yourfile.txt" http://localhost:5000/file_api/txt 
requests.post("http://localhost:5000/file_api/txt", headers = {'Content-Type' : 'text/plain'}, files = {'file' : open('yourfile.txt', 'rb')})

# summarizing raw text data
curl -X POST -d '{"text" : your-text-data}' http://localhost:5000/file_api/direct_text
requests.post("http://localhost:5000/file_api/direct_text, headers = {'Content-Type : 'application/json'}, json = {'text' : your-text-data})

```

Replace `your-video-id` with the actual YouTube video ID you want to summarize.
Replace `yourfile` with the actual file path of the file you want to summarize.
Replace `your-text-data` with the actual text string you want to summarize.

