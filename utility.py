import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import re
from werkzeug.utils import secure_filename
import csv
from PIL import Image
import io
from flask import Response

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def read_csv(csvfile):
    with open(csvfile) as fh:
        for row in csv.reader(fh):
            yield row

def get_thumbnail(image):
    size = 150, 150
    im = Image.open(image)
    io = io.StringIO()
    im.thumbnail(size, Image.ANTIALIAS)
    return Response(io.getvalue(), mimetype='image/jpeg')

def send_email(from_addr, to_addr, subject, html_msg, attachment, server, password):
    from_addr = from_addr
    password = password

    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr)
    msg['Subject'] = subject

    msg.attach(MIMEText(html_msg, 'html'))

    if attachment:
        part = MIMEApplication(attachment.read())
        part.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
        msg.attach(part)

    mail = smtplib.SMTP_SSL(server)
    mail.login(from_addr, password)
    mail.sendmail(from_addr, to_addr, msg.as_string())
    mail.close()

def validate_reception(form_data, attachment=None):
    errors = dict();

    ALLOWED_SUBJECTS = [
        'Обращение',
        'Пожелание',
        'Заявление',
        'Благодарность',
        'Претензия',
        'Жалоба',
        'Другое',
    ]

    ALLOWED_EXT = [
        '.jpg',
        '.png',
        '.pdf',
    ]

    fullname = form_data.get('fullname')
    address = form_data.get('address')
    phone = form_data.get('phone')
    email = form_data.get('email')
    subject = form_data.get('subject')
    body = form_data.get('body')        

    if fullname == '' or fullname == None:
        errors['fullname'] = 'Поле обязательно'
    elif not re.match(r'^[а-я ]+$', fullname, flags=re.IGNORECASE):
        errors['fullname'] = 'Некорректные данные'

    if address == '' or address == None:
        errors['address'] = 'Поле обязательно'
    elif not re.match(r'^[а-я \.\,0-9]+$', address, flags=re.IGNORECASE):
        errors['address'] = 'Некорректный адрес'    

    if phone == '' or phone == None:
        errors['phone'] = 'Поле обязательно'
    elif not re.match(r'^[0-9\+]+$', phone):
        errors['phone'] = 'Некорректный телефон'

    if email == '' or email == None:
        errors['email'] = 'Поле обязательно'
    elif not re.match(r'^.+@.+\..+$', email, flags=re.IGNORECASE):
        errors['email'] = 'Некорректная электронная почта'

    if subject == '' or subject == None:
        errors['subject'] = 'Поле обязательно'
    elif subject not in ALLOWED_SUBJECTS:
        errors['subject'] = 'Некорректная тема'

    if body == '' or body == None:
        errors['body'] = 'Поле обязательно'

    # Validate file
    if attachment:

        filename = secure_filename(attachment.filename.lower())

        if filename == '':
            errors['attachment'] = 'Некорректный тип файла'
        elif os.path.splitext(filename)[1] not in ALLOWED_EXT:
            errors['attachment'] = 'Некорректный тип файла'

    if errors:
        return errors
    else:
        return None

