# Import necessary libraries
import os
from datetime import datetime, date

# Define date format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Check if 'tasks.txt' exists, create it if not
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Initialize task list
task_list = []

# Function to boot the task file
def boot_task_file():
    global task_list
    with open("tasks.txt", 'r') as task_file:      
        task_data = task_file.read().split("\n")        
        task_data = [t for t in task_data if t != ""]   

    # Parse task data and populate task list
    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT) 
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        curr_t['ID'] = task_components[6] if len(task_components) > 6 else 1
        task_list.append(curr_t)

# Function to fix the first line of the task file
def fix_first_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    if lines and len(lines[0].split(';')) < 7:
        lines[0] = lines[0] + ';1\n'
        with open(filename, 'w') as file:
            file.writelines(lines)

# Fix first line and boot task file
fix_first_line('tasks.txt')
boot_task_file()

# User login section
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read username and password data from user.txt
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")        

# Create username-password dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Attempt user login
def user_login(username_password):
    while True:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            return curr_user  # Return the logged-in user's name

# Main part of the code
def main():
    logged_in_user = None
    
    while not logged_in_user:
        logged_in_user = user_login(username_password)  # Log in the user and store the current user's name
    
    # Once logged in, proceed to the main menu
    main_menu(logged_in_user)

# Main menu function
def main_menu(curr_user):
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gr - Generate reports
sw - Switch user
e - Exit
: ''').lower()

    # Function to register a new user
    def reg_user():
        new_username = input("New Username: ")
        existing_usernames = set()
        with open("user.txt", "r") as file:
            for line in file:
                username = line.split(";")[0].strip()
                existing_usernames.add(username)
        while new_username in existing_usernames:
            print(f"The user {new_username} already exists")
            new_username = input("Please register a new user: ")

        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
        else:
            print("\nPasswords do no match")

    # Function to add a task
    def add_task():
        task_id_counter = len(task_list) + 1
        task_username = input("Name of person assigned to task: ")
        while task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            task_username = input("Name of person assigned to task: ")
        
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        curr_date = date.today()
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False,
            "ID" : task_id_counter
        }

        task_list.append(new_task)
        task_id_counter += 1
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [                    
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No",
                    str(t['ID']),
                ]

                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))

        print("\nTask successfully added.")
        boot_task_file()

    # Function to view all tasks
    def view_all():
        for t in task_list:
            disp_str = f"_" * 50
            disp_str += f"\nTask ID: \t {t['ID']}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task Completion: \n {'Yes' if t['completed'] else 'No'}"
            print(disp_str)
        print("_" * 50)

    # Function to view user's own tasks and edit them
    def view_mine():
        def edit_task():
            # Select a task to edit
            with open("tasks.txt", "r") as file:
                    editable_tasks = {}
                    for editable in file:
                        if editable.split(";")[6].strip() not in editable_tasks:
                            if editable.split(";")[5] == "No":
                                if curr_user == "admin":
                                    editable_tasks[(int(editable.split(";")[6].strip()))] = editable.split(";")[0]
                                elif curr_user == editable.split(";")[0]:
                                    editable_tasks[(int(editable.split(";")[6].strip()))] = editable.split(";")[0]
                    print("_" * 50)
                    print("The incomplete tasks, which you can edit are: ")
                    for ID, user in editable_tasks.items():
                        print(f"Task ID: {ID} \t user: {user}")
                    print("_" * 50)
                    while True:
                        try:
                            task_editor = int(input("Enter the task ID you'd like to edit or enter -1 to return to the main menu: "))
                            if task_editor == -1:
                                return main_menu(curr_user)
                            elif task_editor not in editable_tasks:
                                print("Please select from the tasks you are allowed to edit.")
                            else:
                                break
                        except ValueError:
                            print("Invalid input. Please enter a valid task ID.")

                    with open("tasks.txt", "r") as file:
                        lines = file.readlines()
                        while True:
                            changes = input("""
        Are you changing the:
        1. task's owner, 
        2. its due date or 
        3. completion status?                        
        : """)
                            if changes not in ["1", "2", "3"]:
                                print("Invalid input. Please try again.")
                            else:
                                break

                        if changes == "1":
                            with open("user.txt", "r") as users:
                                user_list = []
                                for user in users:
                                    if user.split(";")[0] not in user_list:
                                        user_list.append(user.split(";")[0])
                                change = lines[task_editor - 1].split(";")
                                new_owner = input("Who do you want the new owner to be: ")
                                while True:
                                    if new_owner not in user_list:
                                        print("User does not exist. Existing users are:")
                                        print("_" * 50)
                                        for user in user_list:
                                            print(user)
                                        print("_" * 50)
                                        new_owner = input("Who do you want the new owner to be: ")
                                    else:
                                        break
                                change[0] = new_owner
                                change = ";".join(change)
                                lines[task_editor - 1] = change
                                lines = "".join(lines)
                                with open("tasks.txt", 'w') as file:
                                    file.writelines(lines)
                        
                        elif changes == "2":
                            change = lines[task_editor - 1].split(";")
                            while True:
                                new_date = input("Due date of task (YYYY-MM-DD): ")
                                try:
                                    datetime.strptime(new_date, '%Y-%m-%d')
                                    break
                                except ValueError:
                                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                            change[3] = new_date                      
                            change = ";".join(change)                          
                            lines[task_editor - 1] = change                    
                            lines = "".join(lines)                            
                            with open("tasks.txt", 'w') as file:         
                                file.writelines(lines)                          

                        elif changes == "3":                                 
                            change = lines[task_editor - 1].split(";")         
                            completion_status = input("Enter Yes for completed or No for incomplete status: ")
                            if completion_status.lower() == "yes":
                                completion_status = "Yes"
                            if completion_status.lower() == "no":
                                completion_status = "No"
                                                                               
                            while completion_status not in ["Yes", "No"]:      
                                    print("Invalid input, please enter Yes or No.")
                                    completion_status = input("Enter Yes for completed or No for incomplete status: ")      
                            change[5] = completion_status                     
                            change = ";".join(change)                         
                            lines[task_editor - 1] = change                  
                            lines = "".join(lines)                             
                            with open("tasks.txt", 'w') as file:       
                                file.writelines(lines)                       

        # Display user's tasks (admin can see every task)
        for t in task_list:
            if curr_user == "admin" or t['username'] == curr_user:
                disp_str = f"_" * 50
                disp_str += f"\nTask ID: \t {t['ID']}\n"
                disp_str += f"Task: \t\t {t['title']}\n"                
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                disp_str += f"Task Completion: \n {'Yes' if t['completed'] else 'No'}"
                print(disp_str)                               
                
        edit_task()
        boot_task_file()   

    # Function to display statistics
    def display_stats():
        # Check if user_overview.txt and task_overview.txt exist
        if not os.path.exists("user_overview.txt") or not os.path.exists("task_overview.txt"):
            # If they don't exist, generate the reports
            generate_reports()

        # Read and display the contents of user_overview.txt
        with open("user_overview.txt", "r") as user_file:
            print("User Overview:")
            print(user_file.read())

        # Read and display the contents of task_overview.txt
        with open("task_overview.txt", "r") as task_file:
            print("Task Overview:")
            print(task_file.read())

    def generate_reports():
        from datetime import datetime

        # Get the current date
        current_date = datetime.now().date()

        # Define counters and dictionaries
        task_count = {"total": 0, "completed": 0, "incomplete": 0, "overdue": 0}
        user_tasks = {}
        user_statistics = {}
        total_users = 0
        users = []

        # Read tasks from the file
        with open("tasks.txt", "r") as task_file, open("user.txt", "r") as user_file:
            task_data = task_file.readlines()
            user_data = user_file.readlines()

            # Count total users and initialize user tasks dictionary
            for user_line in user_data:
                username = user_line.strip().split(";")[0]
                total_users += 1
                users.append(username)
                user_tasks[username] = 0
                user_statistics[username] = {"completed": 0, "incomplete": 0, "overdue": 0}

            # Process tasks data and calculate statistics
            for task_line in task_data:
                task_components = task_line.strip().split(";")
                task_count["total"] += 1
                user_tasks[task_components[0]] += 1
                if task_components[5] == "Yes":
                    task_count["completed"] += 1
                    user_statistics[task_components[0]]["completed"] += 1
                else:
                    task_count["incomplete"] += 1
                    user_statistics[task_components[0]]["incomplete"] += 1
                    due_date = datetime.strptime(task_components[3], "%Y-%m-%d").date()
                    if due_date < current_date:
                        task_count["overdue"] += 1
                        user_statistics[task_components[0]]["overdue"] += 1

        # Calculate percentages based on incomplete and overdue tasks for tasks overview
        total_tasks = task_count["total"]
        percentage_complete = (task_count["completed"] / total_tasks) * 100 if total_tasks != 0 else 0
        percentage_incomplete = (task_count["incomplete"] / total_tasks) * 100 if total_tasks != 0 else 0
        percentage_overdue = (task_count["overdue"] / total_tasks) * 100 if total_tasks != 0 else 0

        # Write statistics to task_overview.txt
        with open("task_overview.txt", "w") as task_report:
            task_report.write(f"Tasks in total:\t\t\t\t {task_count['total']}\n")
            task_report.write(f"Completed tasks:\t\t\t {task_count['completed']}\n")
            task_report.write(f"Completed tasks:\t\t\t {round(percentage_complete, 2)}%\n")
            task_report.write(f"Incomplete tasks:\t\t\t {task_count['incomplete']}\n")
            task_report.write(f"Incomplete tasks:\t\t\t {round(percentage_incomplete, 2)}%\n")
            task_report.write(f"Overdue tasks:\t\t\t\t {task_count['overdue']}\n")
            task_report.write(f"Overdue tasks:\t\t\t\t {round(percentage_overdue, 2)}%\n")
            task_report.write("_" * 50)

        # Write statistics to user_overview.txt
        with open("user_overview.txt", "w") as user_overview:
            user_overview.write(f"Total registered users: \t\t {total_users}\n")
            user_overview.write(f"Total number of tasks: \t\t\t {task_count['total']}\n")
            user_overview.write("_" * 50)

            for user in users:
                user_overview.write(f"\nUsername: \t\t\t\t {user}\n")
                user_overview.write(f"Tasks assigned: \t\t\t {user_tasks[user]}\n")

                # Calculate the number of completed, incomplete, and overdue tasks for the user
                completed_tasks = user_statistics[user]['completed']
                incomplete_tasks = user_statistics[user]['incomplete']
                overdue_tasks = user_statistics[user]['overdue']

                # Calculate the percentages based on the number of tasks assigned to the user
                if user_tasks[user] != 0:
                    complete_percentage = (completed_tasks / user_tasks[user]) * 100
                    incomplete_percentage = (incomplete_tasks / user_tasks[user]) * 100
                    overdue_percentage = (overdue_tasks / user_tasks[user]) * 100
                else:
                    complete_percentage = 0
                    incomplete_percentage = 0
                    overdue_percentage = 0

                user_overview.write(f"User's share of tasks: \t\t\t {round((user_tasks[user] / task_count['total']) * 100, 2)}%\n")
                user_overview.write(f"User's complete tasks: \t\t\t {round(complete_percentage, 2)}%\n")
                user_overview.write(f"User's incomplete tasks: \t\t {round(incomplete_percentage, 2)}%\n")
                user_overview.write(f"User's overdue tasks: \t\t\t {round(overdue_percentage, 2)}%\n")
                user_overview.write("_" * 50)
    
    def switch_user():
        print("Switch User")
        new_user = user_login(username_password)
        return new_user


    # Menu options logic
    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'ds' and curr_user != 'admin':                        
        print("\nOnly the administrator can access this function.")
    elif menu == 'ds' and curr_user == 'admin':
        print("")
        display_stats()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'sw':
        curr_user = switch_user()
        main_menu(curr_user)
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("\nYou have made a wrong choice, Please Try again")
        main_menu(curr_user)

    # Continue option
    while True:
        user_input = input("Enter Yes to continue (main menu), No to exit: ").strip().lower()
        if user_input == "yes":
            main_menu(curr_user)
            break
        elif user_input == "no":
            print("Exiting the program.")
            exit()
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Main part of the code
if __name__ == "__main__":
    main()
