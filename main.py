import alchemy
from mysite.parse_mail.mail import Mail

if __name__ == "__main__":
    alchemy.main()
    mail = Mail()
    mail.run()
