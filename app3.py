import gradio as gr
from selenium import webdriver
import time
import pytesseract
from PIL import Image
import nltk
from nltk.tokenize import sent_tokenize
import openai

# Set up OpenAI API key
openai.api_key = "API Key"

# Set up Selenium driver (remove executable_path parameter)
driver = webdriver.Chrome()

# Download the 'punkt' tokenizer if not already downloaded
nltk.download('punkt')

# Function to process URL and generate AI response
def process_url(url):
    # Open the web page
    driver.get(url)

    # Scroll to capture entire page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for page to load completely

    # Capture screenshot
    screenshot_path = "screenshot.png"
    driver.save_screenshot(screenshot_path)

    # Close the browser
    driver.quit()

    # Load screenshot image
    screenshot = Image.open(screenshot_path)

    # Perform OCR on the screenshot
    extracted_text = pytesseract.image_to_string(screenshot)

    # Split the extracted text into sentences using sent_tokenize
    extracted_sentences = sent_tokenize(extracted_text)

    # Create conversation history with extracted sentences and "remember this information"
    chat_history = [
        {"role": "system", "content": "You are a helpful AI Assistant."}
    ]

    # Add each extracted sentence with the "Remember this information" prompt
    for sentence in extracted_sentences:
        chat_history.append({"role": "user", "content": f"Remember this information.\n{sentence}"})
        chat_history.append({"role": "user", "content": "What do you know about this?"})

    # Generate AI response using GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    # Extract AI response
    ai_response = response.choices[0].message['content']

    return ai_response

iface = gr.Interface(
    fn=process_url,
    inputs=gr.inputs.Textbox(label="Enter URL to scrape"),
    outputs=gr.outputs.Textbox(label="AI Response")
)

if __name__ == "__main__":
    iface.launch()
