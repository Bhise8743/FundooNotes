import smtplib, ssl
from email.message import EmailMessage
from Core.settings import email_sender, email_passwrod

mail = EmailMessage()

def email_verification(recipient, link):
    import time
    time.sleep(5)
    sender = email_sender
    password = email_passwrod

    mail['From'] = sender  # sender
    mail['To'] = recipient  # recivers
    mail['Subject'] = 'User Email Verification '  # subject

    body = f"""
        Thank you for loging Fundoo Notes ,
        Please verify your email 
        {link}
    """
    mail.set_content(body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, mail.as_string())
        smtp.quit()
    return f" {recipient} Email send Successfully"
