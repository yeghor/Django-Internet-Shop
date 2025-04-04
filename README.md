# **Django-Internet-Shop**
This web application is my attempt to create an internet shop prototype.

# **Features**
- Login/Register/Logout system.
- Simple and nice Bootstrap 5 design.
- Models for products with the ability to add pictures.
- Working cart class that uses the session key to keep the cart alive during the session life period.
- Dynamic change of product stock quantity and availability when the order is confirmed.
- Working form to collect user delivery info that stores it into the order model.
- Each order has a unique hash and is connected to the user with a foreign key.

### **Installation**
1. **Clone the repository:**
```bash
git clone https://github.com/yeghor/Django-Internet-Shop.git
cd Learning-Log-Django
```
2. **Create a virtual enviroment:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate
# On MacOS/Linux
source venv/bin/activate
```

3. **Install the dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up the database:**
```bash
python manage.py migrate
```

5. **Create a superuser:**
```bash
python manage.py createsuperuser
```

5. **Run the development server:**
```bash
python manage.py runserver
```

## Usage
- Navigate **to http://127.0.0.1:8000** in your web browser.
- Sign up for an account and log in.
- Start making orders and testing the application!
