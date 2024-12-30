import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pymysql
import subprocess 
def connect_db():
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="haritha10142307", 
            database="new_loan"   
        )
        return db
    except pymysql.MySQLError as err:
        messagebox.showerror("Connection Error", f"Database connection failed: {err}")
        return None

class LoanApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Loan Application")
        self.master.configure(bg="#f0f8ff") 
        self.master.geometry("500x700") 
        self.input_frame = tk.Frame(master, bg="#f0f8ff")
        self.input_frame.pack(pady=20)
        labels = [
            "Borrower ID",        
            "Borrower Name", 
            "Phone Number", 
            "Address", 
            "Loan Type", 
            "Loan Amount", 
            "Interest Rate", 
            "Loan Term (Months)", 
            "Loan Start Date (YYYY-MM-DD)", 
            "Loan End Date (YYYY-MM-DD)", 
            "Loan Status", 
        ]
        self.entries = []  
        for i, label in enumerate(labels):
            tk.Label(self.input_frame, text=label, bg="#f0f8ff", fg="#4B0082", font=("Arial", 15)).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = tk.Entry(self.input_frame, width=40, bg="#ffffff", fg="#000000", borderwidth=2, font=("Arial", 15))
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries.append(entry)  
        (self.borrower_id_entry, self.name_entry, self.phoneno_entry, self.address_entry, 
         self.loan_type_entry, self.amount_entry, self.interest_entry, self.term_entry, 
         self.startdate_entry, self.enddate_entry, self.status_entry) = self.entries
        self.submit_button = tk.Button(master, text="Submit", command=self.insert_loan, bg="#4CAF50", fg="#ffffff", font=("Arial", 15, "bold"))
        self.submit_button.pack(pady=10)
        self.back_button = tk.Button(master, text="Back to Home", command=self.go_back_home, bg="#FF6347", fg="#ffffff", font=("Arial", 15, "bold"))
        self.back_button.pack(pady=10)

    def insert_loan(self):
        borrower_id = self.borrower_id_entry.get()
        borrower_name = self.name_entry.get()
        borrower_phoneno = self.phoneno_entry.get()
        borrower_address = self.address_entry.get()
        loan_type = self.loan_type_entry.get()
        loan_amount = self.amount_entry.get()
        interest_rate = self.interest_entry.get()
        long_term = self.term_entry.get()
        loan_startdate = self.startdate_entry.get()
        loan_enddate = self.enddate_entry.get()
        loan_status = self.status_entry.get()

        try:
            borrower_id = int(borrower_id)  
            loan_amount = float(loan_amount)
            interest_rate = float(interest_rate)
            long_term = int(long_term)
            loan_startdate = datetime.strptime(loan_startdate, '%Y-%m-%d')
            loan_enddate = datetime.strptime(loan_enddate, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Input Error", "Please ensure all values are correct.")
            return

        if not borrower_name or not loan_startdate or not loan_enddate:
            messagebox.showwarning("Input Error", "Please fill all required fields.")
            return

        db = connect_db()
        if not db:
            return  

        cursor = db.cursor()
        sql = """
            INSERT INTO loan (borrower_id, borrower_name, phone_no, address, loan_type, loan_amount, 
                              interest, long_term, start_date, end_date, loan_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            borrower_id, borrower_name, borrower_phoneno, borrower_address, loan_type, loan_amount,
            interest_rate, long_term, loan_startdate, loan_enddate, loan_status
        )

        try:
            cursor.execute(sql, values)
            db.commit()
            messagebox.showinfo("Success", "Loan inserted successfully.")
        except pymysql.MySQLError as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    def go_back_home(self):
        self.master.destroy()  
        subprocess.run(["python", "1front.py"])  

if __name__ == "__main__":
    root = tk.Tk()
    app = LoanApp(root)
    root.mainloop()
