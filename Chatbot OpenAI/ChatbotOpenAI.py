import tkinter as tk
from tkinter import scrolledtext, END
import openai

# Set your OpenAI API key here
openai.api_key = "YOUR_API_KEY"

# Function to interact with the OpenAI language model and get the chatbot response
def get_chatbot_response(input_text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=input_text,
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None,
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error: {e}"

# Function to display the chatbot response in the GUI
def show_chatbot_response():
    user_input = user_input_box.get("1.0", END).strip()
    user_input_box.delete("1.0", END)

    # Check if the user wants to exit
    if user_input.lower() in ["exit", "quit", "bye"]:
        chat_log.insert(tk.END, "Chatbot: Goodbye!\n")
        return

    # Display user input in the chat log
    chat_log.insert(tk.END, "You: " + user_input + "\n")

    # Get and display chatbot response
    chatbot_response = get_chatbot_response(user_input)
    chat_log.insert(tk.END, "Chatbot: " + chatbot_response + "\n")

# Main GUI window
root = tk.Tk()
root.title("Chatbot with OpenAI")

# Chat log
chat_log = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# User input box
user_input_box = scrolledtext.ScrolledText(root, width=40, height=4, wrap=tk.WORD)
user_input_box.grid(row=1, column=0, padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Send", command=show_chatbot_response, bg="black", fg="white", font=("Helvetica", 12, "bold"))
send_button.grid(row=1, column=1, padx=20, pady=20)

# Configure grid weights to make the chat log expandable
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Start the GUI event loop
root.mainloop()
