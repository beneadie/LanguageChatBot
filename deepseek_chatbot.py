import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from openai import OpenAI

class UserMessage:
    def __init__(self, parent, message):
        self.parent = parent
        self.message = message
        self.display()

    def display(self):
        """Display the user's message in the chat window."""
        self.frame = tk.Frame(self.parent, bg="#e1f5fe")  # Light blue background
        self.frame.pack(fill=tk.X, pady=5)

        self.label = tk.Label(self.frame, text=f"You: {self.message}", font=("Arial", 12), bg="#e1f5fe", anchor="w")
        self.label.pack(fill=tk.X, padx=10, pady=5)


class ChatbotMessage:
    def __init__(self, parent, message, sender="Chatbot", translation=None, suggestion=None, romanized=None):
        self.parent = parent
        self.message = message
        self.sender = sender
        self.translation = translation  # Translation text
        self.suggestion = suggestion  # Suggestion text
        self.romanized = romanized  # Romanized text (for Japanese, Korean, Chinese)
        self.translation_visible = False  # Translation visibility state
        self.suggestion_visible = False  # Suggestion visibility state
        self.romanized_visible = False  # Romanized visibility state
        self.display()

    def display(self):
        """Display the chatbot's message in the chat window with optional buttons."""
        self.frame = tk.Frame(self.parent, bg="#f0f4c3")  # Light green background
        self.frame.pack(fill=tk.X, pady=5)

        # Message label
        self.message_label = tk.Label(self.frame, text=f"{self.sender}: {self.message}", font=("Arial", 12), bg="#f0f4c3", anchor="w")
        self.message_label.pack(fill=tk.X, padx=10, pady=5)

        # Button to toggle romanized text (if available)
        if self.romanized:
            self.romanized_button = tk.Button(self.frame, text="Show Romanized", command=self.toggle_romanized, font=("Arial", 10))
            self.romanized_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Button to toggle translation
        if self.translation:
            self.translation_button = tk.Button(self.frame, text="Show Translation", command=self.toggle_translation, font=("Arial", 10))
            self.translation_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Button to toggle suggestion
        if self.suggestion:
            self.suggestion_button = tk.Button(self.frame, text="Show Suggestion", command=self.toggle_suggestion, font=("Arial", 10))
            self.suggestion_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame to hold translation, suggestion, and romanized text (hidden by default)
        self.extra_frame = tk.Frame(self.frame, bg="#f0f4c3")
        self.extra_frame.pack(fill=tk.X, padx=10, pady=5)

    def toggle_romanized(self):
        """Toggle the visibility of the romanized text."""
        self.romanized_visible = not self.romanized_visible
        if self.romanized_visible:
            self.romanized_button.config(text="Hide Romanized")
            romanized_label = tk.Label(self.extra_frame, text=f"Romanized: {self.romanized}", font=("Arial", 12), bg="#f0f4c3", anchor="w")
            romanized_label.pack(fill=tk.X, padx=10, pady=5)
        else:
            self.romanized_button.config(text="Show Romanized")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()

    def toggle_translation(self):
        """Toggle the visibility of the translation."""
        self.translation_visible = not self.translation_visible
        if self.translation_visible:
            self.translation_button.config(text="Hide Translation")
            translation_label = tk.Label(self.extra_frame, text=f"Translation: {self.translation}", font=("Arial", 12), bg="#f0f4c3", anchor="w")
            translation_label.pack(fill=tk.X, padx=10, pady=5)
        else:
            self.translation_button.config(text="Show Translation")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()

    def toggle_suggestion(self):
        """Toggle the visibility of the suggestion."""
        self.suggestion_visible = not self.suggestion_visible
        if self.suggestion_visible:
            self.suggestion_button.config(text="Hide Suggestion")
            suggestion_label = tk.Label(self.extra_frame, text=f"Suggestion: {self.suggestion}", font=("Arial", 12), bg="#f0f4c3", anchor="w")
            suggestion_label.pack(fill=tk.X, padx=10, pady=5)
        else:
            self.suggestion_button.config(text="Show Suggestion")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Conversation")
        self.root.geometry("600x700")

        # Initialize OpenAI client
        self.client = OpenAI(api_key="sk-eeec58a2eac5449aa147574a2a090a12", base_url="https://api.deepseek.com")

        # Initialize chat history
        self.chat_history = [
            {"role": "system", "content": """
                You are a language learning conversational teacher.
                You are teaching an English speaker to speak Japanese.
                They are at beginner level.
                You should try to respond in Japanese and then explain what was said in English.
                Make sure that you are continuing on the conversation.
                As the student may not have strong Japanese, you should prepare a response for them to say after you speak.

                The output should come in four parts which are identified with keys: 'response_deepseek', 'translation_deepseek', 'suggestion_deepseek', 'romanized_deepseek'.

                Here is an example:
                response_deepseek: こんにちは
                translation_deepseek: Hello
                suggestion_deepseek: How are you?
                romanized_deepseek: Konnichiwa

                Structure the output very carefully so I can parse it in code.
            """}
        ]

        # Language options
        self.languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Italian", "Russian"]

        # Create a frame for language selection
        self.language_frame = tk.Frame(root)
        self.language_frame.pack(padx=10, pady=10, fill=tk.X)

        # Dropdown for native language
        self.native_language_label = tk.Label(self.language_frame, text="Native Language:", font=("Arial", 12))
        self.native_language_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.native_language_var = tk.StringVar()
        self.native_language_dropdown = ttk.Combobox(self.language_frame, textvariable=self.native_language_var, values=self.languages, font=("Arial", 12))
        self.native_language_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
        self.native_language_dropdown.set("Select Native Language")

        # Dropdown for learning language
        self.learning_language_label = tk.Label(self.language_frame, text="Learning Language:", font=("Arial", 12))
        self.learning_language_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.learning_language_var = tk.StringVar()
        self.learning_language_dropdown = ttk.Combobox(self.language_frame, textvariable=self.learning_language_var, values=self.languages, font=("Arial", 12))
        self.learning_language_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
        self.learning_language_dropdown.set("Select Learning Language")

        # Start button
        self.start_button = tk.Button(self.language_frame, text="Start Chat", command=self.start_chat, font=("Arial", 12))
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Create a main frame to hold the chat display and input frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollable canvas for the chat display
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the messages
        self.chat_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        # Bind the canvas to update the scroll region when the chat frame changes size
        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create a frame for the user input and buttons
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)

        # Text entry for user input
        self.user_input = tk.Entry(self.input_frame, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)  # Bind Enter key to send message

        # Send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message, font=("Arial", 12))
        self.send_button.pack(side=tk.LEFT, padx=(10, 0))

        # Clear chat button
        self.clear_button = tk.Button(self.input_frame, text="Clear Chat", command=self.clear_chat, font=("Arial", 12))
        self.clear_button.pack(side=tk.LEFT, padx=(10, 0))

        # Save chat button
        self.save_button = tk.Button(self.input_frame, text="Save Chat", command=self.save_chat, font=("Arial", 12))
        self.save_button.pack(side=tk.LEFT, padx=(10, 0))

        # Initially hide the chat display and input frame
        self.main_frame.pack_forget()
        self.input_frame.pack_forget()

    def start_chat(self):
        """Start the chat after language selection."""
        native_language = self.native_language_var.get()
        learning_language = self.learning_language_var.get()

        if native_language == "Select Native Language" or learning_language == "Select Learning Language":
            messagebox.showwarning("Language Selection", "Please select both your native language and the language you are learning.")
            return

        # Update the system prompt based on the selected languages
        self.chat_history[0]["content"] = f"""
            You are a language learning conversational teacher.
            You are teaching a {native_language} speaker to speak {learning_language}.
            They are at beginner level.
            You should try to respond in {learning_language} and then explain what was said in {native_language}.
            Make sure that you are continuing on the conversation.
            As the student may not have strong {learning_language}, you should prepare a response for them to say after you speak.

            The output should come in four parts which are identified with keys: 'response_deepseek', 'translation_deepseek', 'suggestion_deepseek', 'romanized_deepseek'.

            Here is an example:
            response_deepseek: こんにちは
            translation_deepseek: Hello
            suggestion_deepseek: How are you?
            romanized_deepseek: Konnichiwa

            Structure the output very carefully so I can parse it in code.
        """

        # Hide the language selection frame and show the chat display and input frame
        self.language_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)

    def send_message(self, event=None):
        # Get the user's message
        user_message = self.user_input.get().strip()
        if not user_message:
            return  # Ignore empty messages

        # Display the user's message
        UserMessage(self.chat_frame, user_message)

        # Add the user's message to the chat history
        self.chat_history.append({"role": "user", "content": user_message})

        # Clear the input field
        self.user_input.delete(0, tk.END)

        # Get the chatbot's response
        self.root.after(1000, self.chatbot_response)  # Delay for 1 second

    def parse_response(self, response):
        """Parse the response into different sections."""
        sections = {
            "response_deepseek": "",
            "translation_deepseek": "",
            "suggestion_deepseek": "",
            "romanized_deepseek": ""  # Romanized version of the response
        }

        lines = response.split('\n')
        for line in lines:
            if line.startswith("response_deepseek:"):
                sections["response_deepseek"] = line[len("response_deepseek:"):].strip()
            elif line.startswith("translation_deepseek:"):
                sections["translation_deepseek"] = line[len("translation_deepseek:"):].strip()
            elif line.startswith("suggestion_deepseek:"):
                sections["suggestion_deepseek"] = line[len("suggestion_deepseek:"):].strip()
            elif line.startswith("romanized_deepseek:"):
                sections["romanized_deepseek"] = line[len("romanized_deepseek:"):].strip()

        print("Parsed Sections:", sections)  # Debug print
        return sections

    def chatbot_response(self):
        # Call the OpenAI API to get a response
        try:
            response_stream = self.client.chat.completions.create(
                model="deepseek-chat",  # Use the Deepseek model
                messages=self.chat_history,  # Pass the entire chat history
                stream=True,  # Enable streaming
            )

            assistant_reply = ""

            for chunk in response_stream:
                if chunk.choices[0].delta.content:  # Check if there's content in the chunk
                    token = chunk.choices[0].delta.content
                    assistant_reply += token

            # Add the chatbot's response to the chat history
            self.chat_history.append({"role": "assistant", "content": assistant_reply})

            # Parse the response into sections
            sections = self.parse_response(assistant_reply)

            # Display the chatbot's response
            ChatbotMessage(
                self.chat_frame,
                sections["response_deepseek"],
                "Chatbot",
                translation=sections["translation_deepseek"],
                suggestion=sections["suggestion_deepseek"],
                romanized=sections["romanized_deepseek"]  # Pass romanized text
            )

            # Scroll to the bottom of the chat
            self.canvas.yview_moveto(1.0)

        except Exception as e:
            # Handle errors (e.g., API issues)
            ChatbotMessage(self.chat_frame, f"Error: {str(e)}", "Chatbot")

    def clear_chat(self):
        """Clear the chat display and reset the chat history."""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.chat_history = [
            {"role": "system", "content": """
                You are a language learning conversational teacher.
                You are teaching an English speaker to speak Japanese.
                They are at beginner level.
                You should try to respond in Japanese and then explain what was said in English.
                Make sure that you are continuing on the conversation.
                As the student may not have strong Japanese, you should prepare a response for them to say after you speak.

                The output should come in four parts which are identified with keys: 'response_deepseek', 'translation_deepseek', 'suggestion_deepseek', 'romanized_deepseek'.

                Here is an example:
                response_deepseek: こんにちは
                translation_deepseek: Hello
                suggestion_deepseek: How are you?
                romanized_deepseek: Konnichiwa

                Structure the output very carefully so I can parse it in code.
            """}
        ]

    def save_chat(self):
        # Save the chat history to a file
        try:
            with open("chat_history.txt", "w") as file:
                for message in self.chat_history:
                    file.write(f"{message['role']}: {message['content']}\n")
            messagebox.showinfo("Save Chat", "Chat history saved to chat_history.txt")
        except Exception as e:
            messagebox.showerror("Save Chat", f"Error saving chat: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
