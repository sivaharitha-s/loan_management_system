import pymysql
from datetime import datetime
from tkinter import Tk, Button, ttk, Frame, Entry, Label, Toplevel
from tkinter.messagebox import showinfo, showerror, askyesno
import subprocess
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='haritha10142307',
    database='new_loan',
    cursorclass=pymysql.cursors.DictCursor
)

def fetch_loan_data(search_query=None):
    cursor = connection.cursor()
    if search_query:
        query = """
            SELECT * FROM loan
            WHERE 
                loan_id LIKE %s OR 
                borrower_id LIKE %s OR 
                borrower_name LIKE %s OR 
                phone_no LIKE %s OR 
                address LIKE %s OR 
                loan_type LIKE %s OR 
                loan_amount LIKE %s OR 
                interest LIKE %s OR 
                long_term LIKE %s OR 
                start_date LIKE %s OR 
                end_date LIKE %s OR 
                loan_status LIKE %s
        """
        like_query = f"%{search_query}%"
        cursor.execute(query, (
            like_query, like_query, like_query, like_query, like_query,
            like_query, like_query, like_query, like_query, like_query,
            like_query, like_query
        ))
    else:
        cursor.execute("SELECT * FROM loan")
    loans = cursor.fetchall()
    cursor.close()
    return loans

def refresh_table():
    load_table(search_entry.get())

def load_table(search_query=None):
    loans = fetch_loan_data(search_query)
    for row in tree.get_children():
        tree.delete(row)
    for loan in loans:
        tree.insert('', 'end', values=(
            loan['loan_id'], loan['borrower_id'], loan['borrower_name'], loan['phone_no'],
            loan['address'], loan['loan_type'], loan['loan_amount'], loan['interest'],
            loan['long_term'], loan['start_date'], loan['end_date'], loan['loan_status']
        ))

def delete_selected_loans():
    selected_items = tree.selection()
    if not selected_items:
        showerror("Selection Error", "Please select at least one row to delete.")
        return

    confirm = askyesno("Confirm Deletion", "Are you sure you want to delete the selected rows?")
    if confirm:
        cursor = connection.cursor()
        for item in selected_items:
            loan_id = tree.item(item, 'values')[0]
            cursor.execute("DELETE FROM loan WHERE loan_id = %s", (loan_id,))
        connection.commit()
        cursor.close()
        showinfo("Deletion Successful", "Selected loan records have been deleted.")
        load_table()

def update_selected_loans():
    selected_items = tree.selection()
    if not selected_items:
        showerror("Selection Error", "Please select at least one row to update.")
        return

    loan_id = tree.item(selected_items[0], 'values')[0]
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM loan WHERE loan_id = %s", (loan_id,))
    loan = cursor.fetchone()
    cursor.close()

    update_window = Toplevel(root)
    update_window.title(f"Update Loan ID: {loan_id}")
    update_window.geometry("400x700")

    fields = {
        'Borrower ID': 'borrower_id', 'Borrower Name': 'borrower_name', 'Phone No': 'phone_no',
        'Address': 'address', 'Loan Type': 'loan_type', 'Loan Amount': 'loan_amount',
        'Interest Rate': 'interest', 'Loan Term': 'long_term', 'Start Date': 'start_date',
        'End Date': 'end_date', 'Loan Status': 'loan_status'
    }

    entries = {}
    for i, (label_text, column_name) in enumerate(fields.items()):
        Label(update_window, text=label_text).pack(pady=5)
        entry = Entry(update_window)
        entry.insert(0, loan[column_name])
        entry.pack(pady=5)
        entries[column_name] = entry

    def save_changes():
        updates = {column: entry.get() for column, entry in entries.items()}
        if any(not value for value in updates.values()):
            showerror("Input Error", "Please fill all the fields.")
            return
        cursor = connection.cursor()
        cursor.execute(""" 
            UPDATE loan
            SET borrower_id = %(borrower_id)s, borrower_name = %(borrower_name)s, phone_no = %(phone_no)s,
                address = %(address)s, loan_type = %(loan_type)s, loan_amount = %(loan_amount)s,
                interest = %(interest)s, long_term = %(long_term)s, start_date = %(start_date)s,
                end_date = %(end_date)s, loan_status = %(loan_status)s
            WHERE loan_id = %(loan_id)s
        """, {**updates, 'loan_id': loan_id})
        connection.commit()
        cursor.close()

        showinfo("Update Successful", "Loan record has been updated.")
        update_window.destroy()
        load_table()

    Button(update_window, text="Save Changes", command=save_changes, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(pady=20)

def open_insert_script():
    subprocess.Popen(['python', '1insert.py'])
    root.after(1000, load_table)

def open_generate_details_script():
    subprocess.Popen(['python', '1gen_details.py'])

root = Tk()
root.title("Financial Transactions")
root.geometry("1200x600")
style = ttk.Style()
style.configure("Treeview", rowheight=20, font=('Arial', 10))
style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
frame = Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)
search_frame = Frame(root, pady=5)
search_frame.pack(fill="x")
Label(search_frame, text="Search:", font=('Arial', 10, 'bold')).pack(side="left", padx=10)
search_entry = Entry(search_frame, font=('Arial', 10))
search_entry.pack(side="left", fill="x", expand=True, padx=5)

Button(search_frame, text="Search", command=refresh_table, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side="left", padx=10)
Button(search_frame, text="Refresh", command=lambda: load_table(), bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side="left", padx=10)
columns = [
    "loan_id", "borrower_id", "borrower_name", "phone_no", "address", 
    "loan_type", "loan_amount", "interest", "long_term", "start_date", 
    "end_date", "loan_status"
]
tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse', height=8)
tree.pack(fill="both", expand=True)
column_widths = {
    "loan_id": 50, "borrower_id": 50, "borrower_name": 100, "phone_no": 100,
    "address": 150, "loan_type": 80, "loan_amount": 100, "interest": 80,
    "long_term": 80, "start_date": 100, "end_date": 100, "loan_status": 80
}
for col, width in column_widths.items():
    tree.heading(col, text=col.replace("_", " ").title())
    tree.column(col, width=width, anchor='center')
button_frame = Frame(root)
button_frame.pack(pady=10)
Button(button_frame, text="Insert New Loan", command=open_insert_script, bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=5)
Button(button_frame, text="Generate Loan Details", command=open_generate_details_script, bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=2, padx=5)
Button(button_frame, text="Delete Loan", command=delete_selected_loans, bg='#F44336', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=3, padx=5)
Button(button_frame, text="Update Loan", command=update_selected_loans, bg='#FF9800', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=5)
load_table()
root.mainloop()
