import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text

def best_tours():
    soup = BeautifulSoup(get_html('https://www.bgoperator.ru/'), 'lxml')
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

    return best