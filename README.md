# Tesseract-Flask

**NOTE: This project was originally a pre-internship assignment, therefore not much effort was put in the frontend since text extraction and task scheduling were the only main goals to achieve and showcase.**

A simple Flask app that uses Pytesseract to extract texts from uploaded images.

Highlights:
- You can upload the image and schedule the extraction process.
- MongoDB Atlas is used to store images along with their text (if extracted) and scheduled extraction time.
- Uses flask-sessions and cookies to keep track of each user's uploads & results.
- Sessions are also stored on MongoDB Atlas.

If you are going to run it then make sure tesseract-ocr is installed on your system and it's in PATH.
