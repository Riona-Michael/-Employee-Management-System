import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Connect to MySQL database
conn = mysql.connector.connect(host="localhost", user="root", password="1234", database="dc")
cursor = conn.cursor()

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login Successful")
        login_window.destroy()
        employee_management()
    else:
        messagebox.showerror("Error", "Invalid credentials. Please try again.")

# Login window
def login_page():
    global login_window, entry_username, entry_password
    login_window = Tk()
    login_window.title("User Login")

    Label(login_window, text="Username").grid(row=0, column=0)
    Label(login_window, text="Password").grid(row=1, column=0)

    entry_username = Entry(login_window)
    entry_password = Entry(login_window, show="*")

    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    Button(login_window, text="Login", command=login).grid(row=2, column=0, columnspan=2)

    login_window.mainloop()

# Employee management window
def employee_management():
    def add_employee():
        name = entry_name.get()
        email = entry_email.get()
        age = entry_age.get()
        dept_name = combo_dept.get()
        salary = entry_salary.get()

        if name and email and age and dept_name and salary:
            cursor.execute("SELECT DepartmentID FROM Department WHERE DepartmentName = %s", (dept_name,))
            dept_row = cursor.fetchone()

            if dept_row:
                dept_id = dept_row[0]
                query = "INSERT INTO Emp (Name, Email, Age, DepartmentID, Salary) VALUES (%s, %s, %s, %s, %s)"
                values = (name, email, age, dept_id, salary)
                cursor.execute(query, values)
                conn.commit()
                messagebox.showinfo("Success", "Employee Added Successfully")
                fetch_data()
            else:
                messagebox.showerror("Error", "Department not found")
        else:
            messagebox.showerror("Error", "All fields are required")

    def fetch_data():
        cursor.execute("""
            SELECT e.EmpID, e.Name, e.Email, e.Age, d.DepartmentName, e.Salary
            FROM Emp e
            JOIN Department d ON e.DepartmentID = d.DepartmentID
        """)
        rows = cursor.fetchall()
        listbox.delete(0, END)
        for row in rows:
            listbox.insert(END, row)

    def delete_employee():
        selected_item = listbox.curselection()
        if selected_item:
            emp_id = listbox.get(selected_item)[0]
            cursor.execute("DELETE FROM EmployeeProject WHERE EmpID = %s", (emp_id,))
            cursor.execute("DELETE FROM Emp WHERE EmpID = %s", (emp_id,))
            conn.commit()
            messagebox.showinfo("Success", "Employee Deleted")
            fetch_data()
        else:
            messagebox.showerror("Error", "Select an employee to delete")

    def assign_to_project():
        selected_item = listbox.curselection()
        if selected_item:
            emp_id = listbox.get(selected_item)[0]
            project_name = combo_project.get()
            if project_name:
                cursor.execute("SELECT ProjectID FROM Projects WHERE ProjectName = %s", (project_name,))
                project_row = cursor.fetchone()

                if project_row:
                    project_id = project_row[0]
                    cursor.execute("INSERT IGNORE INTO EmployeeProject (EmpID, ProjectID) VALUES (%s, %s)", (emp_id, project_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Employee Assigned to Project")
                else:
                    messagebox.showerror("Error", "Project not found")
            else:
                messagebox.showerror("Error", "Please select a valid Project")
        else:
            messagebox.showerror("Error", "Select an employee to assign to a project")

    def update_employee():
        selected_item = listbox.curselection()
        if selected_item:
            emp_id = listbox.get(selected_item)[0]
            name = entry_name.get()
            email = entry_email.get()
            age = entry_age.get()
            dept_name = combo_dept.get()
            salary = entry_salary.get()

            if name and email and age and dept_name and salary:
                cursor.execute("SELECT DepartmentID FROM Department WHERE DepartmentName = %s", (dept_name,))
                dept_row = cursor.fetchone()

                if dept_row:
                    dept_id = dept_row[0]
                    query = """
                        UPDATE Emp
                        SET Name = %s, Email = %s, Age = %s, DepartmentID = %s, Salary = %s
                        WHERE EmpID = %s
                    """
                    values = (name, email, age, dept_id, salary, emp_id)
                    cursor.execute(query, values)
                    conn.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully")
                    fetch_data()
                else:
                    messagebox.showerror("Error", "Department not found")
            else:
                messagebox.showerror("Error", "All fields are required")
        else:
            messagebox.showerror("Error", "Select an employee to update")

    def on_employee_select(event):
        selected_item = listbox.curselection()
        if selected_item:
            emp_id = listbox.get(selected_item)[0]
            cursor.execute("SELECT * FROM Emp WHERE EmpID = %s", (emp_id,))
            employee = cursor.fetchone()
            if employee:
                entry_name.delete(0, END)
                entry_email.delete(0, END)
                entry_age.delete(0, END)
                entry_salary.delete(0, END)

                entry_name.insert(0, employee[1])
                entry_email.insert(0, employee[2])
                entry_age.insert(0, employee[3])
                cursor.execute("SELECT DepartmentName FROM Department WHERE DepartmentID = %s", (employee[4],))
                dept_name = cursor.fetchone()
                if dept_name:
                    combo_dept.set(dept_name[0])
                entry_salary.insert(0, employee[5])

    def load_departments():
        cursor.execute("SELECT DepartmentName FROM Department")
        rows = cursor.fetchall()
        combo_dept['values'] = [row[0] for row in rows]
        combo_search_dept['values'] = [''] + [row[0] for row in rows]

    def load_projects():
        cursor.execute("SELECT ProjectName FROM Projects")
        rows = cursor.fetchall()
        combo_project['values'] = [row[0] for row in rows]

    def show_department_counts():
        cursor.execute("""
            SELECT d.DepartmentName, COUNT(e.EmpID)
            FROM Department d
            LEFT JOIN Emp e ON d.DepartmentID = e.DepartmentID
            GROUP BY d.DepartmentID
        """)
        rows = cursor.fetchall()
        result = "\n".join([f"{row[0]}: {row[1]} employee(s)" for row in rows])
        messagebox.showinfo("Employees per Department", result)

    def show_project_counts():
        cursor.execute("""
            SELECT p.ProjectName, COUNT(ep.EmpID)
            FROM Projects p
            LEFT JOIN EmployeeProject ep ON p.ProjectID = ep.ProjectID
            GROUP BY p.ProjectID
        """)
        rows = cursor.fetchall()
        result = "\n".join([f"{row[0]}: {row[1]} employee(s)" for row in rows])
        messagebox.showinfo("Employees per Project", result)

    def show_salary_stats():
        cursor.execute("""
            SELECT d.DepartmentName, MIN(e.Salary), MAX(e.Salary), AVG(e.Salary)
            FROM Department d
            LEFT JOIN Emp e ON d.DepartmentID = e.DepartmentID
            GROUP BY d.DepartmentName
        """)
        rows = cursor.fetchall()
        result = "\n".join([f"{row[0]}: Min ₹{row[1] or 0:.2f}, Max ₹{row[2] or 0:.2f}, Avg ₹{row[3] or 0:.2f}" for row in rows])
        messagebox.showinfo("Salary Stats", result)

    # Filter Employees by Name and Department only
    def filter_employees():
        name = entry_search_name.get()
        dept = combo_search_dept.get()

        query = """
            SELECT e.EmpID, e.Name, e.Email, e.Age, d.DepartmentName, e.Salary
            FROM Emp e
            JOIN Department d ON e.DepartmentID = d.DepartmentID
            WHERE 1 = 1
        """
        values = []

        if name:
            query += " AND e.Name LIKE %s"
            values.append('%' + name + '%')
        if dept:
            query += " AND d.DepartmentName = %s"
            values.append(dept)

        cursor.execute(query, values)
        rows = cursor.fetchall()
        listbox.delete(0, END)
        for row in rows:
            listbox.insert(END, row)

    root = Tk()
    root.title("Employee Management System")

    Label(root, text="Name").grid(row=0, column=0)
    Label(root, text="Email").grid(row=1, column=0)
    Label(root, text="Age").grid(row=2, column=0)
    Label(root, text="Department").grid(row=3, column=0)
    Label(root, text="Salary").grid(row=4, column=0)
    Label(root, text="Project (For Assignment)").grid(row=5, column=0)

    entry_name = Entry(root)
    entry_email = Entry(root)
    entry_age = Entry(root)
    entry_salary = Entry(root)
    combo_dept = ttk.Combobox(root, state="readonly")
    combo_project = ttk.Combobox(root, state="readonly")

    entry_name.grid(row=0, column=1)
    entry_email.grid(row=1, column=1)
    entry_age.grid(row=2, column=1)
    combo_dept.grid(row=3, column=1)
    entry_salary.grid(row=4, column=1)
    combo_project.grid(row=5, column=1)

    Button(root, text="Add", command=add_employee).grid(row=6, column=0)
    Button(root, text="Update", command=update_employee).grid(row=6, column=1)
    Button(root, text="Delete", command=delete_employee).grid(row=6, column=2)
    Button(root, text="Assign to Project", command=assign_to_project).grid(row=7, column=0)
    Button(root, text="Dept Count", command=show_department_counts).grid(row=7, column=1)
    Button(root, text="Project Count", command=show_project_counts).grid(row=7, column=2)
    Button(root, text="Salary Stats", command=show_salary_stats).grid(row=8, column=0)

    Label(root, text="Search: Name").grid(row=9, column=0)
    entry_search_name = Entry(root)
    entry_search_name.grid(row=9, column=1)

    Label(root, text="Dept").grid(row=10, column=0)
    combo_search_dept = ttk.Combobox(root, state="readonly")
    combo_search_dept.grid(row=10, column=1)

    Button(root, text="Filter", command=filter_employees).grid(row=14, column=0, columnspan=2)

    listbox = Listbox(root, width=100)
    listbox.grid(row=15, column=0, columnspan=3)
    listbox.bind("<<ListboxSelect>>", on_employee_select)

    load_departments()
    load_projects()
    fetch_data()

    root.mainloop()
login_page()
