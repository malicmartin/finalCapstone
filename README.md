# Task Manager - HyperionDev Bootcamp Project

## Description
This project is a task manager application developed as part of the HyperionDev bootcamp coursework. The application helps users manage their tasks efficiently.

## Table of Contents
- [Description](#description)
- [Files Overview](#files-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Note](#note)
- [Contributing](#contributing)
- [How the original program needed to be modified](#how-the-original-program-needed-to-be-modified)
- [Credits](#credits)

## Files Overview
- `task_manager.py`: Contains the original program provided by the bootcamp.
- `tasks.txt` and `user.txt`: Text files used by the program for interaction.

## Installation
To install and run the project clone or download the repository to your local machine.
   
## Usage
To use the program, follow these steps:

1. Open the folder containing the project files in your IDE.
2. Run the program by executing the `task_manager` file.
3. Follow the on-screen instructions to interact with the task manager application.
4. Make sure to keep the `tasks.txt` and `user.txt` files in the same directory as the program for proper functionality.

## Note
- Ensure that you have Python installed on your system and that it is properly configured in your environment variables.
- Make sure to keep the `tasks.txt` and `user.txt` files in the same directory as the program for proper functionality.

## Contributing
Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## How the original program needed to be modified

- Use the `task_manager.py` file, together with the supporting text files `user.txt` and `tasks.txt` for this Capstone project. In this task, you will be modifying `task_manager.py` to extend its functionality. Working on existing code files to extend them is great practice for working in a developer team on an established code base.

- You will notice that the main body of the code requires functionality for:
  - Registering a user
  - Adding a task
  - Viewing all tasks
  - Viewing the current user's tasks. However, because there is so much functionality needed to complete this, the main body of the loop becomes difficult to read. Using the principle of abstraction, refactor the code to create and use the following functions:

    - `reg_user`: a function that is called when the user selects ‘r’ to register a user
    - `add_task`: a function that is called when a user selects ‘a’ to add a new task
    - `view_all`: a function that is called when users type ‘va’ to view all the tasks listed in ‘tasks.txt’.
    - `view_mine`: a function that is called when users type ‘vm’ to view all the tasks that have been assigned to them.

- Modify the function called `reg_user` to make sure that you don’t duplicate usernames when you add a new user to `user.txt`. If a user tries to add a username that already exists in `user.txt`, provide a relevant error message and allow them to try to add a user with a different username.

- Add the following functionality when the user selects ‘vm’ to view all the tasks assigned to them:
  - Display all tasks in a manner that is easy to read. Make sure that each task is displayed with a corresponding number that can be used to identify the task.
  - Allow the user to select either a specific task (by entering a number) or input ‘-1’ to return to the main menu.
  - If the user selects a specific task, they should be able to choose to either mark the task as complete or edit the task.
  - If the user chooses to mark a task as complete, the ‘Yes’/’No’ value that describes whether the task has been completed or not should be changed to ‘Yes’.
  - If the user chooses to edit a task, the username of the person to whom the task is assigned or the due date of the task can be edited. The task can only be edited if it has not yet been completed.

- Add an option to generate reports to the main menu of the application. When the user chooses to generate reports, two text files, called `task_overview.txt` and `user_overview.txt`, should be generated. Both these text files should output data in a user-friendly, easy to read manner:

  - `task_overview.txt` should contain:
    - The total number of tasks that have been generated and tracked using the `task_manager.py`
    - The total number of completed tasks.
    - The total number of uncompleted tasks.
    - The total number of tasks that haven’t been completed and that are overdue
    - The percentage of tasks that are incomplete.
    - The percentage of tasks that are overdue.

  - `user_overview.txt` should contain:
    - The total number of users registered with `task_manager.py`.
    - The total number of tasks that have been generated and tracked using `task_manager.py`.
    - For each user also describe:
      - The total number of tasks assigned to that user.
      - The percentage of the total number of tasks that have been assigned to that user
      - The percentage of the tasks assigned to that user that have been completed
      - The percentage of the tasks assigned to that user that must still be completed
      - The percentage of the tasks assigned to that user that has not yet been completed and are overdue

- Modify the menu option that allows the admin to display statistics so that the reports generated are read from `tasks.txt` and `user.txt` and displayed on the screen in a user-friendly manner. If these text files don’t exist.

## Credits

- Original Project by [HyperionDev](https://www.hyperiondev.com/) - A skills bootcamp company.
