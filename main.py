from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def prep_db(session):
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

    astro3 = User()
    astro3.surname = "Sigourney"
    astro3.name = "Weaver"
    astro3.age = 30
    astro3.position = "Secondary pilot"
    astro3.speciality = "warrant officer"
    astro3.address = "module_2"
    astro3.email = "weaver_sigourney@mars.org"

    session.add(cap)
    session.add(nav)
    session.add(astro1)
    session.add(astro2)
    session.add(astro3)
    session.commit()

    job = Jobs()
    job.team_leader = cap.id
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False

    exploration = Jobs()
    exploration.team_leader = astro1.id
    exploration.job = 'Exploration of mineral resources'
    exploration.work_size = 15
    exploration.collaborators = '4, 3'
    exploration.is_finished = False

    development = Jobs()
    development.team_leader = astro2.id
    development.job = 'Development of a managment system'
    development.work_size = 25
    development.collaborators = '5'
    development.is_finished = False

    session.add(job)
    session.add(exploration)
    session.add(development)

    session.commit()


@app.route('/')
@app.route('/jobs')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


def main():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()

    users = session.query(User).all()
    if not users:
        prep_db(session)

    # for user in session.query(User).filter(User.address.like("module_2"), User.speciality.notilike("%tourist%"), \
    #                                        User.position.notilike("%navigator%")):
    #     print(user.id)
    app.run()


if __name__ == '__main__':
    main()
