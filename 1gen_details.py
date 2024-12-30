import tkinter as tk
from tkinter import messagebox
import pymysql
from datetime import datetime
import subprocess

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='haritha10142307',
    database='new_loan'
)

def go_to_home():
    root.destroy()
    subprocess.run(['python', '1front.py'])

def fetch_loan_details():
    identifier_value = entry_id_or_name.get()
    identifier_type = var_identifier_type.get()

    if not identifier_value:
        messagebox.showwarning("Input Error", "Please enter a loan ID or borrower name.")
        return

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    if identifier_type == "loan_id":
        query = "SELECT * FROM loan WHERE loan_id = %s"
    elif identifier_type == "borrower_name":
        query = "SELECT * FROM loan WHERE borrower_name = %s"
    else:
        messagebox.showerror("Error", "Invalid identifier type selected.")
        return

    cursor.execute(query, (identifier_value,))
    loan = cursor.fetchone()
    cursor.close()

    if loan:
        loan_amount = loan['loan_amount']
        interest_rate = loan['interest']
        loan_startdate = datetime.strptime(str(loan['start_date']), "%Y-%m-%d")
        loan_enddate = datetime.strptime(str(loan['end_date']), "%Y-%m-%d")
        total_months = loan['long_term']
        monthly_interest = (loan_amount * interest_rate / 100) / 12
        total_interest = monthly_interest * total_months
        monthly_payment = (loan_amount / total_months) + monthly_interest
        total_payment = monthly_payment * total_months
        label_result.config(text=(
            f"Loan Details:\n"
            f"Loan ID          : {loan['loan_id']}\n"
            f"Borrower ID      : {loan['borrower_id']}\n"
            f"Borrower Name    : {loan['borrower_name']}\n"
            f"Phone Number     : {loan['phone_no']}\n"
            f"Address          : {loan['address']}\n"
            f"Loan Type        : {loan['loan_type']}\n"
            f"Loan Amount      : ₹{loan_amount:.2f}\n"
            f"Interest Rate    : {interest_rate}%\n"
            f"Loan Duration    : {total_months} months\n"
            f"Monthly Interest : ₹{monthly_interest:.2f}\n"
            f"Total Interest   : ₹{total_interest:.2f}\n"
            f"Monthly Payment  : ₹{monthly_payment:.2f}\n"
            f"Loan Status      : {loan['loan_status']}\n"
            f"Total Payment    : ₹{total_payment:.2f}\n"
        ))
    else:
        messagebox.showinfo("No Record", "No record found for the provided identifier.")

def close_connection():
    try:
        if connection and connection.open:
            connection.close()
    except Exception as e:
        print(f"Error while closing connection: {e}")
    finally:
        root.destroy()

root = tk.Tk()
root.title("Loan Details Viewer")
root.geometry("600x600")
root.configure(bg="#f2f2f2")

label_font = ("Arial", 14, "bold")
entry_font = ("Arial", 12)
result_font = ("Arial", 12)

frame_input = tk.Frame(root, bg="#f2f2f2", bd=2, relief="groove")
frame_input.pack(pady=20, padx=20, fill="x")

label_header = tk.Label(frame_input, text="Enter Loan ID or Borrower Name", font=label_font, bg="#f2f2f2")
label_header.grid(row=0, column=0, columnspan=2, pady=10)

var_identifier_type = tk.StringVar(value="loan_id")
radio_loan_id = tk.Radiobutton(frame_input, text="Loan ID", variable=var_identifier_type, value="loan_id", font=entry_font, bg="#f2f2f2")
radio_loan_id.grid(row=1, column=0, padx=5)
radio_borrower_name = tk.Radiobutton(frame_input, text="Borrower Name", variable=var_identifier_type, value="borrower_name", font=entry_font, bg="#f2f2f2")
radio_borrower_name.grid(row=1, column=1, padx=5)

entry_id_or_name = tk.Entry(frame_input, width=35, font=entry_font)
entry_id_or_name.grid(row=2, column=0, columnspan=2, pady=10)

button_fetch = tk.Button(frame_input, text="Fetch Details", command=fetch_loan_details, font=label_font, bg="#4CAF50", fg="white")
button_fetch.grid(row=3, column=0, columnspan=2, pady=10)

frame_result = tk.Frame(root, bg="white", bd=2, relief="sunken")
frame_result.pack(pady=10, padx=20, fill="both", expand=True)

label_result = tk.Label(frame_result, text="", justify="left", font=result_font, anchor="w", bg="white")
label_result.pack(pady=10, padx=10, fill="both", expand=True)

button_back = tk.Button(root, text="Back to Home", command=go_to_home, font=label_font, bg="#4CAF50", fg="white")
button_back.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", close_connection)
root.mainloop()


