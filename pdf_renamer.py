import os
import re
import requests
from PyPDF2 import PdfReader
import time

# Configuration
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"  # Change this to your preferred model

def get_pdf_directory():
    """Prompt user for PDF directory path"""
    while True:
        directory = input("Enter the PDF directory path: ").strip()
        if os.path.isdir(directory):
            return directory
        print(f"Error: '{directory}' is not a valid directory. Please try again.")

def get_include_subdirs():
    """Ask user if they want to search subdirectories"""
    while True:
        answer = input("Search subdirectories for PDFs? (yes/no): ").lower().strip()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        print("Please enter 'yes' or 'no'.")

def extract_first_two_pages_text(pdf_path):
    """Extract text from the first two pages of a PDF"""
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        text = []
        for page in pdf.pages[:min(2, len(pdf.pages))]:
            text.append(page.extract_text())
        return "\n".join(text)

def clean_filename(title):
    """Clean and format the title to be a valid filename"""
    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
    clean_title = re.sub(r'\s+', " ", clean_title).strip()
    return clean_title[:150]

def get_title_from_text(text):
    """Use Ollama to generate a proper title from the text"""
    prompt = f"""Analyze this academic paper text from the first two pages and return ONLY the actual title. 
    Return NOTHING else except the title in title case. 

    Text sample: {text[:3000]}"""

    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"].strip('"')
    except Exception as e:
        print(f"Error getting title from Ollama: {e}")
        return None

def process_pdfs(directory, include_subdirs):
    """Process PDFs in directory and optionally subdirectories"""
    pdf_files = []
    
    if include_subdirs:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(directory, file))

    if not pdf_files:
        print("\nNo PDF files found in the specified location.")
        return

    print(f"\nFound {len(pdf_files)} PDF file(s) to process...")

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        file_dir = os.path.dirname(pdf_path)
        
        print(f"\nProcessing: {filename}")
        
        try:
            text = extract_first_two_pages_text(pdf_path)
            if not text.strip():
                print("No text found in first two pages")
                continue
        except Exception as e:
            print(f"Error reading PDF: {e}")
            continue
        
        title = get_title_from_text(text)
        if not title:
            print("Failed to generate title")
            continue
        
        clean_title = clean_filename(title)
        new_filename = f"{clean_title}.pdf"
        new_path = os.path.join(file_dir, new_filename)
        
        try:
            os.rename(pdf_path, new_path)
            print(f"Renamed to: {new_filename}")
        except Exception as e:
            print(f"Error renaming file: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("PDF Renamer Script")
    print("------------------\n")
    
    try:
        pdf_directory = get_pdf_directory()
        include_subdirs = get_include_subdirs()
        print(f"\nStarting processing in: {pdf_directory}")
        if include_subdirs:
            print("Including subdirectories...")
        process_pdfs(pdf_directory, include_subdirs)
        print("\nProcessing complete!")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
