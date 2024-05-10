import querys
from db_manager import *
from querys import *
import datetime


class User:
    query_manager = QueryManager("users", db_config, DatabaseManager)

    def __init__(self, user_id, name, last_name, user_name, password, wallet_balance=0.0):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password
        self.wallet_balance = wallet_balance

    def increase_balance(self, value):
        self.wallet_balance += value
        self.query_manager.update(
            {"wallet_balance": str(self.wallet_balance)},
            f"user_id={self.user_id}"
        )

    def decrease_balance(self, value):
        if self.wallet_balance < value:
            raise ValueError(" YOU NEED MORE MONEY")

        self.wallet_balance -= value
        self.query_manager.update(
            {"wallet_balance": str(self.wallet_balance)},
            f"user_id={self.user_id}"
        )

    @classmethod
    def login(cls, username, password):
        users = cls.query_manager.select(
            ["user_id", "name", "last_name", "username", "password", "wallet_balance"],
            f"username='{username}' and password='{password}'"
        )
        if users:
            return cls(*users[-1])
        else:
            raise ValueError("invalid username and password")

    @classmethod
    def register(cls, name, last_name, user_name, password):
        users = cls.query_manager.select(
            ["username"],
            f"username='{user_name}'"
        )
        if not users:
            user = cls.query_manager.insert(
                {
                    "name": name,
                    "last_name": last_name,
                    "username": user_name,
                    "password": password,
                    "wallet_balance": '0'
                }, "user_id"
            )
            ids = user[0][0]

            return cls(ids, name, last_name, user_name, password)
        else:
            raise ValueError(" this username already exists")

    def __str__(self):
        return f"{self.user_name},{self.wallet_balance}"

    def show_trip(self):
        # ticket_id,origins,destinations,date,price,type
        user_trips = self.query_manager.join(
            ["ticket_id",
             "origin",
             "destination",
             "price",
             "type",
             "trip_date"],
            "ticket",
            "trip",
            "trip_id",
            "trip_id",
            f"user_id={self.user_id}"
        )
        for trip in user_trips:
            print(f" ticket={trip[0]}"
                  f",origin={trip[1]},"
                  f"destination={trip[2]},"
                  f"price={trip[3]}, "
                  f"type={trip[4]}"
                  f"date={trip[5]}")


class Trip:
    query_manager = QueryManager("trip", db_config, DatabaseManager)
    trips = []

    def __init__(self, trip_id, origin, destination, trip_date, price):
        self.trip_id = trip_id
        self.origin = origin
        self.destination = destination
        self.trip_date = trip_date
        self.price = price

    @classmethod
    def add_trip(cls, origin, destination, trip_date, price):
        select_trip = cls.query_manager.select(
            ['destination', 'trip_date'],
            f"destination = '{destination}' AND trip_date ='{trip_date}'")
        if not select_trip:
            trips = cls.query_manager.insert({
                "origin": origin,
                "destination": destination,
                "trip_date": trip_date,
                "price": price

            }, "trip_id")
            trip_id = trips[0][0]

            new_trip = cls(trip_id, origin, destination, trip_date, price)
            cls.trips.append(new_trip)
            return new_trip
        else:
            raise ValueError("THIS trip already exist")

    @classmethod
    def load_trips(cls):
        trips = cls.query_manager.select(
            ['trip_id', 'origin', 'destination', 'trip_date', 'price'],
            f"trip_date>'{datetime.datetime.now()}'"
        )
        loads = [cls(*trip) for trip in trips]
        cls.trips.extend(loads)
        return cls.trips

    def __str__(self):
        return (f"{self.trip_id}\t"
                f"{self.origin}\t"
                f"{self.destination}\t"
                f"{self.price}\t"
                f"{self.trip_date}")

    @classmethod
    def get_trip(cls, trip_id):
        filtered_data = list(filter(lambda x: x.trip_id == trip_id, cls.trips))
        if filtered_data:
            return filtered_data[0]
        else:
            raise ValueError("not found...")


class Ticket:
    CASH_TYPE = "cash"
    CREDIT_TYPE = "credit"
    ticket_types = [CASH_TYPE, CREDIT_TYPE]
    all_ticket = []
    query_manager = QueryManager("ticket", db_config, DatabaseManager)

    def __init__(self, ticket_id, user: User, trip: Trip, trip_type):
        self.ticket_id, self.user, self.trip, self.trip_type = \
            ticket_id, user, trip, trip_type

    @classmethod
    def add_ticket(cls, user_id, trip_id, type):
        insert_ticket = cls.query_manager.insert({
            "user_id": user_id,
            "trip_id": trip_id,
            "type": type

        }, "ticket_id")
        ticket_id = insert_ticket[0][0]
        return cls(ticket_id, user_id, trip_id, type)

    @classmethod
    def buy_ticket(cls, user: User, trip: Trip, type):
        if type == cls.CREDIT_TYPE:
            user.decrease_balance(trip.price)

        new_ticket = cls.add_ticket(user.user_id, trip.trip_id, type)
        cls.all_ticket.append(new_ticket)

    @classmethod
    def load_ticket(cls):
        tickets = cls.query_manager.select(
            ['ticket_id', 'user_id', 'trip_id', 'type'])
        loads = [cls(*ticket) for ticket in tickets]
        cls.all_ticket.extend(loads)
        return cls.all_ticket
