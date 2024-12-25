import base64
import email
import imaplib
import json
import os
import re

from dotenv import load_dotenv, find_dotenv
from .models import BaseMail

load_dotenv(find_dotenv())


class Mail:
    password_mail = os.getenv('PASS_MAIL')
    mail_name = os.getenv('MAIL_NAME')
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    mail.login(mail_name, password_mail)
    mail_letter_from = None
    msg_mail_text = None
    ddata = []

    def __get_mail(self):
        mail = imaplib.IMAP4_SSL('imap.yandex.ru')
        mail.login(self.mail_name, self.password_mail)
        print(mail.select("Archive"))  # переходим в папку архив
        # _, count = mail.select("Archive") # переходим в папку архив
        typ, data = mail.search(None, 'ALL')  # номера всех писем
        # print(f'typ: {typ}, data: {data}')
        try:
            for num in data[0].split():
                print(f'[NUM] ->>', num)
                typ, data = mail.fetch(num, '(RFC822)')
                # print('Message %s\n%s\n' % (num, data[0][1]))
                msg = email.message_from_bytes(data[0][1])
                self.mail_letter_from = msg["Return-path"]  # e-mail отправителя
                # with open(f'mail_box/{num}_mail_.txt', 'w') as file:

                print(f'[Почта отправителя]: {self.mail_letter_from}')
                payload = msg.get_payload()
                for part in msg.walk():
                    if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                        try:
                            self.msg_mail_text = base64.b64decode(part.get_payload()).decode()
                            # file.write(f'{base64.b64decode(part.get_payload()).decode()} \n')
                            st = self.msg_mail_text
                            lst = st.split()
                            self.msg_mail_text = ' '.join(lst)

                            tel_lst = self.search_phone()
                            mail_lst = self.search_mail_in_body()
                            name = self.__search_name()

                            ddata = {
                                'email': self.mail_letter_from,
                                'name': list(set(name)),
                                'email_in_body': list(set(mail_lst)),
                                'body': self.msg_mail_text,
                                'phones': tel_lst,
                            }
                            print(f'DATA{ddata}')
                            self.ddata.append(ddata)
                            self.__data_save()
                            self.create_items(ddata)
                            # print(f'self.ddata{self.ddata}')
                        except Exception as Ex:
                            print(Ex)
        except Exception as Ex:
            print(Ex)

    def search_phone(self):
        '''Находим в тексте номера телефонов'''
        lst_tel = []
        phoneNumRegex = re.compile(r"(\+7|8)(\s?)(-?)(\(?)(\d{3})(\)?)(-?)(\s?)(\d{3})(\s?)(-?)(\d{2})(\s?)(-?)(\d{2})")
        mo = phoneNumRegex.findall(self.msg_mail_text)
        for i in mo:
            tel = ''
            for j in i:
                if j not in ' -()' and j != '':
                    tel += j
            print(f'Найден новый телефон: {tel}')
            if tel not in lst_tel:
                lst_tel.append(tel)
        print(f'[СПИСОК ТЕЛЕФОНОВ ПИСЬМА]{lst_tel}')
        return lst_tel

    def search_mail_in_body(self):
        """Находим в тексте почту"""
        lst_mail = []
        emailRegex = re.compile(r"(\w+([.-]?\w+)@\w+([.-]?\w+)(\w{2,3})?)")
        mo = emailRegex.findall(self.msg_mail_text)
        print('Найдено: ', mo)
        for i in mo:
            mail = i[0]
            print(mail)
            if mail not in lst_mail:
                lst_mail.append(mail)
        print(lst_mail)
        return lst_mail

    def __search_name(self):
        lst_name = []
        phoneNumRegex = re.compile(r"([А-ЯЁ][а-яё]*\s[А-ЯЁ](.?)[а-яё]*(\s)?[А-ЯЁ](.?)[а-яё]*)")
        mo = phoneNumRegex.findall(self.msg_mail_text)
        for i in mo:
            print(f'Найдено ИМя {i[0]}')
            lst_name.append(i[0])
        print('Найдено names: ', mo)
        return lst_name

    def search_name_s_uvag(self):
        '''Поиск имен после слов с Уважением'''
        pass

    def __data_save(self):
        with open('../../old_items.json', 'w', encoding='utf-8') as f:
            json.dump(self.ddata, f, ensure_ascii=False, indent=4)

    def create_items(self, data: dict):
        '''Добавляем запись, если такая есть ловим искоючение'''
        BaseMail.objects.get_or_create(
            email=data['email'],
            name=' '.join(data['name']),
            email_in_body=' '.join(data['email_in_body']),
            phones=' '.join(data['phones'])
        )

    def run(self):
        self.__get_mail()


if __name__ == '__main__':
    a = Mail()
    a.run()
