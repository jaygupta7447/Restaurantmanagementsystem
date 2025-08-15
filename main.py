from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import datetime
import csv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')


# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mail config
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
)
mail = Mail(app)

# Database Model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    guests = db.Column(db.String(10))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# ------------------- ROUTES -------------------
@app.route('/healthz')
def health_check():
    return "OK", 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    guests = request.form.get('person')
    date = request.form.get('reservation_date')
    time = request.form.get('reservation_time')
    message = request.form.get('message')

    new_entry = Reservation(
        name=name, phone=phone, email=email,
        guests=guests, date=date, time=time, message=message
    )
    db.session.add(new_entry)
    db.session.commit()

    # Send confirmation email
    msg = Message("Reservation Confirmation",
                  sender=os.getenv("MAIL_USERNAME"),
                  recipients=[email, os.getenv("MAIL_USERNAME")])
    msg.body = f"""
Hello {name},

✅ Your reservation for {guests} guest(s) is confirmed on:
📅 Date: {date}
⏰ Time: {time}

📞 Contact: {phone}
📝 Message: {message}

Thanks for choosing FeastIQ!
"""
    mail.send(msg)

    return redirect(url_for('home'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('view_reservations'))
        else:
            return "Unauthorized", 401
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route("/admin/reservation")
def view_reservations():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    data = Reservation.query.order_by(Reservation.created_at.desc()).all()
    return render_template('admin_reservations.html', reservations=data)

@app.route('/admin/export')
def export_csv():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    reservations = Reservation.query.all()

    def generate():
        yield 'Name,Phone,Email,Guests,Date,Time,Message,Created_At\n'
        for r in reservations:
            yield f'{r.name},{r.phone},{r.email},{r.guests},{r.date},{r.time},"{r.message}",{r.created_at}\n'

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=reservations.csv"})

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_reservation(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    return redirect(url_for('view_reservations'))

# ------------------- MAIN -------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures tables are created
    app.run(debug=True)
