import smtplib
from email.mime.text import MIMEText

def send_mail(customer,wine, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '89675ab788d43d'
    password ='84f03ab93e7ba6'
    message = f'<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Wine: {wine}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>'

    sender_email = 'email1@example.com'
    receiver_email = 'example2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Wine Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())