LOAN MANAGEMENT SYSTEM

![image_alt](https://github.com/sivaharitha-s/loan_management_system/blob/8e6fd14cde902ff9ad79da28863d24768e979ec7/Screenshot%202024-12-30%20173008.png)

This project is a Loan Management System that I created using Python and SQL. It helps manage loan records by allowing users to add, update, delete, and view loan information. I used Tkinter to build the graphical interface and MySQL to store the data.

DATABASE DETAIL:

->Database Name: new_loan

->Table Name: loan

->Table Fields: loan_id, borrower_id, borrower_name, phone_no, address, loan_type, loan_amount, interest, long_term, start_date, end_date, loan_status


WHAT I WORKED ON:


->Python & Tkinter: I used Python and Tkinter to create a simple and easy-to-use window where users can interact with the loan data.


->MySQL Database: I connected the system to a MySQL database where all the loan information is saved. The database has a table called loan to store details like loan ID, borrower’s name, loan amount, interest, and status.


->SQL Queries: I wrote SQL queries to:

     * Fetch and show loan records.
     
     * Add new loans to the system.
     
     * Update or delete loans.
     
     * Search for loans based on keywords.
     
     
->CRUD Operations: I made sure the system can do the following:

     * Create: Add new loans.
     
     * Read: View the list of loans.
     
     * Update: Edit existing loan records.
     
     * Delete: Remove loans from the system.

     
->User Interface: I created an easy-to-use interface with:

     * A search bar to find loans.
     
     * A table to display loan details.
     
     * Buttons for adding, updating, deleting, and generating loan reports.
     
     
->Data Checking: I added checks to make sure the information entered is correct and complete.


->Extra Features: The system can also run extra scripts (1insert.py and 1gen_details.py) to add loans and generate reports.


FEATURES:

->View Loans: See a list of all loans with details like the borrower’s name, loan amount, and status.

->Search Loans: Search for loans using keywords (e.g., loan ID or borrower name).

->Add New Loan: Use a separate script to add new loans.

->Update Loan: Select a loan and edit its details.

->Delete Loan: Delete loans with a confirmation message.

->Generate Loan Reports: Run a script to generate additional loan details.
