# Project Name:  Django Permissions

## Description

This is a Django-based web application that allows users to manage various features such as blogs, products, categories, and more. The application includes role-based permissions for creating, updating, viewing, and deleting entities like blogs and products. The admin dashboard provides an overview of key metrics, and user management functionality allows administrators to manage user accounts and assign permissions.

## Features

- **CRUD Operations** for Blogs, Products, Categories
- **Admin Dashboard** for managing and monitoring project statistics
- **User Management** with role-based permissions
- **Dynamic, responsive UI** built with Bootstrap
- **Minimal `requirements.txt`** generated using `pip-chill`

## Setup

### Prerequisites

- Python 3.x
- Django 4.x
- Virtualenv (for isolated environment)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Fotsingboris/django_permissions.git
    cd django_permissions
    ```

2. **Create and activate a virtual environment**:

    - For macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - For Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3. **Install the dependencies**:

    First, install the required packages using:

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have the `requirements.txt` file yet or need to generate an updated one, use `pip-chill` to create a minimal requirements file:

    ```bash
    pip-chill > requirements.txt
    ```

4. **Apply database migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser for the admin panel**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Start the development server**:

    ```bash
    python manage.py runserver
    ```

    You can now access the project in your browser at `http://127.0.0.1:8000/`.

### Usage

Once the server is running, you can visit the app and start using the functionalities:

- **Admin Panel**: Access the Django admin interface at `http://127.0.0.1:8000/admin/` using the superuser credentials you created earlier.
- **User Management**: Manage user roles and permissions through the admin panel.
- **Dashboard**: View an overview of your blogs, products, categories, and revenue in the admin dashboard.

### Dependencies

- **Django**: A Python framework for building web applications.
- **pip-chill**: Tool for generating a minimal `requirements.txt` file.

### Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new pull request.


