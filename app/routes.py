import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db, mail
from app.models import AnalysisResult
from app.utils.file_processing import read_file
from app.utils.text_processing import preprocess_text
from app.utils.similarity import calculate_similarity
from app.utils.web_search import search_web
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'files' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        filenames = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                filenames.append(filename)
            else:
                flash(f'Invalid file format: {file.filename}', 'error')
                return redirect(request.url)
        
        result = analyze_files(filenames)
        return render_template('report.html', result=result)
    
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def analyze_files(filenames):
    texts = []
    for filename in filenames:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        text = read_file(file_path)
        preprocessed_text = preprocess_text(text)
        texts.append(preprocessed_text)
    
    if len(texts) > 1:
        # Compare multiple files
        similarities = []
        for i in range(len(texts)):
            for j in range(i+1, len(texts)):
                similarity = calculate_similarity(texts[i], texts[j])
                similarities.append({
                    'file1': filenames[i],
                    'file2': filenames[j],
                    'similarity': similarity
                })
        
        result = {
            'type': 'multiple',
            'similarities': similarities
        }
    else:
        # Web search for a single file
        chunks = split_text(texts[0])
        web_results = []
        for chunk in chunks:
            search_results = search_web(chunk, current_app.config['GOOGLE_API_KEY'], current_app.config['GOOGLE_CSE_ID'])
            web_results.extend(search_results.get('items', []))
        
        result = {
            'type': 'single',
            'filename': filenames[0],
            'web_results': web_results
        }
    
    # Store results in database
    analysis_result = AnalysisResult(
        filename=', '.join(filenames),
        similarity_percentage=max(s['similarity'] for s in similarities) if result['type'] == 'multiple' else 0,
        details=str(result),
        sources=str(web_results) if result['type'] == 'single' else None
    )
    db.session.add(analysis_result)
    db.session.commit()
    
    # Send email to teacher
    # send_email_report(result)
    
    return result

def split_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def send_email_report(result):
    subject = "Plagiarism Detection Report"
    sender = current_app.config['MAIL_USERNAME']
    recipients = ["ipafadnam6@gmail.com"]  # Replace with actual teacher's email
    
    html_content = render_template('email_report.html', result=result)
    
    msg = Message(subject=subject,
                  sender=sender,
                  recipients=recipients,
                  html=html_content)
    
    mail.send(msg)

@main.route('/get_file_content', methods=['POST'])
def get_file_content():
    filename = request.json['filename']
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    content = read_file(file_path)
    return jsonify({'content': content})