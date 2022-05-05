from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from sqlalchemy import func, and_

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

    astro4 = User()
    astro4.surname = "House"
    astro4.name = "Gregory"
    astro4.age = 49
    astro4.position = "chief medical officer"
    astro4.speciality = "therapist"
    astro4.address = "module_3"
    astro4.email = "house_gregory@mars.org"

    session.add(cap)
    session.add(nav)
    session.add(astro1)
    session.add(astro2)
    session.add(astro3)
    session.add(astro4)
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
    exploration.is_finished = True

    development = Jobs()
    development.team_leader = astro2.id
    development.job = 'Development of a managment system'
    development.work_size = 5
    development.collaborators = '5'
    development.is_finished = False

    development = Jobs()
    development.team_leader = astro4.id
    development.job = 'Warehouse organization'
    development.work_size = 7
    development.collaborators = '3, 4'
    development.is_finished = False

    air = Jobs()
    air.team_leader = astro4.id
    air.job = 'analysis of atmospheric air samples'
    air.work_size = 5
    air.collaborators = '3, 5, 4'
    air.is_finished = False

    maintenance = Jobs()
    maintenance.team_leader = astro4.id
    maintenance.job = 'Mars Rover maintenance'
    maintenance.work_size = 10
    maintenance.collaborators = '1, 4'
    maintenance.is_finished = False

    session.add(job)
    session.add(maintenance)
    session.add(air)
    session.add(exploration)
    session.add(development)

    dep = Department()
    dep.email = 'geological_exploration@mars.org'
    dep.title = 'Департамент геологической разведки'
    dep.members = '2, 4'
    dep.chief_id = 1

    dep2 = Department()
    dep2.email = 'technical_support@mars.org'
    dep2.title = 'Департамент технического обеспечения'
    dep2.members = '3, 5'
    dep2.chief_id = 6

    session.add(dep)
    session.add(dep2)

    session.commit()
    # jobs = [
    #         "<Job> deployment of residential modules 1 and 2",
    #         "<Job> exploration of mineral resources",
    #         "<Job> development of a management system",
    #         "<Job> analysis of atmospheric air samples",
    #         "<Job> Mars Rover maintenance",
    #         "<Job> search for water below the surface",
    #         "<Job> preventive vaccinations of the crew",
    #         "<Job> testing life system",
    #         "<Job> installation of radiation protection",
    #         "<Job> installing a long-distance communication antenna",
    #         "<Job> searching green men"
    # ]
    # departs = [
    #     "<Department> 1 Department of geological exploration geo@mars.org",
    #     "<Department> 2 Department of biological research bio@mars.org",
    #     "<Department> 3 Department of construction build@mars.org",
    #     "<Department> 4 Department of transportation transport@mars.org",
    #     "<Department> 5 department of terraforming terra@mars.org"
    # ]



@app.route('/')
@app.route('/jobs')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


@app.route('/register')
def register():
    return render_template('register.html')


def team_leaders():
    session = db_session.create_session()
    jobs_collaborators = {}
    for job in session.query(Jobs).all():
        try:
            jobs_collaborators[len(job.collaborators)].append(job.id)
        except KeyError:
            jobs_collaborators[len(job.collaborators)] = [job.id]
    ids = list(jobs_collaborators[sorted(jobs_collaborators, reverse=True)[0]])
    for job in session.query(Jobs).filter(Jobs.id.in_(ids)):
        responsible = session.query(User).filter(User.id == job.team_leader).first()
        print(responsible.name, responsible.surname, sep=" ")


def update_task():
    session = db_session.create_session()
    users = session.query(User).filter(User.address.like("%2%"), User.age < 45)
    users.update({User.address: "module_3"}, synchronize_session=False)
    session.commit()


def department_task():
    session = db_session.create_session()
    department = session.query(Department).filter(Department.id == 1).first()
    members = department.members.split(', ')
    jobs_work_size = {}
    for member in members:
        jobs = session.query(Jobs).filter(Jobs.collaborators.like("%" + member + "%"))
        for job in jobs:
            try:
                jobs_work_size[member] += job.work_size
            except KeyError:
                jobs_work_size[member] = job.work_size
    active_members = []
    for item in jobs_work_size:
        if jobs_work_size[item] > 25:
            active_members.append(item)
    users = session.query(User).filter(User.id.in_([int(elem) for elem in active_members]))
    for user in users:
        print(user.name, user.surname)
    # qry = session.query(func.sum(Jobs.work_size)).filter(Jobs.collaborators.like("%4%"))
    # print(qry)
    # for res in qry:
    #     print(res)
    # users = session.query(User).filter(User.id.in_(members)).all()
    # print(users)


def main():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()

    users = session.query(User).all()
    if not users:
        prep_db(session)

    # team_leaders()
    # update_task()
    department_task()

    app.run()


if __name__ == '__main__':
    main()
