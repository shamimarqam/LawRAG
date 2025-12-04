import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys

# --- Functions ---
# rag_chat_ui.py
import tkinter as tk
from tkinter import scrolledtext
import threading
import importlib

# Import RAG backend dynamically
rag_module = importlib.import_module("rag_local")

def get_rag_response(query):
    answer, docs = rag_module.rag_answer(query, top_k=5)

    # print("\n=== RAG Answer ===\n")
    # print(answer)
    # print("\n=== Sources ===\n")
    response = answer
    for d in docs:
        response = response + f"- {d['source']} (score {d['score']:.4f})"
    response = response + "\n"
    return response


def process_response(user_input):
    """
    Helper function that runs the get_response() function and updates the GUI.
    This runs AFTER the 'thinking...' message has been displayed.
    """
    response_text = get_rag_response(user_input)

    chat_area.config(state=tk.NORMAL)

    chat_area.tag_remove('thinking_indicator', "end-2 lines", "end-1 lines")


    # Display user input and response in the chat area
    chat_area.insert(tk.END, f"Response: {response_text}\n\n", 'bot')
    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

    # Re-enable the send button
    send_button.config(state=tk.NORMAL)


def send_message():
    """
    Initiates the process: displays 'thinking...', disables input, and schedules processing.
    """
    user_input = input_area.get("1.0", tk.END).strip()
    
    if user_input:
        # 1. Disable the send button to prevent multiple clicks
        send_button.config(state=tk.DISABLED)

        # 2. Display the user input immediately
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"You: {user_input}\n", 'user')
        
        # 3. Display the 'thinking...' indicator
        chat_area.insert(tk.END, "Thinking...\n", 'thinking_indicator')
        chat_area.see(tk.END)
        chat_area.config(state=tk.DISABLED)

        # 4. Clear the input area
        input_area.delete("1.0", tk.END)

        # 5. Use 'after' to allow the GUI to update (show the 'thinking...' text) 
        #    before calling the potentially blocking 'get_response' function.
        #    We schedule the 'process_response' function to run in 50ms.
        root.after(50, process_response, user_input)

def reset_app():
    """Resets the chat area and enables inputs."""
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("1.0", tk.END)
    chat_area.config(state=tk.DISABLED)
    input_area.delete("1.0", tk.END)
    send_button.config(state=tk.NORMAL)


def main():
    """Configures and runs the main application window."""
    global root, input_area, chat_area, send_button
    root = tk.Tk()
    root.title("LawRAG")
    root.geometry("600x500")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # --- Scrollable Text Area for Display ---
    chat_area = ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="#616161", font=("Arial", 12))
    chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    chat_area.tag_configure('user', foreground="#B3FFDD")
    chat_area.tag_configure('bot', foreground='#FFFFFF', font=("Arial", 12, "bold"))
    chat_area.tag_configure('thinking_indicator', foreground='gray', font=("Arial", 12, "italic"))


    # --- Input and Buttons Layout ---
    input_frame = tk.Frame(root)
    input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
    input_frame.grid_columnconfigure(0, weight=1)

    input_area = tk.Text(input_frame, height=3, wrap=tk.WORD, font=("Arial", 12))
    input_area.grid(row=0, column=0, sticky="ew", padx=(0, 10))

    button_frame = tk.Frame(input_frame)
    button_frame.grid(row=0, column=1, sticky="nse")

    send_button = tk.Button(button_frame, text="Send", command=send_message, width=10)
    send_button.pack(side=tk.TOP, pady=(0, 5))

    reset_button = tk.Button(button_frame, text="Reset App", command=reset_app, width=10)
    reset_button.pack(side=tk.TOP)

    # Start the application loop
    root.mainloop()

if __name__ == "__main__":
    main()
