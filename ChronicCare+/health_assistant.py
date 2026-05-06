import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class HealthAssistant:
    def _init_(self):
        self.window = tk.Tk()
        self.window.title("Health Assistant AI")
        self.window.geometry("600x800")
        
        # Configure style
        style = ttk.Style()
        style.configure("Bot.TLabel", background="#f0f0f0", padding=10)
        style.configure("User.TLabel", background="#007bff", foreground="white", padding=10)
        
        # Create main container
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create chat display
        self.chat_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=30)
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create input field
        self.input_field = ttk.Entry(input_frame)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Create send button
        send_button = ttk.Button(input_frame, text="Send", command=self.handle_input)
        send_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send message
        self.input_field.bind("<Return>", lambda e: self.handle_input())
        
        # Add disclaimer
        disclaimer = ttk.Label(main_frame, text="This AI assistant provides general health information only.\nAlways consult with healthcare professionals for medical advice.",
                             wraplength=580, justify="center", foreground="gray")
        disclaimer.pack(pady=10)
        
        # Initialize with welcome message
        self.display_message("Hello! I'm your personal health assistant. How can I help you today?", is_user=False)

    def handle_input(self):
        user_input = self.input_field.get().strip()
        if user_input:
            self.display_message(user_input, is_user=True)
            response = self.get_response(user_input)
            self.display_message(response, is_user=False)
            self.input_field.delete(0, tk.END)

    def display_message(self, message, is_user):
        timestamp = datetime.now().strftime("%H:%M:%S")
        sender = "You" if is_user else "Bot"
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.see(tk.END)
        
        # Apply different colors for user and bot messages
        last_line_start = self.chat_display.get("end-2c linestart", "end-1c")
        tag_name = f"message_{self.chat_display.index('end-1c')}"
        self.chat_display.tag_add(tag_name, f"end-{len(last_line_start)+1}c linestart", "end-1c")
        
        if is_user:
            self.chat_display.tag_config(tag_name, background="#007bff", foreground="white")
        else:
            self.chat_display.tag_config(tag_name, background="#f0f0f0")

    def get_response(self, message):
        message = message.lower()
        
        # Health-related responses
        responses = {
            'exercise': "Regular exercise is crucial for maintaining good health. Aim for at least 150 minutes of moderate activity or 75 minutes of vigorous activity per week.",
            'diet': "A balanced diet should include plenty of fruits, vegetables, whole grains, lean proteins, and healthy fats. Stay hydrated by drinking plenty of water.",
            'sleep': "Adults should aim for 7-9 hours of quality sleep per night. Maintain a consistent sleep schedule and create a relaxing bedtime routine.",
            'stress': "Managing stress is important for overall health. Try meditation, deep breathing exercises, regular physical activity, or talking to someone you trust.",
            'headache': "Common headache remedies include rest, hydration, and over-the-counter pain relievers. If headaches are severe or frequent, consult a healthcare provider.",
            'default': "I'm here to help with general health questions. However, please consult a healthcare professional for specific medical advice."
        }
        
        # Check for keywords in the message
        if 'exercise' in message or 'workout' in message:
            return responses['exercise']
        elif 'diet' in message or 'food' in message or 'eat' in message:
            return responses['diet']
        elif 'sleep' in message or 'tired' in message:
            return responses['sleep']
        elif 'stress' in message or 'anxiety' in message:
            return responses['stress']
        elif 'headache' in message or 'pain' in message:
            return responses['headache']
        
        return responses['default']

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = HealthAssistant()
    app.run()