import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import sqlite3

# Set up the database to store customer data
conn = sqlite3.connect('customer_issues.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        issue TEXT NOT NULL,
        solution TEXT
    )
''')
conn.commit()

# Simple ML model setup (dummy model)
vectorizer = CountVectorizer()
classifier = MultinomialNB()

# Train the model with some example data
# For simplicity, we use fixed examples
X_train = vectorizer.fit_transform(["not working", "broken", "error", "bug", "slow"])
y_train = ["Reboot the system", "Replace the component", "Check the logs", "Update software", "Upgrade hardware"]
classifier.fit(X_train, y_train)

# Function to handle the submit button click
def submit_details():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    issue = issue_entry.get("1.0", tk.END)
    
    if not name or not email or not phone or not issue.strip():
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    
    # Predict the solution using the ML model
    X_new = vectorizer.transform([issue.strip()])
    predicted_solution = classifier.predict(X_new)[0]
    
    # Store customer details and predicted solution
    c.execute('''
        INSERT INTO customers (name, email, phone, issue, solution)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, issue.strip(), predicted_solution))
    conn.commit()
    
    # Show the predicted solution to the user
    messagebox.showinfo("Solution", f"Suggested Solution: {predicted_solution}")
    
    # Clear the input fields
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    issue_entry.delete("1.0", tk.END)

# Set up the GUI
root = tk.Tk()
root.title("Suhail Nawaz - Customer Support Chatbot")

tk.Label(root, text="Name:").grid(row=0, column=0, sticky=tk.W)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Email:").grid(row=1, column=0, sticky=tk.W)
email_entry = tk.Entry(root)
email_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Phone No:").grid(row=2, column=0, sticky=tk.W)
phone_entry = tk.Entry(root)
phone_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Describe your issue:").grid(row=3, column=0, sticky=tk.W)
issue_entry = tk.Text(root, height=5, width=40)
issue_entry.grid(row=3, column=1, padx=10, pady=5)

submit_button = tk.Button(root, text="Submit", command=submit_details)
submit_button.grid(row=4, columnspan=2, pady=10)

root.mainloop()

# Close the database connection when done
conn.close()
