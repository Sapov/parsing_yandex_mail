import alchemy
from mail import Mail

from alchemy import BaseMail

if __name__ == "__main__":
    alchemy.main()
    mail = Mail()
    mail.run()
