import tkinter as tk
from tkinter import ttk, messagebox, font
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


class SimpleChatbot:
    def __init__(self):
        self.pipeline = make_pipeline(
            CountVectorizer(),
            MultinomialNB()
        )

        self.responses = {
            "Hello": "Hello! How can I assist you today?",
            "How are you?": "I'm a bot, so I don't feel great, but I'm here to answer your questions!",
            "What are you doing?": "I'm working as a chatbot. How about you?",
            "Goodbye": "Goodbye! Have a great day!",
            "Tell me a joke": "Sure, here's one: Why don't scientists trust atoms? Because they make up everything!",
            "What's the weather like today?": "I'm sorry, I don't have access to real-time data. You can check a weather website for that!",
            "What's your favorite color?": "I don't have personal preferences, but I like all colors!",
            "What's the meaning of life?": "The meaning of life is a philosophical question that has different answers for different people.",
            "Can you sing a song?": "I wish I could, but I'm a chatbot and not capable of singing. How about I tell you a fun fact instead?",
            "Tell me something interesting": "Sure! Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
        }
        self.default_response = "I'm not sure how to respond to that. Feel free to ask me something else!"
        self.train()

    def train(self):
        try:
            questions = list(self.responses.keys())
            answers = list(self.responses.values())
            self.pipeline.fit(questions, answers)
        except Exception as e:
            print("Error during training:", e)

    def get_response(self, user_input):
        if user_input in self.responses:
            return self.responses[user_input]
        else:
            return self.default_response


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.chatbot = SimpleChatbot()

    def setup_gui(self):
        root.title("Simple Chatbot")
        root.configure(bg="#FFD39B")

        custom_font = font.Font(size=12)

        conversation_display = tk.Text(root, height=20, width=86, font=custom_font, bg="#FFD39B", fg="white")
        conversation_display.tag_configure("bold",
                                           font=(custom_font.actual("family"), custom_font.actual("size"), "bold"))
        conversation_display.pack()

        initial_message = "Please Enter Your Message Here"
        user_input = tk.Entry(root, width=85, font=custom_font, fg="gray")
        user_input.insert(0, initial_message)
        user_input.bind("<FocusIn>", self.clear_initial_message)
        user_input.bind("<FocusOut>", self.restore_initial_message)
        user_input.pack(pady=(10, 0))

        button_style = ttk.Style()
        button_style.configure("Custom.TButton", font=custom_font, foreground="black", background="black")

        def send_message():
            user_text = user_input.get()
            conversation_display.insert(tk.END, "You: ", "user_tag")
            conversation_display.insert(tk.END, f"{user_text}\n", "user_message")

            chatbot_response = self.chatbot.get_response(user_text)
            conversation_display.insert(tk.END, "Chatbot: ", "chatbot_tag")
            conversation_display.insert(tk.END, f"{chatbot_response}\n", "chatbot_message")

            user_input.delete(0, tk.END)

        send_button = ttk.Button(root, text="Send", command=send_message, style="Custom.TButton")
        send_button.pack(pady=(5, 0))

        def show_prompts():
            prompts_window = tk.Toplevel(root)
            prompts_window.title("Chatbot Prompts")

            prompts_text = tk.Text(prompts_window, height=10, width=50, font=("Helvetica", 12))
            prompts_text.pack()

            prompts = [
                "Hello", "How are you?", "What are you doing?", "Goodbye", "Tell me a joke",
                "What's the weather like today?", "What's your favorite color?", "What's the meaning of life?",
                "Can you sing a song?", "Tell me something interesting"
            ]

            initial_message = f"Welcome! You can start a conversation by using these prompts:\n\n"
            initial_message += "\n".join(f"- {prompt}" for prompt in prompts)
            initial_message += "\n\nFeel free to ask me anything!"

            prompts_text.insert(tk.END, initial_message)

        prompts_button = ttk.Button(root, text="Show Prompts", command=show_prompts, style="Custom.TButton")
        prompts_button.pack(pady=(5, 0))

        def exit_application():
            if messagebox.askyesno("Exit", "Are you sure you want to close this app?"):
                root.destroy()

        exit_button = ttk.Button(root, text="Exit", command=exit_application, style="Custom.TButton")
        exit_button.pack(pady=(5, 10))

        tag_configs = [
            ("user_tag", "green"),
            ("user_message", "green"),
            ("chatbot_tag", "#8B2323"),
            ("chatbot_message", "#8B2323")
        ]

        for tag, color in tag_configs:
            conversation_display.tag_configure(tag, foreground=color,
                                               font=(custom_font.actual("family"), custom_font.actual("size"), "bold"))

    def clear_initial_message(self, event):
        user_input = event.widget
        if user_input.get() == "Please Enter Your Message Here":
            user_input.delete(0, tk.END)
            user_input.config(fg="black")

    def restore_initial_message(self, event):
        user_input = event.widget
        if user_input.get() == "":
            user_input.insert(0, "Please Enter Your Message Here")
            user_input.config(fg="gray")


root = tk.Tk()
app = ChatbotApp(root)
root.mainloop()
