from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()

    # user = User()
    # user.surname = "Scott"
    # user.name = "Ridley"
    # user.age = 21
    # user.position = "captain"
    # user.speciality = "research engineer"
    # user.address = "module_1"
    # user.email = "scott_chief@mars.org"
    # user.hashed_password = "cap"
    # session.add(user)

    # job = Jobs()
    # job.team_leader = 1
    # job.job = 'deployment of residential modules 1 and 2'
    # job.work_size = 15
    # job.collaborators = '2, 3'
    # job.is_finished = False
    # session.add(job)

    cap = User()
    cap.surname = "Scott"
    cap.name = "Ridley"
    cap.age = 21
    cap.position = "captain"
    cap.speciality = "research engineer"
    cap.address = "module_1"
    cap.email = "scott_chief@mars.org"

    nav = User()
    nav.surname = "Watny"
    nav.name = "Mark"
    nav.age = 25
    nav.position = "rover navigator"
    nav.speciality = "navigator"
    nav.address = "module_2"
    nav.email = "mark_wanty@mars.org"

    astro1 = User()
    astro1.surname = "Weir"
    astro1.name = "Andy"
    astro1.age = 49
    astro1.position = "scientist"
    astro1.speciality = "climatologist"
    astro1.address = "module_2"
    astro1.email = "andy_weir@mars.org"

    astro2 = User()
    astro2.surname = "Sanders"
    astro2.name = "Teddy"
    astro2.age = 41
    astro2.position = "NASA director"
    astro2.speciality = "tourist"
    astro2.address = "module_2"
    astro2.email = "teddy_sanders@mars.org"

    session.add(cap)
    session.add(nav)
    session.add(astro1)
    session.add(astro2)

    session.commit()

    # app.run()


if __name__ == '__main__':
    main()
