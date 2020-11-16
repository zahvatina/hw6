import json


class ColorizeMixin:
    def wrapp(self, text):
        return "\033[1;{};40m{}".format(self.repr_color_code, text)


class AdvertMixin(object):
    def __init__(self, mapping, lvl=0):
        d = mapping
        if type(d) is str:
            d = json.loads(d)
        if lvl == 0:
            if 'price' not in d:
                d['price'] = 0.0
            if d['price'] < 0.0:
                raise ValueError('must be >= 0')
        self.convert_json__(d)

    def convert_json__(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = AdvertMixin(value, lvl=1)
            self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


class Advert(AdvertMixin, ColorizeMixin):
    def __init__(self, mapping):
        super(Advert, self).__init__(mapping)
        self.repr_color_code = 32  # green

    def __repr__(self):
        return self.wrapp(f'{self.title} | {self.price} ₽')


lesson_str = """{
"title": "python",
"price": 1.0,
"location": {
"address": "город Москва, Лесная, 7",
"metro_stations": ["Белорусская"]
}
}"""

x = Advert(lesson_str)
print(x)
print(x.price)
