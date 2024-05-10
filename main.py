from all_class import User, Trip, Ticket
import os

def user_menu():
    user = None
    while True:
        print("\n1-login\n2-rigerster\n3-exit\n")
        condition = input("enter:")
        if condition == "1":
            name = input("enter your name:")
            password = input("enter your password")
            user = User.login(name, password)

            break
        elif condition == "2":
            name = input("enter your name:")
            last_name = input("enter your lastname:")
            user_name = input("enter your username:")
            password = input("enter your password:")
            user = User.register(name, last_name, user_name, password)
            break
        elif condition == "3":
            print("bye...")
            break
    return user


def customer_menu(user):
    available_trips = Trip.load_trips()
    while True:
        print(
            "\n 1-show your trips"
            " \n2-buy ticket"
            "\n3-increase_balance"
            "\n4-exit")

        condition = input("enter:")
        match condition:
            case "1":
                user.show_trip()

            case "2":
                for trip in available_trips:
                    print(trip)
                trip_id = int(input("enter trip id:"))
                trip = Trip.get_trip(trip_id)
                ticket_type = input("enter your type for ticket")
                Ticket.buy_ticket(user, trip, ticket_type)
            case "3":

                user.increase_balance(int(input("enter wallet value :")))
                print("YOUR NEW BALANCE IS",user.wallet_balance)

            case _:
                print("bye...")
                break


def main_menu():
    try:
        user = user_menu()
        os.system('cls||clear')
        customer_menu(user)
        os.system('cls||clear')
    except Exception as e:
        print(f" you have {e}")


main_menu()