import smtplib
import ssl

def SendEmailFromProjectAccount(address,message):
    """Sends an email to the specified email address
        pre-condition: The 'essexdevambasadors@gmail.com' account must exist
        post-condition: The message is sent to the specified address"""
    port = 465  # For SSL
    password = 'Essex_dev1'
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("essexdevambasadors@gmail.com", password)
        server.sendmail("essexdevambasadors@gmail.com",address , message)