from flask import Flask, request, jsonify, render_template, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from ultralytics import YOLO
from easyocr import Reader
import zipfile
import pandas as pd
import cv2
from fuzzywuzzy import fuzz, process
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'

classifier = YOLO("models/classification.pt")
detector = YOLO("models/detection.pt")
reader = Reader(['en'])

db = SQLAlchemy(app)

class Aadhar_Results(db.Model):
    ID = db.Column(db.String(100), primary_key=True)
    UID = db.Column(db.String(15), nullable=False)
    UID_Score = db.Column(db.Integer, default = 0)
    Name = db.Column(db.String(100), default="Non-Aadhar")
    Name_Score = db.Column(db.Integer, default=0)
    Address = db.Column(db.String(200), default="Non-Aadhar")
    Address_Score = db.Column(db.Integer, default=0)
    Document_Type = db.Column(db.String(10), nullable=False)
    Final_Remarks = db.Column(db.String(20), nullable=False)
    Acceptance = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Table>"




def process_image(image_path):
    if classifier.predict(image_path)[0].probs.numpy().top1 == 0:
        fields = detector(image_path)
        image = cv2.imread(image_path)
        extracted_data = {}
        for field in fields[0].boxes.data.tolist():
            x1, y1, x2, y2, confidence, class_id = map(int, field[:6])
            field_class = detector.names[class_id]
            cropped_roi = image[y1:y2, x1:x2]
            gray_roi = cv2.cvtColor(cropped_roi, cv2.COLOR_BGR2GRAY)
            text = reader.readtext(gray_roi, detail=0)
            extracted_data[field_class] = ' '.join(text)
        return extracted_data
    return None

# Helper Functions
def normalize_text(text):
    if not text:
        return "text empty"
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split()).lower()

def calculate_match_score(input_value, extracted_value):
    if pd.isna(input_value) or pd.isna(extracted_value):
        return 0
    return fuzz.ratio(str(input_value), str(extracted_value))


def name_match(input_name, extracted_name):
    if extracted_name is None:
        return False
    input_name = normalize_text(input_name)
    extracted_name = normalize_text(extracted_name)

    if input_name == extracted_name:
        return True

    input_parts = input_name.split()
    extracted_parts = extracted_name.split()

    if sorted(input_parts) == sorted(extracted_parts):
        return True

    if len(input_parts) == 2 and len(extracted_parts) == 3:
        if input_parts[0] == extracted_parts[0] and input_parts[1] == extracted_parts[2]:
            return True
    if len(input_parts) == 3 and len(extracted_parts) == 2:
        if extracted_parts[0] == input_parts[0] and extracted_parts[1] == input_parts[2]:
            return True

    for part in input_parts:
        if part not in extracted_parts:
            return False
    return True


def address_match(input_address, extracted_address):
    if input_address is None or extracted_address is None:
        return False, 0.0, {}

    # Handle input_address if it's a Series
    if isinstance(input_address, pd.Series):
        input_address = input_address.to_dict()
    
    extracted_address = normalize_text(extracted_address)
    final_score = 0
    
    weights = {
        "State": 0.2,
        "Landmark": 0.2,
        "Premise Building Name": 0.2,
        "City":0.2,
        "Street Road Name":0.1,
        "Floor Number": 0.05,
        "House Flat Number": 0.05
    }
    tokens = extracted_address.split(" ")
    # Component matching logic
    for field, weight in weights.items():
        input_value = input_address.get(field, "")
        match_score = fuzz.token_set_ratio(normalize_text(input_value), extracted_address) if input_value else 0
        input_address[field + " Match Score"] = match_score
        final_score += match_score * weight
    pincode_score = process.extractOne(input_address.get("PINCODE"), tokens)[1]
    input_address['PINCODE Match Score'] = pincode_score
    pincode_matched = True if input_address['PINCODE Match Score'] == 100 else False

    return final_score >= 70 and pincode_matched, final_score, input_address



def compare_data(input_data, json_data):
    excel_data = input_data.copy()
    for idx, row in excel_data.iterrows():
        serial_no = row.get("SrNo")
        uid = row.get("UID")
        extracted = json_data.get(serial_no)

        if extracted:
            extracted_uid = extracted.get("uid", "").replace(" ", "")
            extracted_name = extracted.get("name", "")
            extracted_address = extracted.get("address", "")
            row['Extracted UID'] = extracted_uid
            row['Extracted Name'] = extracted_name
            row['Extracted Address'] = extracted_address
            # UID Match
            uid_match = uid == extracted_uid
            uid_score = 100 if uid_match else 0
            row['UID Match Score'] = uid_score

            # Name Match
            name_match_result = name_match(row.get("Name"), extracted_name)
            name_score = calculate_match_score(row.get("Name"), extracted_name)
            row['Name Match Score'] = name_score
            row['Name match percentage'] = name_score

            # Address Match
            address_match_result, address_score, partial_scores = address_match(row, extracted_address)
            if partial_scores:
                row['House Flat Number Match Score'] = partial_scores['House Flat Number Match Score']
                row['Street Road Name Match Score'] = partial_scores['Street Road Name Match Score']
                row['City Match Score'] = partial_scores['City Match Score']
                row['Floor Number Match Score'] = partial_scores['Floor Number Match Score']
                row['Premise Building Name Match Score'] = partial_scores['Premise Building Name Match Score']
                row['Landmark Match Score'] = partial_scores['Landmark Match Score']
                row['State Match Score'] = partial_scores['State Match Score']
                row['Final Address Match'] = address_match_result
                row['Final Address Match Score'] = address_score
                row['PINCODE Match Score'] = partial_scores['PINCODE Match Score']
            
            # Final Match
            overall_match = uid_match and name_match_result and address_match_result

            row['Overall Match'] = overall_match

            if overall_match:
                row['Final Remarks'] = "All matched"
            elif not uid_match:
                row['Final Remarks'] = "UID mismatch"
            elif not name_match_result:
                row['Final Remarks'] = "Name mismatch"
            elif not address_match_result:
                if address_score >= 70: 
                    row['Final Remarks'] = "PINCODE mismatch"
                else:
                    row['Final Remarks'] = "Address mismatch"
            else:
                if extracted_address is None:
                    row['Final Remarks'] = "Address missing in aadhar"
                elif extracted_name is None:
                    row['Final Remarks'] = "Name missing in aadhar"
                else:
                    row['Final Remarks'] = "Non Aadhar"

            row["Document Type"] = "Aadhaar" if overall_match else "Non Aadhar"
        else:
            row.replace(float('nan'), 0)
            row['Final Remarks'] = "Non Aadhar"
            row['Document Type'] = "Non Aadhar"
        excel_data.loc[idx] = row
    return excel_data

@app.route('/download', methods=['GET'])
def download_results():
    file_path = os.path.join(app.config['RESULTS_FOLDER'], 'results.xlsx')
    return send_file(file_path, as_attachment=True)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/index')
def home():
    return render_template('test.html')


@app.route('/upload', methods=['POST'])
def upload_files():

    if 'zipfile' in request.files and 'excelfile' in request.files:
        zip_file = request.files['zipfile']
        excel_file = request.files['excelfile']

        # Save files
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_file.filename)
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_file.filename)
        zip_file.save(zip_path)
        excel_file.save(excel_path)

        # Unzip and process images
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(app.config['UPLOAD_FOLDER'])

        image_paths = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.jpg', '.png'))]
        processed_results = {}

        for image_path in image_paths:
            file_name = os.path.basename(image_path)
            key = file_name.split('.')[0][:3]
            extracted_data = process_image(image_path)
            
            if extracted_data:
                if key in processed_results:
                    # Perform union of the existing and new data
                    processed_results[key] = {**processed_results[key], **extracted_data}
                else:
                    processed_results[key] = extracted_data

        # Read Excel and compare data
        df = pd.read_excel(excel_path)
        df = df.astype('str')
        comparison_results = compare_data(df, processed_results)
        comparison_results['Accepted/Rejected'] = np.where(comparison_results['Final Remarks'] == 'All matched', 'Accepted', 'Rejected')

        # Save results to a new Excel file
        results_df = pd.DataFrame(comparison_results)
        os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
        results_file_path = os.path.join(app.config['RESULTS_FOLDER'], 'results.xlsx')
        results_df.to_excel(results_file_path, index=False)

        # Save results to database
        for _, row in comparison_results.iterrows():
            result = Aadhar_Results(
                ID=row['SrNo'],
                UID=row['UID'],
                UID_Score=row['UID Match Score'],
                Name=row['Name'],
                Name_Score=row['Name Match Score'],
                Address=row['Extracted Address'],
                Address_Score=row.get('Final Address Match Score', 0),
                Document_Type=row['Document Type'],
                Final_Remarks=row['Final Remarks'],
                Acceptance=row['Accepted/Rejected']
            )
            db.session.merge(result)  # Use merge to update or insert
        db.session.commit()
        document_counts = results_df['Document Type'].value_counts()
        category_distribution = results_df['Accepted/Rejected'].value_counts()
        task_distribution = results_df['Final Remarks'].value_counts()

        # Create the figure and the grid layout
        fig = plt.figure(figsize=(15, 6))
        grid = fig.add_gridspec(2, 3, wspace=0.3, hspace=0.3)

        # Full-height bar graph on the left
        ax1 = fig.add_subplot(grid[:, 0])  # Spanning all rows of the first column
        ax1.bar(document_counts.index, document_counts.values, color='skyblue')
        ax1.set_title('Document Type')
        ax1.set_ylabel('Count')
        ax1.set_xlabel('Type')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Pie chart on the top right
        ax2 = fig.add_subplot(grid[0, 1:])
        ax2.pie(category_distribution.values, labels=category_distribution.index, autopct='%1.1f%%', startangle=90, colors=['gold', 'lightgreen', 'lightcoral'])
        ax2.set_title('Category Distribution')

        # Horizontal bar graph on the bottom right
        ax3 = fig.add_subplot(grid[1, 1:])
        ax3.barh(task_distribution.index, task_distribution.values, color='lightblue')
        ax3.set_title('Final Remarks')
        ax3.set_xlabel('Count')
        ax3.grid(axis='x', linestyle='--', alpha=0.7)
        
        # Save the figure
        os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
        results_file_path = os.path.join(app.root_path, 'static', 'results', 'analysis.png')
        plt.savefig(results_file_path, bbox_inches='tight')
        plt.close(fig)
        print(results_file_path)
        return jsonify({"message": "Files processed successfully!", "results": comparison_results[['SrNo', 'Document Type',  'Accepted/Rejected', 'Final Remarks']].to_dict(orient='records'), "figure": url_for('static', filename='results/analysis.png')})

    return jsonify({"error": "Both files are required."}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized!")
    app.run(debug=True)
