#coding: utf-8

import tkinter as tk
from tkinter import filedialog
import subprocess
import openai
import os
import configparser

def browse_input_file():
    input_file_path = filedialog.askopenfilename(defaultextension=".mp3")
    if input_file_path:
        input_file_entry.delete(0, tk.END)  # Delete current content
        input_file_entry.insert(0, input_file_path)  # Insert path into entry
        if output_file_entry.get() == "":
            output_file_path = os.path.splitext(input_file_path)[0]+'.txt'
            output_file_entry.delete(0, tk.END)  # Delete current content
            output_file_entry.insert(0, output_file_path)  #Insert path into entry

def browse_output_file():
    output_file_path = filedialog.askopenfilename(defaultextension=".txt")
    if output_file_path:
        output_file_entry.delete(0, tk.END)  # Delete current content
        output_file_entry.insert(0, output_file_path)  # Insert path into entry

# Function to save the openAI API key in environment variables
def save_api_key():
    key = api_key_entry.get()
    if (test_key()==True):
        subprocess.call(['setx', 'OPENAI_API_KEY', key])
        update_text_from_script("Valid openAI API key sucessfully registred")

def run_transcribe():
    # Transcribe only (automatic language detection)
    openai.api_key = api_key_entry.get()
    test_key()
    input_path = input_file_entry.get()
    output_path = output_file_entry.get()
    if input_path:
        audio_file= open(input_path,"rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        update_text_from_script(transcript.text)
        if output_path:
            outfile = open(output_path,"a+")
            outfile.write(transcript.text)
            outfile.close()
    else:
        update_text_from_script("Please provide the input audio file path.\r\n")
    

def run_translate():
    # transcribe + translate
    openai.api_key = api_key_entry.get()
    test_key()
    input_path = input_file_entry.get()
    output_path = output_file_entry.get()
    if input_path:
        audio_file= open(input_path,"rb")
        transcript = openai.Audio.translate("whisper-1", audio_file)
        update_text_from_script(transcript.text)
        if output_path:
            outfile = open(output_path,"a+")
            outfile.write(transcript.text)
            outfile.close()
    else:
        update_text_from_script("Please provide the input audio file path.\r\n")
    
    

def update_text_from_script(text):
    text_widget.delete(1.0, tk.END)  #  Delete current content of the text window
    text_widget.insert(tk.END, text)  # Insert content inside the text window

def test_openai_api_key():
    if 'OPENAI_API_KEY' in os.environ:
        api_key_entry.delete(0, tk.END)  # Delete current content
        key = os.environ['OPENAI_API_KEY']
        api_key_entry.insert(0, key)  # Insert openAI API key in the entry
        return True

def test_key():
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="Testing the openAI API key validity",
            max_tokens=5
        )
        return True
    except Exception as e:
        update_text_from_script("Error while trying to validate your openAI API key :" +  str(e) + "\r\n")
        return False


if __name__ == "__main__":
    
    # configparser used to store the default directories ()
    config = configparser.ConfigParser()

    # Creation of the main window
    root = tk.Tk()
    root.title("Speech to text")

    # Creation of labels indicating the utility of the entries
    input_label   = tk.Label(root, text="Input audio file :".rjust(18), font=("Monaco", 10), justify="right")
    output_label  = tk.Label(root, text="Output text file :".rjust(18), font=("Monaco", 10), justify="right")
    api_key_label = tk.Label(root, text="OpenAI API key :".rjust(18), font=("Monaco", 10), justify="right")

    # Add title
    title_label = tk.Label(root, text="Speech to text", font=("Monaco", 24))
    title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Use the grid geometry manager to organize labels
    api_key_label.grid(row=1, column=0, padx=10, pady=10)
    input_label.grid(row=2, column=0, padx=10, pady=10)
    output_label.grid(row=3, column=0, padx=10, pady=10)

    # Create text fields (Entry) for directories and the API key
    api_key_entry = tk.Entry(root, width=70)  # Text field for API key
    input_file_entry = tk.Entry(root, width=70)  # Text field for input audio file directory
    output_file_entry = tk.Entry(root, width=70)  # Text field for outpout text file directory
    
    # Use grid to organize text boxes
    input_file_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
    output_file_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
    api_key_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    # Create "Browse" buttons to select key and input/output files
    save_api_key_button = tk.Button(root, text="Save".center(11), command=save_api_key, font=("Monaco", 10), justify="left")
    browse_input_button = tk.Button(root, text="Browse".center(11), command=browse_input_file, font=("Monaco", 10), justify="left")
    browse_output_button = tk.Button(root, text="Browse".center(11), command=browse_output_file, font=("Monaco", 10), justify="left")

    # Use grid to organize the "Browse" buttons
    browse_input_button.grid(row=2, column=3, padx=10, pady=10)
    browse_output_button.grid(row=3, column=3, padx=10, pady=10)
    save_api_key_button.grid(row=1, column=3, padx=10, pady=10)

    # Create buttons to run scripts
    run_transcribe_button = tk.Button(root, text="Transcribe", command=run_transcribe, font=("Monaco", 10), justify='left')
    run_translate_button = tk.Button(root, text="Translate", command=run_translate, font=("Monaco", 10), justify='right')

    # Use grid to organize execution buttons above the text box
    run_transcribe_button.grid(row=5, column=1, padx=10, pady=10)
    run_translate_button.grid(row=5, column=2, padx=10, pady=10)

    # Create a text box to display the content
    text_widget = tk.Text(root, wrap=tk.WORD, width=90, height=10)
    text_widget.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
    
    # Check if openAI api key exists in environment variables 
    test_openai_api_key()

    # Start the main GUI loop
    root.mainloop()

    
    