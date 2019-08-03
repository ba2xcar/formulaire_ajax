from flask import Flask, render_template, request, flash, url_for, redirect,session,send_file
import os
import psycopg2 as psy
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
import json
from flask import jsonify


""" def ConnexionDB():
    try:
        #Connexion à la base de données
        connection = psy.connect(user="postgres",password="",
                                host="localhost",
                                port="5432",
                                database="scolaire"
        )  
        return connection
    except (Exception) as error :
        print ("Problème de connexion au serveur PostgreSQL", error)
connection = ConnexionDB()
curseur = connection.cursor() """

app = Flask(__name__) #permet de localiser les ressources cad les templates
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/scolaireAlchemy'
app.secret_key = 'some_secret'
db = SQLAlchemy(app)
connection = db.session.connection()

#**************************************TABLE APPRENANT************************************
class Apprenant(db.Model):
    id = db.Column('id_app',db.Integer,primary_key = True)
    matricule = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    nom = db.Column(db.String(100))
    sexe = db.Column(db.String(100))
    date_naiss = db.Column(db.Date())
    lieu_naiss = db.Column(db.String(100))
    adresse = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tel = db.Column(db.String(100))

    def __init__(self, matricule, prenom, nom, sexe, date_naiss, lieu_naiss, adresse, email, tel):
        self.matricule = matricule
        self.prenom = prenom
        self.nom = nom
        self.sexe = sexe
        self.date_naiss = date_naiss
        self.lieu_naiss = lieu_naiss
        self.adresse = adresse
        self.email = email
        self.tel = tel
#**************************************TABLE INSCRIPTION************************************
class Inscription(db.Model):
    id = db.Column('id_ins',db.Integer, primary_key = True)
    date_ins = db.Column(db.Date())
    annee_aca = db.Column(db.String(100))
    id_app = db.Column(db.Integer, db.ForeignKey('Apprenant.id_app'))


    def __init__(self, date_ins, annee_aca, id_app):
        self.date_ins = date_ins
        self.annee_aca = annee_aca
        self.id_app = id_app
#**************************************TABLE FILIERE************************************
class Filiere(db.Model):
    id = db.Column('id_fil',db.Integer, primary_key = True)
    libelle = db.Column(db.String(100))

    def __init__(self, libelle):
        self.libelle = libelle
#**************************************TABLE CLASSE************************************
class Classe(db.Model):
    id = db.Column('id_classe',db.Integer, primary_key = True)
    libelle = db.Column(db.String(100))
    mont_ins = db.Column(db.Integer)
    mensualite = db.Column(db.Integer)
    id_fil = db.Column(db.Integer, db.ForeignKey('filiere.id_fil'))


    def __init__(self, libelle,mont_ins,mensualite,id_fil):
        self.libelle = libelle
        self.mont_ins = mont_ins
        self.mensualite = mensualite
        self.id_fil = id_fil
#**************************************ACCUEIL************************************
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':      
        student = Apprenant(request.form['matricule'],request.form['prenom'].strip(),request.form['nom'].strip(),request.form['sexe'],
                            request.form['date_naissance'],request.form['lieu_naissance'].strip(),
                            request.form['adresse'].strip(),request.form['email'].strip(),request.form['telephone'].strip())

        id_app=Apprenant.query.count()+1
        print(id_app)

        inscrire = Inscription(request.form['date_ins'],request.form['annee_ac'].strip(),id_app=id_app)
        db.session.add(student)
        db.session.add(inscrire)
        db.session.commit()
        return render_template("ajouter_apprenant.html")
    elif request.method == 'GET':
        #---------------------------------Génération matricule-------------------------------------
        date_actu=datetime.datetime.today().strftime('%Y')
        matricule = Apprenant.query.count()
        if matricule == 0:
            num=1
            val='-'+str(num)+'-'
            gen_mat = "SA"+val+str(date_actu)
        else:
            num=matricule+1
            val='-'+str(num)+'-'
            gen_mat="SA"+val+str(date_actu)

        #----------------------------------Génération Année Académique-----------------------------------
        mois=int(datetime.datetime.today().strftime('%m'))
        annee1=0
        annee2=0
        annee_academy=None
        if mois>=8:
            annee1 = int(datetime.datetime.today().strftime('%Y'))
            print(annee1)
            annee2 = annee1+1
            annee_academy = str(annee1)+"/"+str(annee2)
        else:
            annee1=int(datetime.datetime.today().strftime('%Y'))
            annee2=annee1-1
            annee_academy=str(annee2)+"/"+str(annee1)
        result=db.session.query(Filiere).all()
        res = Filiere.query.all()
        print(res)
        filieres=[]
        for row in result:
            ma_liste = [row.id, row.libelle]  
            filieres.append(ma_liste)  
        print(filieres)
        return render_template("ajouter_apprenant.html",gen_mat=gen_mat,annee_academy=annee_academy,filieres=filieres)


@app.route('/filiere&<string:ide>', methods = ['GET','POST'])
def action_filiere(ide):
    print(ide)
    data=[
        { "Prenom":"John" , "Nom":"Doe", "Age":"25" },
        { "Prenom":"Anna" , "Nom":"Smith", "Age":"34" },
        { "Prenom":"Peter" , "Nom":"Jones", "Age":"17" }
    ]
    classe = Classe.query.filter_by(id_fil=ide).all()
    liste_classe=[]
    for val in classe:
        mon_dict= { "id":val.id , "libelle":val.libelle }
        liste_classe.append(mon_dict)
    print(liste_classe)  

    return jsonify(liste_classe)

@app.route('/ancien')
def ancien():
    return render_template("accueil.html")
#*********************************************************************************

#***************************************AJOUT APPRENANT*******************************
@app.route('/inscription')
def ajouter_apprenant():
    requete_liste_promo = "SELECT id_promo,libelle FROM promotion WHERE date_debut>=DATE( NOW() )"
    curseur.execute(requete_liste_promo)
    result = curseur.fetchall()
    valeurs=result   

    requete_liste_matricule = "SELECT max(id_app) FROM apprenant"
    curseur.execute(requete_liste_matricule)
    result_matricule = curseur.fetchall()
    for mat in result_matricule:
        matricule=mat[0]    
    date_actu=datetime.datetime.today().strftime('%Y')

    if matricule == None:
        num=1
        val='-'+str(num)+'-'
        gen_mat = "SA"+val+str(date_actu)
    else:
        num=matricule+1
        val='-'+str(num)+'-'
        gen_mat="SA"+val+str(date_actu)
    user = session['username']
    return render_template("ajouter_apprenant.html",valeurs=valeurs,gen_mat=gen_mat,user=user)

#---------------------------------------------------------------------------------
@app.route('/scolarite/inscription', methods=["POST"])
def insertion_app():
    matricule = request.form["matricule"]
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    sexe = request.form["sexe"]
    date_naissance = request.form["date_naissance"]
    lieu_naissance = request.form["lieu_naissance"]
    adresse = request.form["adresse"]
    email = request.form["email"].lower()
    telephone = request.form["telephone"]
    promotion = request.form["promo"]
    statut = 'inscrit'
    data=(matricule,prenom,nom,sexe,date_naissance,lieu_naissance,adresse,email,telephone,promotion,statut)

    requete_libelle_promo = "SELECT telephone,email FROM apprenant"
    curseur.execute(requete_libelle_promo)
    apprenant = curseur.fetchall()
    control_app=False

    for app in apprenant:
        if app[0] == telephone or app[1].lower()==email.lower():
            control_app = True
            break
    if control_app == True:
        flash("WARNING : L'apprenant existe déjà")
        requete_liste_promo = "SELECT id_promo,libelle FROM promotion WHERE date_debut>DATE( NOW() )"
        curseur.execute(requete_liste_promo)
        result = curseur.fetchall()
        valeurs=result   

        requete_liste_matricule = "SELECT max(id_app) FROM apprenant"
        curseur.execute(requete_liste_matricule)
        result_matricule = curseur.fetchall()
        for mat in result_matricule:
            matric=mat[0]
        date_actu=datetime.datetime.today().strftime('%Y')

        if matric == None:
            num=1
            val='-'+str(num)+'-'
            gen_mat = "SA"+val+str(date_actu)
        else:
            num=matric+1
            val='-'+str(num)+'-'
            gen_mat="SA"+val+str(date_actu)
        user = session['username']
        return render_template("ajouter_apprenant.html",valeurs=valeurs,gen_mat=gen_mat,prenom=prenom,nom=nom,date_naissance=date_naissance,lieu_naissance=lieu_naissance,adresse=adresse,email=email,telephone=telephone,user=user)
    elif control_app == False: 
        requete_ajout_app = """INSERT INTO apprenant 
                            (matricule,prenom,nom,sexe,date_naissance,lieu_naissance,adresse,email,telephone,id_promo,statut) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        curseur.execute(requete_ajout_app,data)
        connection.commit() 
        flash("SUCCESS : Apprenant ajouté avec succès!!!")
        return redirect(url_for('ajouter_apprenant'))

#**********************************************************************************


#****************************************MODIFIER APPRENANT*********************************************
@app.route('/modifier&<string:id_data>', methods = ['GET','POST'])
def modifier(id_data):
    if request.method == 'GET':
        requete_ajout_app = """ select matricule,prenom,nom,sexe,date_naissance,lieu_naissance,adresse,email,telephone,
                                apprenant.id_promo,promotion.libelle from apprenant, promotion where
                                apprenant.id_promo = promotion.id_promo and matricule=%s"""
        data= (id_data,)
        curseur.execute(requete_ajout_app,data)
        result_up = curseur.fetchall()

        for val in result_up:
            data_promo=val[9]
            break

        requete_promo = "SELECT * FROM promotion WHERE id_promo!=%s "
        curseur.execute(requete_promo,(data_promo,))
        result_promo = curseur.fetchall()
        user = session['username']
        return render_template("modifier_apprenant.html",result_up=result_up,result_promo=result_promo,user=user)
    elif request.method == 'POST':
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        sexe = request.form["sexe"]
        date_naissance = request.form["date_naissance"]
        lieu_naissance = request.form["lieu_naissance"]
        adresse = request.form["adresse"]
        email = request.form["email"]
        telephone = request.form["telephone"]
        promotion = request.form["promo"]
        
        requete_libelle_promo = "select telephone,email from apprenant WHERE matricule!=%s "
        curseur.execute(requete_libelle_promo,(id_data,))
        apprenant = curseur.fetchall()
        control_app=False

        for app in apprenant:
            if app[0] == telephone and app[1].lower()==email.lower():
                control_app = True
                break
        if control_app == True:
            flash("l'apprenant existe déjà")
            print("l'utilisateur existe déjà")
            return redirect(url_for('index'))     
        else: 

            requete_up_app = """UPDATE apprenant SET prenom=%s, nom=%s, sexe=%s, date_naissance=%s, 
                            lieu_naissance=%s, adresse=%s, email=%s, telephone=%s, id_promo=%s
                            WHERE matricule=%s"""    
            data_up = (prenom,nom,sexe,date_naissance,lieu_naissance,adresse,email,telephone,promotion,id_data)
            curseur.execute(requete_up_app,data_up)
            connection.commit()
            return redirect(url_for('lister_apprenant_mod'))

#***********************************************************************************************
if __name__ == '__main__': #si le fichier est executer alors execute le bloc
    db.create_all()
    app.run(debug=True) #debug=True relance le serveur à chaque modification



