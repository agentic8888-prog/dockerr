import os
import shutil
from pypdf import PdfReader
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD
import json

def list_files(path):

    try:

        files = os.listdir(path)

        return "\n".join(files)

    except Exception as e:

        return f"Error: {str(e)}"


def read_file(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except Exception as e:

        return f"Error: {str(e)}"
    



def copy_folder(source, destination):

    try:

        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=True
        )

        return (
            f"Successfully copied\n"
            f"FROM: {source}\n"
            f"TO: {destination}"
        )

    except Exception as e:

        return f"Error: {str(e)}"
    

def read_pdf(pdf_path):

    try:

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text[:15000]

    except Exception as e:

        return f"Error: {str(e)}"
    
    
def send_email(to_email, subject, body):

    try:

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        return (
            f"Email sent successfully to "
            f"{to_email}"
        )

    except Exception as e:

        return f"Error: {str(e)}"
