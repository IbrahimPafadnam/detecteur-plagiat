from app import db
from datetime import datetime

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    similarity_percentage = db.Column(db.Float, nullable=False)
    details = db.Column(db.Text, nullable=False)
    sources = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<AnalysisResult {self.filename}>'