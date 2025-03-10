<h1 align="center"> AI-based Fraud Management System for UID Aadhar</h1>

## This is a team project made under Infosys Sringboard Internship 5.0, initiative by Infosys Springboard with mentor led guidance

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Usage](#usage)
5. [Workflow](#workflow)
6. [Results](#results)
7. [Future Scope](#future-scope)
8. [License](#license)

---

## Introduction
The **AI-based Fraud Management System** is a Flask-based web application designed to automate document verification and detect fraudulent activities. It uses AI models to classify documents (Aadhaar vs. non-Aadhaar), extract text using OCR, and verify the authenticity of the document by comparing extracted details with a database.

This project was developed as part of the **Infosys Springboard Internship** to address the growing need for secure and efficient document verification systems.

---

## Features
- **Document Classification**: Classifies uploaded documents as **Aadhaar** or **non-Aadhaar** using the YOLOv11n-cls model.
- **OCR Text Extraction**: Extracts text (e.g., UID, name, address) from Aadhaar documents using EasyOCR.
- **Fraud Detection**: Verifies the extracted details against a database to detect mismatches or inconsistencies.
- **User-Friendly Interface**: A Flask-based web app for easy document upload and result display.
- **Real-Time Processing**: Provides quick and accurate results for uploaded documents.

---

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Flask (Python)
- **AI/ML Models**:
  - YOLOv11n-cls (Document Classification)
  - EasyOCR (Text Extraction)
- **Database**: SQLite (for storing verified UIDs and document details)
- **Tools**: Git, GitHub, Visual Studio Code

---

## Usage  

### 📤 Upload a Document:  
1. Go to the **web interface** and upload a document (image or PDF).  

### 📊 View Results:  
- The system will **classify the document**, extract text, and verify its authenticity.  
- Results will be displayed as **Accepted** or **Rejected**.  

---

## Workflow  

1️⃣ **User Uploads Document**: The user uploads a document via the web interface.  
2️⃣ **Document Classification**: The system classifies the document as **Aadhaar or non-Aadhaar**.  
3️⃣ **OCR Text Extraction**: If the document is classified as Aadhaar, the system extracts text using **OCR (Optical Character Recognition)**.  
4️⃣ **Database Verification**: The extracted details are compared against a **database**.  
5️⃣ **Fraud Detection**: The system checks for **inconsistencies or mismatches**.  
6️⃣ **Result Display**: The system displays whether the document is **Accepted or Rejected**.  

---

## Results  

✅ **Document Classification Accuracy**: **98.4%** (on validation set).  
✅ **Fraud Detection**: Successfully detects **mismatches** in UID and other details.  
✅ **User Interface**: Clean and intuitive **design** for easy document upload and result display.  

---

## Future Scope  

🚀 **Support for More Document Types**: Add support for **PAN cards, passports**, etc.  
🚀 **Improved OCR Accuracy**: Enhance OCR for **handwritten text** and **low-quality images**.  
🚀 **Cloud Deployment**: Deploy the system on **cloud platforms** for wider accessibility.  
🚀 **Integration with Government Databases**: Enable **real-time verification** with official databases.  


## License  
This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.
