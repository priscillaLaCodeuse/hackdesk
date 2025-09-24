from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_mail import Mail, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from models import Base, User, Client, Project, Task

import os

load_dotenv()

# ============
# Config Flask
# ============
app = Flask('__name__')
app.secret_key = os.environ.get('SECRET_KEY')


# =================
# Config SQLAlchemy
# =================
db = os.environ.get('DB_PATH')

engine = create_engine(db)

try:
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print("DB success!")

except Exception as ex:
    print(ex)


# ==================
# Config Flask-Login
# ==================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

# ==================
# Config Flask-Mail
# ==================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_ADDRESS")
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD_MAIL')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("EMAIL_ADDRESS")

mail = Mail(app)


# ======
# Routes
# ======
@app.route('/', methods=["GET", "POST"])
def index():
    # Si l'utilisateur est déjà connecté
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    # Si l'utilisateur soumet le formulaire de connexion
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        # Vérifier que les champs sont remplis
        if not email:
            flash("L'email est obligatoire.", "error")
            return redirect(url_for('index'))
        if not password:
            flash("Le mot de passe est obligatoire.", "error")
            return redirect(url_for('index'))
        
        user = session.query(User).filter_by(email=email).first()

        # Si l'utilisateur existe et que le mot de passe correspond
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        elif not user:
            flash("Cet email est inconnu.", "error")
            return redirect(url_for('index'))
        else:
            flash("Mot de passe incorrect", "error")
            return redirect(url_for('index'))
        
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "POST":
        lastname = request.form.get("lastname").upper()
        firstname = request.form.get("firstname").capitalize()
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Vérifier que tous les champs sont remplis
        if not lastname:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('register'))
        if not firstname:
            flash("Le prénom est obligatoire.", "error")
            return redirect(url_for('register'))
        if not email:
            flash("L'email est obligatoire.", "error")
            return redirect(url_for('register'))
        if not password:
            flash("Le mot de passe est obligatoire.", "error")
            return redirect(url_for('register'))
        if not confirmation:
            flash("La confirmation est obligatoire.", "error")
            return redirect(url_for('register'))
        
        # Vérifier que le mot de passe et la confirmation correspondent
        if password != confirmation:
            flash("Le mot de passe et la confirmation ne correspondent pas.", "error")
            return redirect(url_for('register'))

        # Vérifier que l'email n'existe pas dans la base de données
        check_user = session.query(User).filter_by(email=email).first()

        # Si l'utilisateur n'existe pas dans la base de données
        if not check_user:
            # Crypter le mot de passe
            hashed_password = generate_password_hash(password)

            # Ajouter le nouvel utilisateur
            new_user = User(
                lastname=lastname,
                firstname=firstname,
                email=email,
                password=hashed_password
            )

            session.add(new_user)
            session.commit()

            msg = Message("Bienvenue sur HackDesk", recipients=[email])
            msg.html = render_template("emails/welcome.html", firstname=firstname, lastname=lastname)
            mail.send(msg)

            # Connecter l'utilisateur
            login_user(new_user)

            return redirect(url_for('dashboard'))
        
        else:
            # Informer que le compte existe déjà
            flash("Un compte existe déjà avec cette adresse email. Connectez-vous!", "error")
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/reinitialisation-password', methods=["GET", "POST"])
def reinitialisationPassword():
    if request.method == "POST":
        lastname = request.form.get("lastname").upper()
        firstname = request.form.get("firstname").capitalize()
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Vérifier que tous les champs sont remplis
        if not lastname:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('reinitialisationPassword'))
        if not firstname:
            flash("Le prénom est obligatoire.", "error")
            return redirect(url_for('reinitialisationPassword'))
        if not email:
            flash("L'email est obligatoire.", "error")
            return redirect(url_for('reinitialisationPassword'))
        if not password:
            flash("Le mot de passe est obligatoire.", "error")
            return redirect(url_for('reinitialisationPassword'))
        if not confirmation:
            flash("La confirmation est obligatoire.", "error")
            return redirect(url_for('reinitialisationPassword'))

        # Vérifier que le mot de passe et la confirmation correspondent
        if password != confirmation:
            flash("Le mot de passe et la confirmation ne correspondent pas.", "error")
            return redirect(url_for('reinitialisationPassword'))
        
        # Vérifier si toutes les informations données sont justes
        user = session.query(User).filter(lastname==lastname, firstname==firstname, email==email).first()

        # Si c'est juste, modifier le mot de passe
        if user:

            hashed_password = generate_password_hash(password)
            user.password = hashed_password

            session.commit()
            
            # Envoyer un email à l'utilisateur pour l'informer du changement de mot de passe
            msg = Message("Réinitialisation de votre mot de passe", recipients=[email])
            msg.html = render_template("emails/reinitialisation.html", firstname=firstname, lastname=lastname)
            mail.send(msg)

            flash("Le mot de passe a bien été modifié.", "success")

            login_user(user)

        return redirect(url_for('index'))


    return render_template('reinitialisation-password.html')


# ================
# Routes Dashboard
# ================
@app.route('/dashboard')
@login_required
def dashboard():
    total_projects = session.query(Project).filter_by(user_id=current_user.id).count()
    cours_projects = session.query(Project).filter_by(user_id=current_user.id, status="En cours").count()
    end_projects = session.query(Project).filter_by(user_id=current_user.id, status="Terminé").count()
    total_clients =session.query(Client).filter_by(user_id=current_user.id).count()
    
    return render_template('dashboard/dashboard.html', total_projects=total_projects, cours_projects=cours_projects, end_projects=end_projects, total_clients=total_clients)


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    user = session.query(User).filter_by(id=current_user.id).first()

    if request.method == "POST":
        lastname = request.form.get("lastname").upper()
        firstname = request.form.get("firstname").capitalize()
        email = request.form.get("email").lower()

        if not lastname:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('profile'))
        if not firstname:
            flash("Le prénom est obligatoire.", "error")
            return redirect(url_for('profile'))
        if not email:
            flash("L'email est obligatoire.", "error")
            return redirect(url_for('profile'))

        user.lastname = lastname
        user.firstname = firstname
        user.email = email

        session.commit()

        return redirect(url_for('profile'))
    
    return render_template('dashboard/profile.html', user=user)

@app.route('/delete-account', methods=['GET', 'POST'])
@login_required
def deleteAccount():
    if request.method == "POST":
        user = session.query(User).filter_by(id=current_user.id).first()

        if user:
            session.delete(user)
            session.commit()

            flash("Compte supprimé avec succès.", "success")

        else:
            flash("Une erreur s'est produite. Veuillez réessayer s'il-vous-plaît.", "error")

        return redirect(url_for('index'))


@app.route('/projects')
@login_required
def projects():
    projects = session.query(Project).filter_by(user_id=current_user.id).all()

    return render_template('dashboard/projects.html', projects=projects)


@app.route('/add-a-project', methods=["GET", "POST"])
@login_required
def addAProject():
    clients = session.query(Client).filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        name_project = request.form.get("name_project")
        description = request.form.get("description")
        url = request.form.get("url")
        hosting_server = request.form.get("hosting_server")
        status = request.form.get("status")
        hourly_rate = request.form.get("hourly_rate")
        client = request.form.get("client")

        client = int(client)

        # Vérifier que tous les champs sont remplis
        if not name_project:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('addAProject'))
        if not description:
            flash("La description est obligatoire.", "error")
            return redirect(url_for('addAProject'))
        if not url:
            url = "Aucune"
        if not hosting_server:
            hosting_server = "Aucun"
        if not status:
            flash("Le statut est obligatoire.", "error")
            return redirect(url_for('addAProject'))
        if not hourly_rate:
            hourly_rate = 0
        if not client:
            flash("Le client est obligatoire.", "error")
            return redirect(url_for('addAProject'))
        
        newProject = Project(
            name_project=name_project,
            description=description,
            url=url,
            hosting_server=hosting_server,
            status=status,
            hourly_rate=hourly_rate,
            client_id=client,
            user_id=current_user.id
        )

        session.add(newProject)
        session.commit()
        
        return redirect(url_for('projects'))

    return render_template('dashboard/add-a-project.html', clients=clients)


@app.route('/view-project/<int:project_id>', methods=["GET", "POST"])
@login_required
def viewProject(project_id):
    project = session.query(Project).filter_by(id=project_id).first()
    tasks = (
        session.query(Task)
        .join(Project)
        .filter(Project.id == project_id)
        .all()
    )
    return render_template('dashboard/view-project.html', project=project, tasks=tasks)


@app.route('/edit-project/<int:project_id>', methods=["GET", "POST"])
@login_required
def editProject(project_id):
    project = session.query(Project).filter_by(id=project_id).first()

    if request.method == "POST":
        name_project = request.form.get("name_project")
        description = request.form.get("description")
        url = request.form.get("url")
        hosting_server = request.form.get("hosting_server")
        status = request.form.get("status")
        hourly_rate = request.form.get("hourly_rate")
        client = request.form.get("client")

        # Vérifier que tous les champs sont remplis
        if not name_project:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('editProject', project_id=project_id))
        if not description:
            flash("La description est obligatoire.", "error")
            return redirect(url_for('editProject', project_id=project_id))
        if not url:
            flash("L'URL est obligatoire.", "error")
            return redirect(url_for('editProject', project_id=project_id))
        if not hosting_server:
            flash("Le serveur d'hébergement est obligatoire.", "error")
            return redirect(url_for('editProject', project_id=project_id))
        if not status:
            flash("Le statut est obligatoire.", "error")
            return redirect(url_for('editProject', project_id=project_id))
        if not hourly_rate:
            flash("Le tarif horaire est obligatoire.", "error")
            return redirect(url_for('editProject', project_id=project_id))
        if not client:
            flash("Le client est obligatoire.", "error")
            return redirect(url_for('editProject', project_id=project_id))
        
        # Mettre à jour les informations
        project.name_project=name_project
        project.description=description
        project.url=url
        project.hosting_server=hosting_server
        project.status=status
        project.hourly_rate=hourly_rate
        project.client_id=client

        session.commit()
        
        flash("Les modifications ont bien été sauvegardées.", "success")
        return redirect(url_for('editProject', project_id=project_id))
    
    return render_template('dashboard/edit-project.html', project=project)


@app.route('/delete-project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def deleteProject(project_id):
    if request.method == "POST":
        project = session.query(Project).filter_by(id=project_id).first()

        if project:
            session.delete(project)
            session.commit()

            flash("Projet supprimé avec succès.", "success")

        else:
            flash("Une erreur s'est produite. Veuillez réessayer s'il-vous-plaît.", "error")

        return redirect(url_for('projects'))


@app.route('/tasks')
@login_required
def tasks():
    tasks = (
        session.query(Task)
        .join(Project)
        .filter(Project.user_id == current_user.id)
        .all()
    )

    return render_template('dashboard/tasks.html', tasks=tasks)


@app.route('/add-a-task', methods=["GET", "POST"])
@login_required
def addATask():
    projects = session.query(Project).filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        name_task = request.form.get("name_task")
        status = request.form.get("status")
        time_spent = request.form.get("time_spent")
        project = request.form.get("project")

        project = int(project)

        # Vérifier que tous les champs sont remplis
        if not name_task:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('addAProject'))
        if not status:
            flash("Le statut est obligatoire.", "error")
            return redirect(url_for('addAProject'))
        if not time_spent:
            time_spent = 0

        if not project or project == 0:
            flash("Le projet est obligatoire.", "error")
            return redirect(url_for('addAProject'))

        newTask = Task(
            name_task=name_task,
            status=status,
            time_spent=time_spent,
            project_id=project
        )

        session.add(newTask)
        session.commit()
        
        return redirect(url_for('tasks'))

    return render_template('dashboard/add-a-task.html', projects=projects)


@app.route('/edit-task/<int:task_id>', methods=["GET", "POST"])
@login_required
def editTask(task_id):
    task = session.query(Task).filter_by(id=task_id).first()

    if request.method == "POST":
        name_task = request.form.get("name_task")
        status = request.form.get("status")
        time_spent = request.form.get("time_spent")

        # Vérifier que tous les champs sont remplis
        if not name_task:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('editTask', task_id=task_id))
        if not status:
            flash("Le statut est obligatoire.", "error")
            return redirect(url_for('editTask', task_id=task_id))
        if not time_spent:
            flash("Le temps passé est obligatoire.", "error")
            return redirect(url_for('editTask', task_id=task_id))

        # Mettre à jour les informations
        task.name_task=name_task
        task.status=status
        task.time_spent=time_spent

        session.commit()
        
        flash("Les modifications ont bien été sauvegardées.", "success")
        return redirect(url_for('tasks'))
    
    return render_template('dashboard/edit-task.html', task=task)


@app.route('/delete-task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def deleteTask(task_id):
    if request.method == "POST":
        task = session.query(Task).filter_by(id=task_id).first()

        if task:
            session.delete(task)
            session.commit()

            flash("Tâche supprimée avec succès.", "success")

        else:
            flash("Une erreur s'est produite. Veuillez réessayer s'il-vous-plaît.", "error")

        return redirect(url_for('tasks'))


@app.route('/clients')
@login_required
def clients():
    clients = session.query(Client).filter_by(user_id=current_user.id).all()

    return render_template('dashboard/clients.html', clients=clients)


@app.route('/add-a-client', methods=["GET", "POST"])
@login_required
def addAClient():
    if request.method == "POST":
        lastname = request.form.get("lastname").upper()
        firstname = request.form.get("firstname").capitalize()
        enterprise = request.form.get("enterprise")
        address = request.form.get("address")
        zip_code = request.form.get("zip_code")
        city = request.form.get("city").capitalize()
        country = request.form.get("country").capitalize()
        phone_number = request.form.get("phone_number")
        email = request.form.get("email").lower()
        note = request.form.get("note")

        # Vérifier que tous les champs sont remplis
        if not lastname:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not firstname:
            flash("Le prénom est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not enterprise:
            enterprise = ""
        if not address:
            address = ""
        if not zip_code:
            zip_code = ""
        if not city:
            city = ""
        if not country:
            country = ""
        if not phone_number :
            flash("Le numéro de téléphone est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not email :
            flash("L'email est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not note :
            note = ""
        
        # Ajouter le client
        newClient = Client(
            lastname=lastname,
            firstname=firstname,
            enterprise=enterprise,
            address=address,
            zip_code=zip_code,
            city=city,
            country=country,
            phone_number=phone_number,
            email=email,
            note=note,
            user_id=current_user.id
            
        )

        session.add(newClient)
        session.commit()
        
        return redirect(url_for('clients'))

    return render_template('dashboard/add-a-client.html')


@app.route('/view-client/<int:client_id>', methods=["GET", "POST"])
@login_required
def viewClient(client_id):
    client = session.query(Client).filter_by(id=client_id).first()
    projects = session.query(Project).filter_by(client_id=client_id).all()
    
    return render_template('dashboard/view-client.html', client=client, projects=projects)


@app.route('/edit-client/<int:client_id>', methods=["GET", "POST"])
@login_required
def editClient(client_id):
    client = session.query(Client).filter_by(id=client_id).first()

    if request.method == "POST":
        lastname = request.form.get("lastname").upper()
        firstname=request.form.get("firstname").capitalize()
        enterprise=request.form.get("enterprise")
        address=request.form.get("address")
        zip_code=request.form.get("zip_code")
        city=request.form.get("city").capitalize()
        country=request.form.get("country").capitalize()
        phone_number=request.form.get("phone_number")
        email=request.form.get("email").lower()
        note=request.form.get("note")

        # Vérifier que tous les champs sont remplis
        if not lastname:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not firstname:
            flash("Le prénom est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not enterprise:
            enterprise = ""
        if not address:
            address = ""
        if not zip_code:
            zip_code = ""
        if not city:
            city = ""
        if not country:
            country = ""
        if not phone_number :
            flash("Le numéro de téléphone est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not email :
            flash("L'email est obligatoire.", "error")
            return redirect(url_for('addAClient'))
        if not note :
            note = ""

        # Mettre à jour les informations
        client.lastname=lastname
        client.firstname=firstname
        client.enterprise=enterprise
        client.address=address
        client.zip_code=zip_code
        client.city=city
        client.country=country
        client.phone_number=phone_number
        client.email=email
        client.note=note

        session.commit()
        
        flash("Les modifications ont bien été sauvegardées.", "success")
        return redirect(url_for('clients'))
    
    return render_template('dashboard/edit-client.html', client=client)


@app.route('/delete-client/<int:client_id>', methods=['GET', 'POST'])
@login_required
def deleteClient(client_id):
    if request.method == "POST":
        client = session.query(Client).filter_by(id=client_id).first()

        if client:
            session.delete(client)
            session.commit()

            flash("Client supprimé avec succès.", "success")

        else:
            flash("Une erreur s'est produite. Veuillez réessayer s'il-vous-plaît.", "error")

        return redirect(url_for('clients'))

# ===
# Run
# ===
if __name__ == '__main__':
    app.run(debug=True)