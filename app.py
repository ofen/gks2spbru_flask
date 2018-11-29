import database
import utility
import datetime
import os
import io
import csv

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
from flask import send_file
from flask import abort
from flask import redirect
from flask import url_for


from natsort import natsorted

from glob import glob

app = Flask(__name__)

app.jinja_env.globals['navbar'] = database.navbar_structure



@app.context_processor
def current_datetime():
    return dict(current_datetime=datetime.datetime.now())

# Routes

@app.route('/')
def home():
    return render_template('home.htm')

@app.route('/news')
def news():
    files = glob('data/news/*.htm')

    natsorted(files, reverse=True)
    
    files = [file for file in utility.chunks(files, 3)]

    current_page = 0
    data = list()

    if request.args.get('page'):
        current_page = request.args.get('page', type=int)

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(file_content)

        json_data = {'result': data, 'lenght': len(files)}
        return jsonify(json_data)

    else:

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(file_content)
    
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
    data = dict();
    years = map(str, range(2018, 2011, -1))

    for year in years:
        year_data = glob(f'{path}/*_{year}.jpg')
        data[year] = utility.chunks(year_data, 3)

    return render_template('thank_you_letter.htm', data=data)

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
        year_data = glob(f'{path}/*.{year}.pdf')
        data[year] = utility.to_generator(year_data)

    return render_template('law.htm', data=data)

@app.route('/press')
def press():
    files = glob('data/press/*.htm')

    files = natsorted(files, reverse=True)
    
    files = [file for file in utility.chunks(files, 3)]

    current_page = 0
    data = list()

    if request.args.get('page'):
        current_page = request.args.get('page', type=int)

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(file_content)

        json_data = {'result': data, 'lenght': len(files)}
        return jsonify(json_data)

    else:

        for file in files[current_page]:
            with open(file) as fh:
                file_content = fh.read()
                data.append(file_content)
    
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
    data = {key:value for (key, value) in sorted(data.items(), reverse=True)}
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
    data = {key:value for (key, value) in sorted(data.items(), reverse=True)}
    return render_template('house_meter_reading.htm', data=data)

@app.route('/house_meter_reading/<report_type>/<date>')
def house_meter_reading_report(report_type, date):

    allowed_types = ['cold_water', 'hot_water', 'electric_energy', 'heat_energy']

    if report_type in allowed_types:

        file = f'data/house_meter_reading/{report_type}_{date}.csv'

        try:
            with open(file) as csvfile:
                data = csv.reader(csvfile)

                return render_template('house_meter_reading.htm', data=data, report_type=report_type, date=date)

        except FileNotFoundError:
            return abort(404)


@app.route('/house_service_report')
def house_service_report():
    data = database.house_service_report
    data = {key:value for (key, value) in sorted(data.items(), reverse=True)}
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
    data = database.weekly_report.keys()
    data = list(data)[::-1]
    return render_template('weekly_report.htm', data=data)

@app.route('/weekly_report/<date>')
def weekly_report_(date):
    if date in database.weekly_report.keys():
        data = utility.chunks(database.weekly_report.get(date), 3)
        return render_template('weekly_report.htm', data=data, date=date)
    else:
        abort(404)

@app.route('/purchases')
def purchases():
    return render_template('purchases.htm')

@app.route('/gas_equipment_service')
def gas_equipment_service():
    data = database.gas_equipment_service
    return render_template('gas_equipment_service.htm', data=data)

@app.route('/test')
def test():
    return json.dumps(request.args)

if __name__ == '__main__':
    app.run()