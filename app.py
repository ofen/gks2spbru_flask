import database
import utility
import datetime
import os
import io

from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
from flask import make_response
from flask import jsonify
from flask import send_file
from flask import abort
from flask import redirect
from flask import url_for
from flask import Response

from PIL import Image



from natsort import natsorted

from glob import glob

app = Flask(__name__)

app.jinja_env.globals['navbar'] = database.navbar_structure

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.context_processor
def current_datetime():
    return dict(current_datetime=datetime.datetime.now())

# Routes

@app.route('/get_thumbnail/<path:image>')
def get_thumbnail(image):
    size = 300, 300
    im = Image.open(image)
    im.thumbnail(size, Image.ANTIALIAS)
    output = io.BytesIO()
    im.save(output, format='JPEG')
    return send_file(output, mimetype='image/jpeg')

@app.route('/')
def home():
    return render_template('home.htm')

@app.route('/news')
def news():
    files = natsorted(glob('data/news/*.htm'), reverse=True)
    
    files = [file for file in utility.chunks(files, 3)]

    current_page = 0
    data = list()

    if request.args.get('page'):
        current_page = request.args.get('page', type=int)

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(render_template_string(file_content))

        json_data = {'result': data, 'lenght': len(files)}

        return jsonify(json_data)

    else:

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(render_template_string(file_content))
    
        return render_template('news.htm', data=data)

@app.route('/about')
def about():
    return render_template('about.htm')

@app.route('/organization_structure')
def organization_structure():
    data = database.organization_structure
    return render_template('organization_structure.htm', data=data)

@app.route('/job')
def job():
    data = database.job
    return render_template('job.htm', data=data)

@app.route('/houses_in_service')
def houses_in_service():
    data = database.houses_in_service
    return render_template('houses_in_service.htm', data=data)

@app.route('/thank_you_letter')
def thank_you_letter():
    path = 'static/doc/thank_you_letter'
    data = list();
    years = map(str, range(2018, 2011, -1))

    for year in years:
        year_data = natsorted(glob(f"{path}/*_{year}.jpg"), reverse=True)
        if year_data:
            data.append(year)

    return render_template('thank_you_letter.htm', data=data)

@app.route('/thank_you_letter/<year>')
def thank_you_letter_(year):
    path = 'static/doc/thank_you_letter'

    year_data = natsorted(glob(f"{path}/*_{year}.jpg"), reverse=True)

    if year_data:
        data = utility.chunks(year_data, 3)
        return render_template('thank_you_letter.htm', data=data, year=year)
    else:
        return abort(404)

@app.route('/house_service_contract')
def house_service_contract():
    file = 'static/doc/Договор_управления_МКД.pdf'
    filename = 'Договор_управления_МКД.pdf'
    return send_file(file, mimetype='application/pdf', attachment_filename=filename, as_attachment=True)

@app.route('/law')
def law():
    path = 'static/doc/law'
    data = dict()
    years = map(str, range(2018, 2011, -1))

    for year in years:
        year_data = natsorted(glob(f"{path}/*.{year}.pdf"), reverse=True)
        if year_data:
            data[year] = {os.path.basename(file): file for file in year_data}

    return render_template('law.htm', data=data)

@app.route('/press')
def press():
    files = natsorted(glob('data/press/*.htm'), reverse=True)
    
    files = [file for file in utility.chunks(files, 3)]

    current_page = 0
    data = list()

    if request.args.get('page'):
        current_page = request.args.get('page', type=int)

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(render_template_string(file_content))

        json_data = {'result': data, 'lenght': len(files)}
        return jsonify(json_data)

    else:

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(render_template_string(file_content))
    
        return render_template('press.htm', data=data)

@app.route('/useful_info')
def useful_info():
    return render_template('useful_info.htm')

@app.route('/contacts_and_working_hours')
def contacts_and_working_hours():
    data = database.contacts_and_working_hours
    return render_template('contacts_and_working_hours.htm', data=data)

@app.route('/paid_services')
def paid_services():
    file = 'static/doc/Платные_услуги_2014.pdf'
    filename = 'Платные_услуги.pdf'
    return send_file(file, mimetype='application/pdf', attachment_filename=filename, as_attachment=True)

@app.route('/utility_rate')
def utility_rate():
    data = database.utility_rate
    return render_template('utility_rate.htm', data=data)

@app.route('/cost_reduction')
def cost_reduction():
    return render_template('cost_reduction.htm')

@app.route('/financial_report')
def financial_report():
    data = database.financial_report
    return render_template('financial_report.htm', data=data)

@app.route('/house_report')
def house_report():
    return redirect('https://www.reformagkh.ru/mymanager/profile/6743234/')

@app.route('/house_information')
def house_information():
    return redirect('https://gorod.gov.spb.ru/facilities/search/')

@app.route('/house_meter_reading')
def house_meter_reading():
    data = database.house_meter_reading
    return render_template('house_meter_reading.htm', data=data)

@app.route('/house_meter_reading/<report_type>/<date>')
def house_meter_reading_report(report_type, date):

    allowed_types = ['cold_water', 'hot_water', 'electric_energy', 'heat_energy']

    if report_type in allowed_types:

        file = f"data/house_meter_reading/{report_type}_{date}.csv"

        try:
            data = utility.read_csv(file)
            return render_template('house_meter_reading.htm', data=data, report_type=report_type, date=date)

        except FileNotFoundError:
            return abort(404)


@app.route('/house_service_report')
def house_service_report():
    data = database.house_service_report
    return render_template('house_service_report.htm', data=data)

@app.route('/energy_efficiency')
def energy_efficiency():
    data = database.energy_efficiency
    return render_template('energy_efficiency.htm', data=data)

@app.route('/average_monthly_temperature')
def average_monthly_temperature():
    data = database.average_monthly_temperature
    return render_template('average_monthly_temperature.htm', data=data)

@app.route('/weekly_report')
def weekly_report():
    data = database.weekly_report
    return render_template('weekly_report.htm', data=data)

@app.route('/weekly_report/<year>/<date>')
def weekly_report_(year, date):

    if year in database.weekly_report:
        if date in database.weekly_report[year]:
            data = utility.chunks(database.weekly_report[year][date], 3)
            return render_template('weekly_report.htm', data=data, date=date)
        else:
            abort(404)
    else:
        abort(404)

@app.route('/purchases')
def purchases():
    return render_template('purchases.htm')

@app.route('/gas_equipment_service')
def gas_equipment_service():
    data = database.gas_equipment_service
    return render_template('gas_equipment_service.htm', data=data)

@app.route('/reception', methods=['GET', 'POST'])
def reception():
    if request.method == 'POST':

        form_data = request.form
        attachment = request.files.get('attachment')
        
        errors = utility.validate_reception(form_data, attachment)

        if not errors:
            from_addr = 'server@yandex.ru'
            to_addr = ['example@yandex.ru']
            server = 'smtp.yandex.ru:465'
            password = 'pa$$word'

            subject = f"Интернет приемная - {form_data['subject']}"

            html_msg = f"""
                IP: {request.remote_addr}<br>
                ФИО: {form_data['fullname']}<br>
                Адрес: {form_data['address']}<br>
                Телефон: {form_data['phone']}<br>
                Email: {form_data['email']}<br>
                Тема обращения: {form_data['subject']}<br>
                Текст обращения:<br>
                {form_data['body']}
            """

            utility.send_email(from_addr, to_addr, subject, html_msg, attachment, server, password)

            return jsonify({'result': 'OK'})
        else:
            return jsonify({'result': errors})
    
    else:
        return render_template('reception.htm')



@app.route('/test')
def test():
    return json.dumps(request.args)

if __name__ == '__main__':
    app.run()