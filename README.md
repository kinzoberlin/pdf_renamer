# pdf_renamer
Use ollama to rename a big folder of randomly named PDF files 

Useful for when you've scraped a bunch of PDFs but they are all named something random or inscrutable like 3424232gvk.pdf. Extracts text from the two pages and generates proper titles for academic papers/documents. It uses the first two pages to handle situations where the first page of a document might be blank. 

Works well with llama3.2 3b which is small enough to run on most computers without a GPU. 

## Prerequisites
- [Ollama](https://ollama.ai/) installed and running
- Python 3.6+
- Required packages: `PyPDF2`, `requests`

## Installation
1. Clone/download this repository
2. Install dependencies:
```pip install -r requirements.txt```

4. Install Ollama and your preferred model:
``` ollama pull llama3.2:latest ``` or your preferred model

## Usage

Start ollama

```ollama serve```

Run python script

```
python pdf_renamer.py
```

When prompted, enter the path to your PDF directory.

When prompted enter whether or not to include PDFs in subdirectories. 

When the script is finished it will say ```Processing complete!```

## Troubleshooting
*Only works on PDFs that contain text!*

For better performance, this script does not ask the LLM to OCR the pdfs, it just copies and pastes the first two pages of text along with the prompt. 

**Changed titles are bad**

It uses this prompt by default, but you need to tweak it depending on your use case. You can do that by editing line 33 in pdf_renamer.py

 prompt = f"""Analyze this academic paper text from the first two pages and return ONLY the actual title. 
    Return NOTHING else except the title in title case. 
    Text sample: {text[:3000]}"""
    
**WARNING**: If you think you might want to keep the original titles of the files, make a backup of them first. 
    
**Can I use a different LLM model?**
  Yes. This script uses llama3.2:latest by default. To use a different model, change line 9 in  pdf_renamer.py. 

**Error codes**
If you get something like these below, it's probably because ollama isn't running or is running a different model then then the one you are trying to use. 


```
Error getting title from Ollama: 404 Client Error: Not Found for url: http://localhost:11434/api/generate
Failed to generate title
```


```
Error getting title from Ollama: HTTPConnectionPool(host='localhost', port=11434): Max retries exceeded with url: /api/generate (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7d12c3e9f470>: Failed to establish a new connection: [Errno 111] Connection refused'))
Failed to generate title
```

To fix this check to see if ollama is already running with
```ollama ps```

Check that you have llama3.2 installed (or whatever model is definied on line 9 of the script with ```ollama list```

If that doesn't work, you can try 'systemctl stop ollama` (on linux) and then run `ollama serve` again. Restarting your computer will accomplish the same. 


