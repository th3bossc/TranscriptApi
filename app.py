from transcript_api import create_app
from threading import Thread

app = create_app()


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)


# def run():
#     app.run(host = "0.0.0.0", port = 8080)  

# def keep_alive():
#     t = Thread(target = run)
#     t.start()

# keep_alive()