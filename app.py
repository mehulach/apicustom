# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg
from scipy.spatial import distance


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/get_similar', methods=['POST'])
def cosine_similarity():
    data = request.json
    query_vector = data['query_vector']
    vector_text_pairs = data['vectors']

    # Extract embeddings and their corresponding texts
    vectors = [pair['embeddings'] for pair in vector_text_pairs]
    texts = [pair['text'] for pair in vector_text_pairs]

    # Calculate cosine similarity for each vector
    # Return the index of the most similar vector


    most_similar_index = max(range(len(vectors)), key=lambda index: 1 - distance.cosine(query_vector, vectors[index]))

    return jsonify({'most_similar_text': texts[most_similar_index]})
#START code for get_datetime api

from flask import Flask, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/get_datetime')
def get_datetime():
    # Get current UTC time
    utc_time = datetime.now(pytz.utc)
    
    # Convert UTC time to IST, GMT, and CET timezones
    ist_timezone = pytz.timezone('Asia/Kolkata')
    gmt_timezone = pytz.timezone('GMT')
    cet_timezone = pytz.timezone('CET')
    
    ist_time = utc_time.astimezone(ist_timezone)
    gmt_time = utc_time.astimezone(gmt_timezone)
    cet_time = utc_time.astimezone(cet_timezone)
    
    # Format the times
    ist_formatted = ist_time.strftime('%d/%m/%Y %H:%M:%S IST')
    gmt_formatted = gmt_time.strftime('%d/%m/%Y %H:%M:%S GMT')
    cet_formatted = cet_time.strftime('%d/%m/%Y %H:%M:%S CET')
    
    # Create a dictionary with the times and labels
    times = {
        'IST': ist_formatted,
        'GMT': gmt_formatted,
        'CET': cet_formatted
    }
    
    return jsonify(times)

if __name__ == '__main__':
    app.run(debug=True)

#END of code for get_datetime api
