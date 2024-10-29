Here’s the properly formatted Markdown for your `README.md` file:


**Inventory Management System (IMS)**

An Inventory Management System built with Django and Django REST Framework (DRF), featuring JWT-based authentication, product management, stock alerts, and filtering capabilities.


**Features**

- **Authentication**: User authentication using JWT (JSON Web Tokens).
- **Admin & User Roles**: Admins can manage inventory items; regular users can view them.
- **Product Management**: CRUD operations for products, including filtering by category, supplier, and stock level.
- **Stock Alerts**: Low stock alert for items with quantity below a threshold.
- **Token Blacklisting**: JWT refresh tokens are blacklisted upon logout.

**Requirements**

- Python 3.12
- Django 5.1.2
- Django REST Framework
- djangorestframework-simplejwt

**Installation**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd ims
   ```
2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
   
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root and add the following variables:

   ```env
   DEBUG=True
   DOMAIN="localhost"
   DOMAIN_IP="127.0.0.1"
   
   DB_NAME="ims_db"
   DB_USER="postgres"
   DB_PASSWORD="password"
   DB_HOST="localhost"
   ```

5. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Admin User)**:
   ```bash
   python manage.py createsuperuser
   ```
7. **To start the server, run**:
  ```bash
    python manage.py runserver
   ```
You can then access the application at http://localhost:8000.


**API Documentation**

For detailed API documentation, please refer to the [Postman Documentation](https://documenter.getpostman.com/view/36402825/2sAY4uDPg3).
