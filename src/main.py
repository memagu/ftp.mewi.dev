import os
from zipfile import ZipFile
from io import BytesIO

from flask import Flask, send_file, render_template, request

DOWNLOAD_DIR = "../io"
UPLOAD_DIR = "../io"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download")
def download():
    return render_template("download.html", filenames=os.listdir(DOWNLOAD_DIR))


@app.route("/download", methods=("POST",))
def download_files():
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for filename in request.form.values():
            zf.write(f"{DOWNLOAD_DIR}/{filename}", filename)
    stream.seek(0)

    return send_file(stream, as_attachment=True, download_name="archive.zip")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/upload", methods=("POST",))
def upload_files():
    for file in request.files.getlist("files"):
        if not file.filename:
            continue
        file.save(f"{UPLOAD_DIR}/{file.filename}")

    return upload()


def debug():
    app.debug = True
    app.run()


def run():
    app.run(host="0.0.0.0", port=443, ssl_context=("../ssl/certificate.pem", "../ssl/private.pem"))


if __name__ == "__main__":
    run()
