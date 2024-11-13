# VRS - Movie Rental and Purchase Platform

This project is a web-based platform for buying and renting movies, featuring real-time payment integration. Built with Django, this application offers a streamlined experience for users to browse, rent, and purchase movies, with secure payment handling and user-friendly navigation.

## Features

- **Movie Catalog**: Browse a comprehensive list of movies available for rent or purchase.
- **Real-Time Payments**: Integrated payment system for seamless transactions.
- **User Authentication**: Secure login and registration system.
- **Responsive Design**: Optimized for a range of devices, offering a smooth user experience on both desktop and mobile.
- **Admin Dashboard**: Allows admins to manage movie listings, monitor transactions, and handle user inquiries.

## Project Structure

- **VRS/** - Main project directory.
  - **VRS/** - Django project files.
    - **asgi.py** - ASGI configuration for the project.
    - **settings.py** - Main settings file for Django configurations.
    - **urls.py** - URL routing for the entire project.
    - **wsgi.py** - WSGI configuration for deployment.
  - **static/** - Contains all static assets.
    - **CSS/** - Stylesheets for the website.
    - **images/** - Image assets for movies and UI elements.
    - **js/** - JavaScript files for frontend interactivity.
  - **store/** - Main application folder for handling movie rentals and purchases.
    - **templates/store/** - HTML templates for the store application.
    - **templatetags/** - Custom template tags for dynamic rendering.
    - **admin.py** - Configuration for the Django admin interface.
    - **apps.py** - Application configuration for Django.
    - **models.py** - Database models for movies, transactions, and users.
    - **tests.py** - Unit tests for the application.
    - **urls.py** - URL configurations specific to the store application.
    - **utils.py** - Utility functions to support core functionalities.
    - **views.py** - Main views handling HTTP requests and responses.
  - **db.sqlite3** - SQLite database file for storing application data.
  - **manage.py** - Command-line utility for administrative tasks.

- **SRS.pdf** - Software Requirements Specification document for the project.
- **Test_Plan_Outline.pdf** - Test plan and outline for quality assurance.

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Django 3.x**
- **SQLite** (or another database if configured in `settings.py`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/VRS.git
   cd VRS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Usage

- **Access the site**: Go to `http://127.0.0.1:8000` in your web browser.
- **Admin Interface**: Access the Django admin panel at `http://127.0.0.1:8000/admin` to manage movies and users (admin credentials required).

### Testing

Run unit tests using:
```bash
python manage.py test
```

## Documentation

- **SRS.pdf**: Details the functional and non-functional requirements of the system.
- **Test_Plan_Outline.pdf**: Provides an overview of the testing strategy and cases for quality assurance.

## License

This project is licensed under the MIT License.
