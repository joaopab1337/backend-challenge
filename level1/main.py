from datetime import datetime
import json


def read_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def write_json(data):
    with open('data/output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return 0


def days_between(d1, d2):
    d1 = datetime.strptime(d1, '%Y-%m-%d')
    d2 = datetime.strptime(d2, '%Y-%m-%d')
    return abs((d2 - d1).days)


class Car:
    def __init__(self, id, price_per_day, price_per_km):
        self.id = id
        self.price_per_day = price_per_day
        self.price_per_km = price_per_km


class Rent:
    def __init__(self, id, car, start_date, end_date, distance):
        self.id = id
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.distance = distance

    def time_rate(self):
        days = days_between(self.start_date, self.end_date)
        return days * self.car.price_per_day

    def distance_rate(self):
        return self.distance * self.car.price_per_km

    def rental_price(self):
        return self.distance_rate() + self.time_rate()


def main():
    data = read_json('data/input.json')

    # Models instances

    cars = [
        Car(
            car.get('id'),
            car.get('price_per_day'),
            car.get('price_per_km')
        )
        for car in data.get('cars')
    ]

    rentals = [
        Rent(
            rent.get('id'),
            next(car for car in cars if car.id == rent.get('car_id')),
            rent.get('start_date'),
            rent.get('end_date'),
            rent.get('distance')
        )
        for rent in data.get('rentals')
    ]

    # Bill generation

    rental_bills = {
        'rentals':
            [
                {'id': rent.id, 'price': rent.rental_price()}
                for rent in rentals
            ]
    }

    write_json(rental_bills)

    return 0


main()
