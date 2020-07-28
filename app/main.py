import os
from datetime import datetime

from flask import Flask, render_template, request, send_file
from dateutil.relativedelta import relativedelta

from app.data import get_countries, get_population, calc_factor, to_str


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

    date = to_str(datetime.now().date() - relativedelta(days=1))

    countries = [
        country for country in get_countries()
        if int(get_population(country['Country']) or 0) > 100000
    ]
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
    for country, factor, conf, sicked in data:
        pop = get_population(country)
        res.append((country, round(factor or 0, 1), pop, conf, sicked))

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
