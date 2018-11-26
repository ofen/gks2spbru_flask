import database
from utility import chunks
import datetime
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
from flask import send_file

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
    
    files = [file for file in chunks(files, 3)]

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
    years = map(str, range(2012, 2018))

    for year in years:
        year_data = glob(f'{path}/*_{year}.jpg')
        data[year] = chunks(year_data, 3)

    data = {key:value for (key, value) in sorted(data.items(), reverse=True)}

    return render_template('thank_you_letter.htm', data=data)

@app.route('/contacts_and_working_hours')
def contacts_and_working_hours():
    data = database.contacts_and_working_hours
    return render_template('contacts_and_working_hours.htm', data=data)

@app.route('/house_service_contract')
def house_service_contract():
    file = 'static/doc/Договор_управления_МКД.pdf'
    return send_file(file, mimetype='application/pdf', attachment_filename='test.pdf')

@app.route('/test')
def test():
    return json.dumps(request.args)

if __name__ == '__main__':
    app.run()