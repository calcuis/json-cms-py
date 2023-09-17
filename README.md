## a simple NoSQL (json) contact-list management system

This Python code is a GUI application using the `tkinter` library that allows the user to manage a contact list. The application provides options to add, edit, delete, and print contacts. The contacts are stored in a JSON file named "contact.json."

Here's a breakdown of the code:

The code imports necessary modules from the `tkinter` library for creating the GUI, as well as the `uuid` and json modules.

Initializing GUI:
- The code initializes the main window (`root`) with the title "Contact List" and a specific geometry.
- It sets up a frame (`input_frame`) to hold input elements for contact details.

Creating Labels and Entry Fields:
- Labels and Entry fields are created to display and input contact details like ID, first name, last name, and cell phone number.

Creating a Treeview:
- A `ttk.Treeview` widget is created to display the contact data in a tabular format with columns for ID, first name, last name, and cell phone.

Loading and Saving Data:
- Functions are defined to load contact data from a JSON file into the Treeview and to save data from the Treeview to the JSON file.

Handling User Actions:
- Functions are defined to handle user actions such as adding, updating, deleting, and canceling entries.

Button Actions:
- Button actions are defined for "Print," "Add," "Update," "Delete," "Cancel," and "Exit" operations.

Event Binding:
- A function (`MouseButtonUpCallBack`) is bound to the Treeview to handle the event when the user clicks a row.

Executing the GUI:
- The GUI main loop is started using `root.mainloop()` to display the interface and handle user interactions.

Overall, the code creates a simple contact management system with basic functionalities using `tkinter`.
