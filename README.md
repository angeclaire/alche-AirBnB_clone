# AirBnB Clone – The Command Interpreter

## Description

The AirBnB Clone is a project that aims to develop a simplified version of the AirBnB platform. The first phase focuses on building a command-line interpreter that allows users to manage objects within the application.

The project introduces fundamental concepts of Python programming, including object-oriented programming, inheritance, serialization, deserialization, file storage, and unit testing.

The application allows users to create, retrieve, display, update, and delete objects such as users, places, cities, states, reviews, and amenities.

The project is designed using a modular structure, making it easier to extend its functionality in future stages, including database storage, API development, and front-end integration.

## Project Objectives

The main objectives of this project are to:

- Create a parent class called `BaseModel` to handle initialization, serialization, and deserialization.
- Implement a serialization and deserialization process between Python instances, dictionaries, JSON strings, and files.
- Create application classes that inherit from `BaseModel`.
- Develop a file storage engine to save and retrieve objects.
- Build a command interpreter using Python's `cmd` module.
- Implement unit tests to validate the classes and storage engine.

## Command Interpreter

The command interpreter is a command-line interface that allows users to interact with and manage objects in the application.

It supports operations such as:

- Creating new objects.
- Retrieving individual objects.
- Displaying all existing objects.
- Updating object attributes.
- Deleting objects.

### Starting the Command Interpreter

To start the command interpreter, navigate to the root directory of the project and execute:

```bash
./console.py
```

Alternatively, run:

```bash
python3 console.py
```

When the interpreter starts successfully, the following prompt will appear:

```text
(hbnb)
```

### Using the Command Interpreter

Commands are entered after the `(hbnb)` prompt.

The main commands include:

| Command | Description | Example |
|---|---|---|
| `help` | Displays available commands and their descriptions. | `help` |
| `create` | Creates a new instance of a specified class. | `create User` |
| `show` | Displays the details of a specific instance. | `show User <id>` |
| `all` | Displays all instances or instances of a specified class. | `all` or `all User` |
| `update` | Updates an attribute of an existing instance. | `update User <id> email "user@example.com"` |
| `destroy` | Deletes a specified instance. | `destroy User <id>` |
| `quit` | Exits the command interpreter. | `quit` |
| `EOF` | Exits the command interpreter. | `Ctrl+D` |

**Note:** Commands become available as they are implemented in the project.

### Command Examples

**1. Create a new User**

```text
(hbnb) create User
```

The interpreter creates a new User object and returns its unique identifier.

**2. Display a specific User**

```text
(hbnb) show User <id>
```

Replace `<id>` with the identifier returned when the User was created.

**3. Display all objects**

```text
(hbnb) all
```

To display only User objects:

```text
(hbnb) all User
```

**4. Update an object's attribute**

```text
(hbnb) update User <id> email "user@example.com"
```

This updates the email attribute of the specified User.

**5. Delete an object**

```text
(hbnb) destroy User <id>
```

This removes the specified User object from storage.

**6. Exit the interpreter**

```text
(hbnb) quit
```

Alternatively, use `Ctrl+D` to exit.

## Project Structure

The project is organized into modules and packages to support modular development and testing.

```text
AirBnB_clone/
│
├── console.py
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── base_model.py
│   ├── user.py
│   ├── state.py
│   ├── city.py
│   ├── place.py
│   ├── review.py
│   ├── amenity.py
│   └── engine/
│       ├── __init__.py
│       └── file_storage.py
│
└── tests/
    ├── __init__.py
    ├── test_models/
    │   ├── __init__.py
    │   ├── test_base_model.py
    │   ├── test_user.py
    │   ├── test_state.py
    │   ├── test_city.py
    │   ├── test_place.py
    │   ├── test_review.py
    │   └── test_amenity.py
    └── test_engine/
        ├── __init__.py
        └── test_file_storage.py
```

## Testing

The project uses Python's built-in `unittest` framework to test classes, methods, and storage functionality.

To run all unit tests, execute:

```bash
python3 -m unittest discover tests
```

To run an individual test file, execute:

```bash
python3 -m unittest tests/test_models/test_base_model.py
```

## Technologies Used

- **Python 3:** Main programming language.
- **Python cmd module:** Used to develop the command interpreter.
- **JSON:** Used for data serialization and storage.
- **UUID:** Used to generate unique identifiers.
- **Datetime:** Used to manage creation and modification timestamps.
- **Unittest:** Used for automated testing.

## Author

Developed as part of a Python programming project focused on building the first stage of an AirBnB Clone application.
