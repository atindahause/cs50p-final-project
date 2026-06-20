import requests
import sys
import json
import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from dotenv import load_dotenv

# Loads the .env file variables to the system
load_dotenv()

# The API key from Openrouter is not "hardcoded" into the code
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "nvidia/nemotron-nano-9b-v2:free"


def main():
    topic = input("What do you want to learn? ").strip()
    if not topic:
        sys.exit("Invalid subject.")
    
    print(f"Generating flashcards about {topic}...")
    
    response = get_ai_response(topic)
    # The get_ai_response() function is called with the contents of the topic variable that was entered by the user
    #print("RAW RESPONSE:")
    #print(response)

    flashcards = parse_flashcards(response)
    # The parse_flashcards() function is called with the content obtained from the get_ai_response() function
    #print("PARSED:")
    #print(flashcards)

    
    if flashcards:
        # File name based on the chosen topic (removing blankspaces)
        filename = f"flashcards_{topic.replace(' ', '_')}.pdf"
        save_to_pdf(flashcards, filename)
        # The save_to_pdf() function saves the contents to a PDF file

        print(f"Success! PDF '{filename}' created.")
    else:
        print("It wasn't possible to generate flashcards, check AI API's connection.")


# This function query Openrouters' API and returns raw data
def get_ai_response(topic):
    # Check if the .env file is ok
    if not API_KEY:
        print("Error: API key not found. Setup the .env file")
        return None
    # Query the OpenRouter's API and returns raw data
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    Generate exactly 3 simple flashcards about {topic}.

    Return ONLY valid JSON in this format:

    [
    {{"question":"...", "answer":"..."}},
    {{"question":"...", "answer":"..."}},
    {{"question":"...", "answer":"..."}}
    ]
    """
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Connection error: {e}")
        return None


# This function Transforms the raw data into tuples
def parse_flashcards(text):
    # Transforms the response into tuples
    try:
        data = json.loads(text)
        return [
            (item["question"], item["answer"])
            for item in data
        ]
    except Exception:
        return []


# This function generates a formated .PDF file (fpdf2 library)
def save_to_pdf(cards, filename):
    # Generates a formated PDF  with the flashcards acquired from AI
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(
    0,
    10,
    "My Study Flashcards",
    align="C",
    new_x=XPos.LMARGIN,
    new_y=YPos.NEXT
    )
    #pdf.cell(0, 10, "My Study Flashcards", ln=True, align='C')
    #pdf.ln(10)

    for q, a in cards:
        y_start = pdf.get_y()

        # Question box
        pdf.set_font("helvetica", "B", 8)
        pdf.set_fill_color(230, 230, 230)
        pdf.set_xy(10, y_start)  # coluna esquerda
        pdf.multi_cell(90, 5, f"Q: {q}", border=1, fill=True)

        y_after_q = pdf.get_y()

        # Answer box (located at the same initial line)
        pdf.set_font("helvetica", "", 8)
        pdf.set_xy(110, y_start)  # coluna direita
        pdf.multi_cell(90, 5, f"A: {a}", border=1)

        # Adjusts the line for the biggest block
        y_after_a = pdf.get_y()
        pdf.set_y(max(y_after_q, y_after_a) + 5)

    pdf.output(filename)
    return True

if __name__ == "__main__":
    main()