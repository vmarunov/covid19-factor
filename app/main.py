from gevent import monkey
monkey.patch_all()

import os

from flask import Flask, render_template, request, send_from_directory, send_file
from gevent import joinall
from gevent.pool import Pool

from app.data import get_countries, get_population, calc_factor


app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'templates'),
    static_url_path=''
)


@app.route('/')
@app.route('/index.html')
@app.route('/index.html/<days>')
def index(days=14):

    date = '2020-07-24'

    countries = get_countries()
    res = []
    # pool = Pool(1)
    # jobs = [
    #     pool.spawn(
    #         calc_factor, country['Slug'], country['Country'], date, days)
    #     for country in countries
    # ]
    # for job in joinall(jobs):
    #     country, factor, conf = job.get()
    #     pop = get_population(country)
    #     data.append((country, round(factor or 0, 0), pop, conf))
    data = [
        calc_factor(country['Slug'], country['Country'], date, days)
        for country in countries
    ]
    for country, factor, conf in data:
        # country, factor, conf = entry[0], entry[1], entry[2]
        pop = get_population(country)
        res.append((country, round(factor or 0, 0), pop, conf))

    return render_template(
        'index.html',
        date=date, days=days, request=request, data=res)


@app.route('/static/<path:path>')
def server_static(path):
    return send_file(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', 'static', path))


if __name__ == '__main__':
    app.run()
