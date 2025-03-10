<h1 align="center">Al-based Fraud Management System for UID Aadhaar Using AI-OCR</h1>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Infosys-Springboard-brightgreen.svg" alt="Infosys Springboard">
  <img src="https://img.shields.io/badge/Status-Completed-success.svg" alt="Status">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7a6d4988-738f-4f17-ad5a-0f77e364dfad" alt="Project Banner">
</p>

## 🌟 Overview
This team project was developed under the **Infosys Springboard Internship 5.0** with mentor-led guidance. Our goal was to create a secure and efficient **AI-based Fraud Management System** for document verification.

## 📜 Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Usage](#usage)
5. [Workflow](#workflow)
6. [Results](#results)
7. [Future Scope](#future-scope)
8. [License](#license)

---

## 🔍 Introduction
The **AI-based Fraud Management System** is a Flask-based web application designed to automate document verification and detect fraudulent activities. Using advanced AI models, it classifies documents (e.g., Aadhaar) and ensures their authenticity.

This project was developed as part of the **Infosys Springboard Internship** to address the growing need for secure and efficient document verification systems.

---

## ✨ Features
- **Document Classification**: Classifies uploaded documents as **Aadhaar** or **non-Aadhaar** using the YOLOv11n-cls model.
- **OCR Text Extraction**: Extracts text (e.g., UID, name, address) from Aadhaar documents using EasyOCR.
- **Fraud Detection**: Verifies the extracted details against a database to detect mismatches or inconsistencies.
- **User-Friendly Interface**: A Flask-based web app for easy document upload and result display.
- **Real-Time Processing**: Provides quick and accurate results for uploaded documents.

---

## 🛠 Technologies Used
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Flask (Python)
- **AI/ML Models**:
  - YOLOv11n-cls (Document Classification)
  - EasyOCR (Text Extraction)
- **Database**: SQLite (for storing verified UIDs and document details)
- **Tools**: Git, GitHub, Visual Studio Code

---

## 🚀 Usage

### Upload a Document
1. Go to the **web interface** and upload a document (image or PDF).

### View Results
- The system will **classify the document**, extract text, and verify its authenticity.
- Results will be displayed as **Accepted** or **Rejected**.

---

## 🔄 Workflow

1. **User Uploads Document**: The user uploads a document via the web interface.
2. **Document Classification**: The system classifies the document as **Aadhaar or non-Aadhaar**.
3. **OCR Text Extraction**: If the document is classified as Aadhaar, the system extracts text using **OCR (Optical Character Recognition)**.
4. **Database Verification**: The extracted details are compared against a **database**.
5. **Fraud Detection**: The system checks for **inconsistencies or mismatches**.
6. **Result Display**: The system displays whether the document is **Accepted or Rejected**.

---

## 📈 Results

- **Document Classification Accuracy**: **98.4%** (on validation set).
- **Fraud Detection**: Successfully detects **mismatches** in UID and other details.
- **User Interface**: Clean and intuitive **design** for easy document upload and result display.

---

## 🌍 Future Scope

- **Support for More Document Types**: Add support for **PAN cards, passports**, etc.
- **Improved OCR Accuracy**: Enhance OCR for **handwritten text** and **low-quality images**.
- **Cloud Deployment**: Deploy the system on **cloud platforms** for wider accessibility.
- **Integration with Government Databases**: Enable **real-time verification** with official databases.

---

## 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by the Infosys Springboard Internship Team
</p>
