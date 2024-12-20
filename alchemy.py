import datetime
from sqlalchemy.sql import func
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///base.db")


class Base(DeclarativeBase):
    pass


class BaseMail(Base):
    __tablename__ = "mail_ya"
    # id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(String(200), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    email_in_body: Mapped[str] = mapped_column()
    phones: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.item_id!r})"


def create_items(data: dict):
    '''Добавляем запись, если такая есть ловим искоючение'''
    try:
        with Session(engine) as session:
            items_mail = BaseMail(
                email=data['email'],
                name=' '.join(data['name']),
                email_in_body=' '.join(data['email_in_body']),
                phones=' '.join(data['phones']),
            )

            session.add(items_mail)
            session.commit()
    except Exception as err:
        print('--ERROR--', str(err))


def fetch_id(email: str):
    '''проверяем уникальность объявления в базе'''
    with Session(engine) as session:
        stmt = select(BaseMail).where(BaseMail.email == email)
        resp = session.scalar(stmt)
        if resp is None:
            print('[!] Нет такого объявления, значит добавляем')
            return True
        else:
            print('[+] Объявление уже есть в базе', resp)
            return False


def view_items(email: str):
    with Session(engine) as session:
        stmt = select(BaseMail).where(BaseMail.email == email)
        res = session.scalar(stmt)
        print('[!] Новый адрес: ', res)

    # def change_valid():
    #     '''Объявления меньше 5000 руб. и объявления больше 70 000 руб. нам не интересны'''
    #     with Session(engine) as session:
    #         stmt = select(Avito).where(Avito.price <= 5000)    #         resp = session.scalars(stmt)
    #         for i in resp:
    #             print(i)


def main():
    Base.metadata.create_all(engine)
    # change_valid()


if __name__ == '__main__':
    main()
