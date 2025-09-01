# 🍽️ Restaurant Management System (RMS)

A modern, full-stack **Restaurant Management System** built using **Python (Flask)**, HTML, CSS, and JavaScript, with a **SQLite/MySQL** database.  
This project manages reservations, orders, menu items, and feedback with an admin panel for restaurant owners.

---

## 📌 Features

- **Admin Login** — Secure login to manage reservations, menu, and feedback.
- **Reservation Management** — View, approve, and delete reservations.
- **Menu Management** — Add, edit, and delete menu items.
- **Order Tracking** — Keep track of placed orders.
- **Feedback System** — Customer feedback with sentiment analysis.
- **Export to CSV** — Download reservation and order details.
- **Email Confirmation** — Send booking confirmation emails.
- **Responsive UI** — Mobile-friendly design using Bootstrap.

---

## 🛠️ Tech Stack

**Frontend**  
- HTML5, CSS3, JavaScript  
- Bootstrap 5 for responsiveness  

**Backend**  
- Python (Flask Framework)  
- Flask-Mail for email service  
- Flask-Login for authentication  

**Database**  
- SQLite (Development)  
- MySQL (Optional for production)

---

## 📂 Project Structure

```bash
Restaurant-Management-System/
│── static/              # CSS, JS, Images
│── templates/           # HTML templates (Jinja2)
│── app.py               # Main Flask application
│── instance             # reservation.db
│── requirements.txt     # Python dependencies
