import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, simpledialog
from openai import OpenAI
from collections import deque
import os

root = tk.Tk()
root.iconbitmap("stellabot_logo.ico")

# Modern color scheme
BG_COLOR = "#f0f0f0"  # Light gray background
USER_BG = "#d1e8ff"   # Light blue for user messages
BOT_BG = "#e0ffe0"    # Light green for bot messages
BUTTON_BG = "#4CAF50" # Green for buttons
BUTTON_FG = "white"   # White text for buttons
FONT = ("Arial", 15, "bold")  # Modern font
FONT_TOGGLES = ("Arial", 11, "bold")
FONT_MESSAGES = ("Chalkboard", 12, "bold")

api_prompt=f"""
to create deepseek API key https://platform.deepseek.com/api_keys \n
Please enter your deepseek API key:
"""
def get_api_key():
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as file:
            return file.read().strip()
    else:
        api_key = simpledialog.askstring("API Key", api_prompt, parent=root)
        if api_key:
            with open("api_key.txt", "w") as file:
                file.write(api_key)
            return api_key
        else:
            messagebox.showerror("Error", "API key is required to use the app.")
            return None

class UserMessage:
    def __init__(self, parent, message):
        self.parent = parent
        self.message = message
        self.display()

    def display(self):
        """Display the user's message in the chat window."""
        self.frame = tk.Frame(self.parent, bg=BG_COLOR)
        self.frame.pack(fill=tk.X, pady=5, padx=10)

        self.label = tk.Label(
            self.frame,
            text=f"You: {self.message}",
            font=FONT_MESSAGES,
            bg=USER_BG,
            anchor="w",
            wraplength=500,
            justify="left",
            padx=10,
            pady=5,
            relief=tk.RIDGE,
            bd=4
        )
        self.label.pack(fill=tk.X, padx=5, pady=5)

class ChatbotMessage:
    def __init__(self, parent, message, sender="Chatbot", translation=None, suggestion=None, suggestion_translation=None, romanized=None, romanized_suggestion=None, native_language_var=None, learning_language_var=None):
        self.parent = parent
        self.message = message
        self.sender = sender
        self.translation = translation
        self.suggestion = suggestion
        self.suggestion_translation = suggestion_translation
        self.romanized = romanized
        self.romanized_suggestion = romanized_suggestion
        self.native_language_var = native_language_var
        self.learning_language_var = learning_language_var
        self.translation_visible = False
        self.suggestion_visible = False
        self.suggestion_translation_visible = False
        self.romanized_suggestion_visible = False
        self.romanized_visible = False

        self.display()

    def display(self):
        """Display the chatbot's message in the chat window with optional buttons."""
        self.frame = tk.Frame(self.parent, bg=BG_COLOR)
        self.frame.pack(fill=tk.X, pady=5, padx=10)

        # Message label
        self.message_label = tk.Label(
            self.frame,
            text=f"{self.sender}: {self.message}",
            font=FONT_MESSAGES,
            bg=BOT_BG,
            anchor="w",
            wraplength=500,
            justify="left",
            padx=10,
            pady=5,
            relief=tk.RIDGE,
            bd=4
        )
        self.message_label.pack(fill=tk.X, padx=5, pady=5)

        # Button to toggle romanized text (if available)
        if self.romanized:
            self.romanized_button = tk.Button(
                self.frame,
                text="Show Romanized",
                command=self.toggle_romanized,
                font=FONT_TOGGLES,
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                relief=tk.RAISED,
                bd=3
            )
            self.romanized_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Button to toggle translation
        if self.translation:
            self.translation_button = tk.Button(
                self.frame,
                text="Show Translation",
                command=self.toggle_translation,
                font=FONT_TOGGLES,
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                relief=tk.RAISED,
                bd=3
            )
            self.translation_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Button to toggle suggestion
        if self.suggestion:
            self.suggestion_button = tk.Button(
                self.frame,
                text=f"Show Suggestion ({self.learning_language_var})",
                command=self.toggle_suggestion,
                font=FONT_TOGGLES,
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                relief=tk.RAISED,
                bd=3
            )
            self.suggestion_button.pack(side=tk.LEFT, padx=5, pady=5)

        if self.romanized_suggestion:
            self.romanized_suggestion_button = tk.Button(
                self.frame,
                text=f"Show Romanized Suggestion",
                command=self.toggle_romanized_suggestion,
                font=FONT_TOGGLES,
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                relief=tk.RAISED,
                bd=3
            )
            self.romanized_suggestion_button.pack(side=tk.LEFT, padx=5, pady=5)

        if self.suggestion_translation:
            self.suggestion_translation_button = tk.Button(
                self.frame,
                text=f"Show Suggestion ({self.native_language_var})",
                command=self.toggle_suggestion_translation,
                font=FONT_TOGGLES,
                bg=BUTTON_BG,
                fg=BUTTON_FG,
                relief=tk.RAISED,
                bd=3
            )
            self.suggestion_translation_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame to hold translation, suggestion, and romanized text (hidden by default)
        self.extra_frame = tk.Frame(self.frame, bg=BG_COLOR)
        self.extra_frame.pack(fill=tk.X, padx=10, pady=5)

    def toggle_romanized(self):
        """Toggle the visibility of the romanized text."""
        self.romanized_visible = not self.romanized_visible
        if self.romanized_visible:
            self.romanized_button.config(text="Hide Romanized")
            romanized_label = tk.Label(
                self.extra_frame,
                text=f"Romanized: {self.romanized}",
                font=FONT_MESSAGES,
                bg=BOT_BG,
                anchor="w",
                wraplength=500,
                justify="left",
                padx=10,
                pady=5,
                relief=tk.RIDGE,
                bd=2
            )
            romanized_label.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.romanized_button.config(text="Show Romanized")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()

    def toggle_translation(self):
        """Toggle the visibility of the translation."""
        self.translation_visible = not self.translation_visible
        if self.translation_visible:
            self.translation_button.config(text="Hide Translation")
            translation_label = tk.Label(
                self.extra_frame,
                text=f"Translation: {self.translation}",
                font=FONT_MESSAGES,
                bg=BOT_BG,
                anchor="w",
                wraplength=500,
                justify="left",
                padx=10,
                pady=5,
                relief=tk.RIDGE,
                bd=2
            )
            translation_label.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.translation_button.config(text="Show Translation")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()

    def toggle_romanized_suggestion(self):
        """Toggle the visibility of the romanized suggestion."""
        self.romanized_suggestion_visible = not self.romanized_suggestion_visible #
        if self.romanized_suggestion_visible:
            self.romanized_suggestion_button.config(text=f"Hide Romanized Suggestion")
            romanized_suggestion_label = tk.Label(
                self.extra_frame,
                text=f"Suggestion: {self.romanized_suggestion}",
                font=FONT_MESSAGES,
                bg=BOT_BG,
                anchor="w",
                wraplength=500,
                justify="left",
                padx=10,
                pady=5,
                relief=tk.RIDGE,
                bd=2
            )
            romanized_suggestion_label.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.romanized_suggestion_button.config(text=f"Show Romanized Suggestion")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()

    def toggle_suggestion(self):
        self.suggestion_visible = not self.suggestion_visible
        if self.suggestion_visible:
            self.suggestion_button.config(text=f"Hide Suggestion ({self.learning_language_var})")
            suggestion_label = tk.Label(
                self.extra_frame,
                text=f"Suggestion: {self.suggestion}",
                font=FONT_MESSAGES,
                bg=BOT_BG,
                anchor="w",
                wraplength=500,
                justify="left",
                padx=10,
                pady=5,
                relief=tk.RIDGE,
                bd=2
            )
            suggestion_label.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.suggestion_button.config(text=f"Show Suggestion ({self.learning_language_var})")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()

    def toggle_suggestion_translation(self):
        self.suggestion_translation_visible = not self.suggestion_translation_visible
        if self.suggestion_translation_visible:
            self.suggestion_translation_button.config(text=f"Hide Suggestion ({self.native_language_var})")
            suggestion_translation_label = tk.Label(
                self.extra_frame,
                text=f"Suggestion: {self.suggestion_translation}",
                font=FONT_MESSAGES,
                bg=BOT_BG,
                anchor="w",
                wraplength=500,
                justify="left",
                padx=10,
                pady=5,
                relief=tk.RIDGE,
                bd=2
            )
            suggestion_translation_label.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.suggestion_translation_button.config(text=f"Show Suggestion ({self.native_language_var})")
            for widget in self.extra_frame.winfo_children():
                widget.destroy()


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Conversation")
        self.root.geometry("600x700")
        self.root.configure(bg=BG_COLOR)
        self.api_key = get_api_key()

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

        self.native_language_var = "English"
        self.learning_language_var = "Chinese"


        # Initialize chat history
        self.chat_history = deque(maxlen=13)
        self.chat_record = []
        # Language options
        self.languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Italian", "Irish"]

        # Create a frame for language selection
        self.language_frame = tk.Frame(root, bg=BG_COLOR)
        self.language_frame.pack(padx=10, pady=10, fill=tk.X)

        # Dropdown for native language
        self.native_language_label = tk.Label(self.language_frame, text="Native Language:", font=FONT, bg=BG_COLOR)
        self.native_language_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.native_language_var = tk.StringVar()
        self.native_language_dropdown = ttk.Combobox(self.language_frame, textvariable=self.native_language_var, values=self.languages, font=FONT)
        self.native_language_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
        self.native_language_dropdown.set("Select Native Language")

        self.chat_base_instructions = {
            "role": "system",
            "content": f"""
                You are a language learning conversational teacher.
                You are teaching an {self.native_language_var} speaker to speak {self.learning_language_var}.
                They are at beginner level.
                You should try to respond in {self.learning_language_var} and then explain what was said in {self.native_language_var}.
                Make sure that you are continuing on the conversation.
                As the student may not have strong {self.learning_language_var}, you should prepare a response for them to say after you speak.

                The output should come in six parts which are identified with keys: 'response_deepseek', 'translation_deepseek', 'suggestion_deepseek', 'suggestion_translation_deepseek', 'romanized_deepseek', 'romanized_suggestion'.
                The order is important.

                Here is an example of how it looks and you must do it in {self.learning_language_var}:
                'response_deepseek: this is the response in {self.learning_language_var}.
                translation_deepseek: this is the translation in {self.native_language_var}.
                suggestion_deepseek: this is the suggestion for the next message in {self.learning_language_var}.
                suggestion_translation_deepseek: this is the translation of the suggestion in {self.native_language_var}
                romanized_deepseek: this is the romanized version of your response.
                romanized_suggestion: this is the romanized version of the suggestion.'

                Structure the output very carefully so I can parse it in code. The order is important.
            """
        }

        # Dropdown for learning language
        self.learning_language_label = tk.Label(self.language_frame, text="Learning Language:", font=FONT, bg=BG_COLOR)
        self.learning_language_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.learning_language_var = tk.StringVar()
        self.learning_language_dropdown = ttk.Combobox(self.language_frame, textvariable=self.learning_language_var, values=self.languages, font=FONT)
        self.learning_language_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
        self.learning_language_dropdown.set("Select Learning Language")

        # Start button
        self.start_button = tk.Button(
            self.language_frame,
            text="Start Chat",
            command=self.start_chat,
            font=FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            relief=tk.RAISED,
            bd=2
        )
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Create a main frame to hold the chat display and input frame
        self.main_frame = tk.Frame(root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollable canvas for the chat display
        self.canvas = tk.Canvas(self.main_frame, bg=BG_COLOR)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the messages
        self.chat_frame = tk.Frame(self.canvas, bg=BG_COLOR)
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        # Bind the canvas to update the scroll region when the chat frame changes size
        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Typing indicator label
        self.typing_indicator = tk.Label(
            self.chat_frame,
            text="",
            font=FONT,
            bg=BG_COLOR,
            fg="gray",
            anchor="w",
            padx=10,
            pady=5
        )
        self.typing_indicator.pack(fill=tk.X, padx=5, pady=5)

        # Create a frame for the user input and buttons
        self.input_frame = tk.Frame(root, bg=BG_COLOR)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)

        # Text entry for user input
        self.user_input = tk.Entry(self.input_frame, font=FONT)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.user_input.bind("<Return>", self.send_message)  # Bind Enter key to send message

        # Send button
        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            font=FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            relief=tk.RAISED,
            bd=2
        )
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Clear chat button
        self.clear_button = tk.Button(
            self.input_frame,
            text="Clear Chat",
            command=self.clear_chat,
            font=FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            relief=tk.RAISED,
            bd=2
        )
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Save chat button
        self.save_button = tk.Button(
            self.input_frame,
            text="Save Chat",
            command=self.save_chat,
            font=FONT,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            relief=tk.RAISED,
            bd=2
        )
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Initially hide the chat display and input frame
        self.main_frame.pack_forget()
        self.input_frame.pack_forget()

        # Typing animation control
        self.typing_animation_id = None



    def start_typing_animation(self):
        """Start the typing animation."""
        self.typing_indicator.config(text="Typing.")
        self.typing_animation_id = self.root.after(500, self.update_typing_animation)

    def update_typing_animation(self):
        """Update the typing animation."""
        current_text = self.typing_indicator.cget("text")
        if current_text.endswith("..."):
            self.typing_indicator.config(text="Typing.")
        else:
            self.typing_indicator.config(text=current_text + ".")
        self.typing_animation_id = self.root.after(500, self.update_typing_animation)

    def stop_typing_animation(self):
        """Stop the typing animation."""
        if self.typing_animation_id:
            self.root.after_cancel(self.typing_animation_id)
            self.typing_animation_id = None
        self.typing_indicator.config(text="")

    def start_chat(self):
        """Start the chat after language selection."""
        native_language = self.native_language_var.get()
        learning_language = self.learning_language_var.get()

        if native_language == "Select Native Language" or learning_language == "Select Learning Language":
            messagebox.showwarning("Language Selection", "Please select both your native language and the language you are learning.")
            return

        # Update the system prompt based on the selected languages
        self.chat_base_instructions["content"] = f"""
                You are a language learning conversational teacher.
                You are teaching an {self.native_language_var} speaker to speak {self.learning_language_var}.
                They are at beginner level.
                You should try to respond in {self.learning_language_var} and then explain what was said in {self.native_language_var}.
                Make sure that you are continuing on the conversation.
                As the student may not have strong {self.learning_language_var}, you should prepare a response for them to say after you speak.

                The output should come in six parts which are identified with keys: 'response_deepseek', 'translation_deepseek', 'suggestion_deepseek', 'suggestion_translation_deepseek', 'romanized_deepseek', 'romanized_suggestion'.
                The order is important.

                Here is an example of how it looks and you must do it in {self.learning_language_var}:
                'response_deepseek: this is the response in {self.learning_language_var}.
                translation_deepseek: this is the translation in {self.native_language_var}.
                suggestion_deepseek: this is the suggestion for the next message in {self.learning_language_var}.
                suggestion_translation_deepseek: this is the translation of the suggestion in {self.native_language_var}
                romanized_deepseek: this is the romanized version of your response.
                romanized_suggestion: this is the romanized version of the suggestion.'

                Structure the output very carefully so I can parse it in code. The order is important.
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

        # Start the typing animation
        self.start_typing_animation()

        # Get the chatbot's response
        self.root.after(1000, self.chatbot_response)  # Delay for 1 second

    def parse_response(self, response):
        """Parse the response into different sections."""
        sections = {
            "response_deepseek": "",
            "translation_deepseek": "",
            "suggestion_deepseek": "",
            "suggestion_translation_deepseek": "",
            "romanized_deepseek": "",
            "romanized_suggestion": ""
        }

        lines = response.split('\n')
        response_deepseek_line_index = 0
        translation_deepseek = 0
        suggestion_deepseek = 0
        romanized_deepseek = 0
        romanized_suggestion = 0
        suggestion_translation_deepseek = 0
        for index in range(len(lines)):
            if lines[index].startswith("response_deepseek:"):
                response_deepseek_line_index = index
            elif lines[index].startswith("translation_deepseek:"):
                translation_deepseek = index
            elif lines[index].startswith("suggestion_deepseek:"):
                suggestion_deepseek = index
            elif lines[index].startswith("suggestion_translation_deepseek:"):
                suggestion_translation_deepseek = index
            elif lines[index].startswith("romanized_deepseek:"):
                romanized_deepseek = index
            elif lines[index].startswith("romanized_suggestion:"):
                romanized_suggestion = index

        sections["response_deepseek"] = " ".join(lines[response_deepseek_line_index:translation_deepseek])[len("response_deepseek:"):].strip()
        sections["translation_deepseek"] = " ".join(lines[translation_deepseek:suggestion_deepseek])[len("translation_deepseek:"):].strip()
        sections["suggestion_deepseek"] = " ".join(lines[suggestion_deepseek:suggestion_translation_deepseek])[len("suggestion_deepseek:"):].strip()
        sections["suggestion_translation"] = " ".join(lines[suggestion_translation_deepseek:romanized_deepseek])[len("suggestion_translation_deepseek:"):].strip()
        sections["romanized_deepseek"] = " ".join(lines[romanized_deepseek:romanized_suggestion])[len("romanized_deepseek:"):].strip()
        sections["romanized_suggestion"] = " ".join(lines[romanized_suggestion:])[len("romanized_suggestion:"):].strip()

        #print("Parsed Sections:", sections)  # Debug print
        return sections

    def chatbot_response(self):
        self.chat_record = self.chat_record + [self.chat_base_instructions] + list(self.chat_history)

        chat_instruct_plus_history = [self.chat_base_instructions] + list(self.chat_history)

        # Call the OpenAI API to get a response
        try:
            response_stream = self.client.chat.completions.create(
                model="deepseek-chat",  # Use the Deepseek model
                messages=chat_instruct_plus_history,  # Pass the entire chat history
                stream=True,  # Enable streaming,
            )

            assistant_reply = ""

            for chunk in response_stream:
                if chunk.choices[0].delta.content:  # Check if there's content in the chunk
                    token = chunk.choices[0].delta.content
                    assistant_reply += token

            # Stop the typing animation
            self.stop_typing_animation()

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
                suggestion_translation=sections["suggestion_translation"],
                romanized=sections["romanized_deepseek"],
                romanized_suggestion=sections["romanized_suggestion"],
                native_language_var=self.native_language_var.get(),
                learning_language_var=self.learning_language_var.get()
            )

            # Scroll to the bottom of the chat
            self.canvas.yview_moveto(1.0)

        except Exception as e:
            # Stop the typing animation in case of an error
            self.stop_typing_animation()

            # Handle errors (e.g., API issues)
            ChatbotMessage(self.chat_frame, f"Error: {str(e)}", "Chatbot")

    def clear_chat(self):
        """Clear the chat display and reset the chat history."""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.chat_base_instructions = {
            "role": "system",
            "content": f"""
                You are a language learning conversational teacher.
                You are teaching an {self.native_language_var} speaker to speak {self.learning_language_var}.
                They are at beginner level.
                You should try to respond in {self.learning_language_var} and then explain what was said in {self.native_language_var}.
                Make sure that you are continuing on the conversation.
                As the student may not have strong {self.learning_language_var}, you should prepare a response for them to say after you speak.

                The output should come in six parts which are identified with keys: 'response_deepseek', 'translation_deepseek', 'suggestion_deepseek', 'suggestion_translation_deepseek', 'romanized_deepseek', 'romanized_suggestion'.
                The order is important.

                Here is an example of how it looks and you must do it in {self.learning_language_var}:
                'response_deepseek: this is the response in {self.learning_language_var}.
                translation_deepseek: this is the translation in {self.native_language_var}.
                suggestion_deepseek: this is the suggestion for the next message in {self.learning_language_var}.
                suggestion_translation_deepseek: this is the translation of the suggestion in {self.native_language_var}
                romanized_deepseek: this is the romanized version of your response.
                romanized_suggestion: this is the romanized version of the suggestion.'

                Structure the output very carefully so I can parse it in code. The order is important.
            """
        }
        self.chat_history = deque(maxlen=13)

    def save_chat(self):
        # Save the chat history to a file
        try:
            with open("chat_history.txt", "w", encoding="utf-8") as file:  # Specify utf-8 encoding
                for message in self.chat_record:
                    file.write(f"{message['role']}: {message['content']}\n")
            messagebox.showinfo("Save Chat", "Chat history saved to chat_history.txt")
        except Exception as e:
            messagebox.showerror("Save Chat", f"Error saving chat: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    api_key = get_api_key()
    root.mainloop()
