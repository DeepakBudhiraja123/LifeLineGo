from celery import shared_task


from project.mail_config import mail

from flask_mail import Message


@shared_task(bind = True)
def send_email(self,email_data):
    """Send an email notification."""
    print(f"sending mail with this email data \n {email_data}")
    try:
        msg = Message(subject=email_data['subject'], recipients=[email_data['to_email']])
        msg.body = email_data['body']
        mail.send(msg)
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        
    return "done"

        
        