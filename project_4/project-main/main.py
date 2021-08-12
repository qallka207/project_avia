from flask import Flask, render_template, request
import db_session
import tyrs
import datetime

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
@app.route('/best')
def best():
    r = requests.get('https://www.bgoperator.ru/')
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, 'lxml')
    best_offers = soup.find_all("div", {"class": "best-offers__item"})
    best = []

    for best_offer in best_offers:
        strana = {}

        country = best_offer.find("div", {"class": "offer__title"}).string
        strana["country"] = country

        offers = best_offer.find("ul", {"class": "offer__price-list ul-nostyle"}).find_all("li", {"class": "offer__item"})

        tours = []
        for offer in offers:
            tour = {}

            name = offer.find("div", {"class": "offer__price"}).find("div", {"class": "offer__name"}).string
            tour["name"] = name

            info = offer.find("div", {"class": "offer__info"})
            info_text = "{date}, {stars} звезды, {food}".format(
                date=info.text.split(',')[0].strip()[0:12] + info.text.split(',')[0].strip()[13:],
                stars=info.text.split(',')[1].strip(),
                food=info.text.split(',')[2].strip())
            tour["info"] = info_text

            price = offer.find("div", {"class": "offer__price"}).find("div", {"class": "offer__cost"}).text
            price = price[0:-2] + " p."
            tour["price"] = price

            tours.append(tour)
        strana["tours"] = tours
        best.append(strana)

    return render_template("best.html", tours=best)


@app.route('/popular')
def popular():
    return render_template("popular.html")


@app.route('/find', methods=['POST', 'GET'])
def find():
    if request.method == 'GET':
        return render_template("find.html", pos=0, ot="Россия", ku="Без разницы", d1="", d2="", dat1=datetime.date.today(), dat2=datetime.date.today()+datetime.timedelta(days=365), lev="Любой", pit="Любой", st1="", st2="")

    elif request.method == 'POST':
        otkuda = request.form['otkuda']
        kuda = request.form['kuda']
        dni1 = request.form['dni1']
        if dni1=="":
            dni1 = 1
        dni2 = request.form['dni2']
        if dni2=="":
            dni2 = 21
        data1 = request.form['data1']
        data_d1 = datetime.date(int(data1[0:4]), int(data1[5:7]), int(data1[8:10]))
        data2 = request.form['data2']
        data_d2 = datetime.date(int(data2[0:4]), int(data2[5:7]), int(data2[8:10]))
        level = request.form['level']
        pitanie = request.form['pitanie']
        cena1 = request.form['cena1']
        if cena1=="":
            cena1 = 0
        cena2 = request.form['cena2']
        if cena2=="":
            cena2 = 200000

        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        name = session.query(tyrs.Tyrs).filter(tyrs.Tyrs.Otkuda==otkuda).filter((tyrs.Tyrs.Kuda==kuda) | (kuda=="Без разницы")).\
            filter(data_d1<=tyrs.Tyrs.Data).filter(tyrs.Tyrs.Data<=data_d2).\
            filter(int(dni1)<=tyrs.Tyrs.Dni).filter(tyrs.Tyrs.Dni<=int(dni2)).filter((tyrs.Tyrs.Level==level) | (level=="Любой")).\
            filter((tyrs.Tyrs.Pitanie==pitanie) | (pitanie=="Любой")).filter(int(cena1)<=tyrs.Tyrs.Cena).filter(tyrs.Tyrs.Cena<=int(cena2))
        session.commit()
        return render_template("find.html", pos=1, tyrs=name, ot=otkuda, ku=kuda, d1=dni1, d2=dni2, dat1=data1, dat2=data2, lev=level, pit=pitanie, st1=cena1, st2=cena2)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')