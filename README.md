# **E-Commerce Desktop Application (Django + PyQt5)**

A full-featured E-Commerce platform built with Django and packaged as a standalone Windows Desktop Application using PyQt5 and PyInstaller.
This project combines a modern web backend with a native desktop interface for a smooth, browser-free user experience.

---

## 🚀 Features

### **🛒 User Features**

* **Product Catalog**
  Browse items by categories such as Men's Clothing, Women's Clothing, Mobiles, and Vegetables.
* **User Authentication**
  Secure signup and login system.
* **Shopping Cart**
  Add and remove items, update quantities, and view live totals.
* **Order Management**
  Place orders and track status (Pending or Completed).
* **Responsive UI**
  Built with Bootstrap 5 for a clean and modern layout.

### **🔧 Admin Features**

* **Dashboard**
  Full Django Admin included.
* **Product Management**
  Add, edit, and delete products and categories.
* **Order Tracking**
  View customer orders and update delivery status.
* **User Management**
  Manage customer accounts.

### **🖥️ Desktop App Features**

* **Native Window**
  Runs inside a dedicated desktop window using PyQt5.
* **Splash Screen**
  Shows a loading screen while the Django server starts.
* **Zero Configuration**
  The packaged `.exe` automatically starts the server and loads the UI.
* **No Browser Needed**
  The app opens inside a PyQt5 WebEngine view.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.12, Django 5.2
* **Frontend:** HTML5, Bootstrap 5, JavaScript
* **Database:** SQLite (bundled inside the EXE)
* **Desktop GUI:** PyQt5, PyQtWebEngine
* **Packaging:** PyInstaller

---

## ⚙️ Installation (For Developers)

### **Prerequisites**

* Python 3.12
* Git

---

### **1. Clone the Repository**

```bash
git clone https://github.com/Bineesh627/e_shop.git
cd e_shop
```

### **2. Set Up Virtual Environment**

```bash
python -m venv myenv
myenv\Scripts\activate
```

### **3. Install Dependencies**

```bash
pip install django pyinstaller PyQt5 PyQtWebEngine
```

### **4. Initialize Database**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Create Admin User**

```bash
python manage.py createsuperuser
```

### **6. Run Web Server (Dev Mode)**

```bash
python manage.py runserver
```

Open:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📦 Building the Desktop App (.exe)

This project includes a ready-to-use PyInstaller spec file.

### **1. Collect Static Files**

```bash
python manage.py collectstatic --noinput
```

### **2. Build Using PyInstaller**

```bash
pyinstaller build_exe.spec
```

### **3. Run the Application**

Find the executable inside the `dist/` folder.

Run:

```
e_shop.exe
```

A splash screen appears while Django starts, then the desktop window opens.

---

## 📂 Project Structure

```
e_shop/
│
├── build_exe.spec
├── manage.py
├── runserver_no_reload.py
├── db.sqlite3
│
├── e_shop/
│   ├── settings.py
│   ├── urls.py
│
├── store/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── templatetags/
│
├── templates/
├── static/
└── media/
```

---

## 🐛 Troubleshooting

### **1. App opens then closes**

* Enable console mode in `build_exe.spec` (`console=True`).
* Ensure PyQt5 and PyQtWebEngine are installed.

### **2. Images not loading**

* Run `collectstatic` again.
* Confirm `settings.py` includes the correct frozen-path logic (`sys._MEIPASS`).

### **3. "Connection Refused"**

* Happens if GUI loads before Django starts.
* The included `runserver_no_reload.py` uses a server-waiting loop to fix this.

---

## 📜 License

This project was created as part of a **Master of Computer Applications (MCA)** submission for **Uttaranchal University**.
