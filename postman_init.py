import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', action='store', required=True, help="Username's user admin or staff")
parser.add_argument('-p', '--password', action='store', required=True, help='Password user')
args = parser.parse_args()


def post(data, route):
    for entry in data.values():
        response = requests.post(f"http://localhost:8000/{route}/",
                                 json=entry['body'], headers={"Authorization": token})

        d = response.json()
        if 'pk' in d:
            entry['pk'] = d['pk']

        print(f" - {entry['status']}  :  status code {response.status_code}  -  {str(response.json())[:50]}")


print("========================= Postman init =========================")

# Login
response_login = requests.post("http://localhost:8000/login/",
                               json={"username": args.username, "password": args.password})

token = f"Bearer {response_login.json()['access']}"

# --
users = {
        'Jean': {'status': 'Create user Jean',
                 'pk': 0,
                 'body': {'username': 'Jean',
                          'email': 'Jean@postman.com',
                          'password': 'test01234',
                          'first_name': 'Jeannot',
                          'last_name': 'Martimou',
                          'is_staff': 'True'}},

        'Mireille': {'status': 'Create user Mireille',
                     'pk': 0,
                     'body': {'username': 'Mireille',
                              'email': 'mireille37@postman.com',
                              'password': 'test01234',
                              'first_name': 'Mireille'}},

        'Sophie37': {'status': 'Create user Sophie37',
                     'pk': 0,
                     'body': {'username': 'Sophie37',
                              'email': 'sophie@postman.com',
                              'password': 'test01234',
                              'first_name': 'Sophie',
                              'last_name': 'Pilouti'}},

        'René': {'status': 'Create user René37',
                 'pk': 0,
                 'body': {'username': 'René',
                          'email': 'rene@postman.com',
                          'password': 'test01234',
                          'first_name': 'René',
                          'last_name': 'Namato'}}
        }

post(users, 'users')
print("=========================")

# --
user_groups = {
        'Jean-manager': {'request': 'put',
                         'route_extra': 'set_manager',
                         'status': 'Set group manager to Jean',
                         'user': 'Jean'},

        'Mireille-sales': {'request': 'put',
                           'route_extra': 'set_sales',
                           'status': 'Set group sales to Mireille',
                           'user': 'Mireille'},
        }

for user in user_groups.values():
    response = requests.put(f"http://localhost:8000/users/{users[user['user']]['pk']}/{user['route_extra']}/",
                            headers={"Authorization": token})

    print(f" - {user['status']}  :  status code {response.status_code}  -  {str(response.json())[:70]}")

print("=========================")

# --
customers = {

        'SuperFrais': {'pk': 0,
                       'body': {'name': 'SuperFrais',
                                'email': 'hello@superfrais.com',
                                'phone': '+33578425474',
                                'assigned_user': users['Mireille']['pk']},
                       'status': 'Create customer SuperFrais'},

        'cogip': {'pk': 0,
                  'body': {'name': 'COGIP',
                           'email': 'hello@cogip.com',
                           'phone': '0256451548',
                           'assigned_user': users['René']['pk']},
                  'status': 'Create customer COGIP'},

        'dundermifflin': {'pk': 0,
                          'body': {'name': 'Dunder Mifflin',
                                   'email': 'hello@dm.com',
                                   'phone': '+33556565654',
                                   'assigned_user': users['Mireille']['pk']},
                          'status': 'Create customer Dunder Mifflin'},
        }

post(customers, 'customers')
print("=========================")

# --
contracts = {

        'contractcogip1': {'pk': 0,
                           'body': {'amount': '1000.00',
                                    'information': 'blabla',
                                    'customer': customers['cogip']['pk'],
                                    'date_signed': '2022-12-24'},
                           'status': 'Create contract with cogip'},

        'contractcogip2': {'pk': 0,
                           'body': {'amount': '5555.55',
                                    'information': 'bliblibli',
                                    'customer': customers['cogip']['pk'],
                                    'date_signed': '2023-01-12'},
                           'status': 'Create second contract with cogip'},

        'contractdundermifflin': {'pk': 0,
                                  'body': {'amount': '77777.77',
                                           'information': 'blublulbu',
                                           'customer': customers['dundermifflin']['pk']},
                                  'status': 'Create unsigned contract with Dunder Mifflin'},
        }

post(contracts, 'contracts')
print("=========================")

# --
events = {

        'eventcogip1': {'pk': 0,
                        'body': {'name': 'Cogip creation',
                                 'information': 'louloulou',
                                 'contract': contracts['contractcogip1']['pk'],
                                 'assigned_user': users['Sophie37']['pk'],
                                 'date': '2023-05-24'},
                        'status': 'Create event with cogip'},

        'eventcogip2': {'pk': 0,
                        'body': {'name': 'Cogip creation (after)',
                                 'information': 'lililililili',
                                 'contract': contracts['contractcogip1']['pk'],
                                 'assigned_user': users['Jean']['pk'],
                                 'date': '2023-05-24'},
                        'status': 'Create second event with cogip'},

        'eventcogip3': {'pk': 0,
                        'body': {'name': 'Cogip first baby',
                                 'information': 'lalalalalala',
                                 'contract': contracts['contractcogip2']['pk'],
                                 'assigned_user': users['Sophie37']['pk'],
                                 'date': '2023-05-24'},
                        'status': 'Create event contract 2 with cogip'},
        }

post(events, 'events')
print("=========================")
