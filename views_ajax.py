from flask import Flask, render_template, request, flash, url_for, redirect,session,jsonify
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from tables import *


app = Flask(__name__) #permet de localiser les ressources cad les templates
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/scolaireAlchemy'
app.secret_key = 'some_secret'
db = SQLAlchemy(app)

#**************************************ACCUEIL************************************
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':     
        requete_check_app= Apprenant.query.all()
        control_app=False
        control_mat=False
        for val in requete_check_app:
            if request.form['matricule'] == val.matricule:
                control_mat=True
                id_update_app=val.id

            if val.tel==request.form['telephone'].strip() or val.email== request.form['email'].strip():
                control_app=True
                
        if control_mat == True:
            requete_update = Inscription.query.filter_by(id_app=id_update_app).first()
            requete_update.date_ins=request.form['date_ins']
            requete_update.annee_aca=request.form['annee_ac'].strip()
            requete_update.id_classe=request.form['classe']
            db.session.commit()
            flash("SUCCESS : Modification avec succès!!!")
            return redirect(url_for('index'))

        elif control_app == False:
            student = Apprenant(request.form['matricule'],request.form['prenom'].strip(),request.form['nom'].strip(),request.form['sexe'],
                                request.form['date_naissance'],request.form['lieu_naissance'].strip(),
                                request.form['adresse'].strip(),request.form['email'].strip(),request.form['telephone'].strip())

           
            

            inscrire = Inscription(request.form['date_ins'],request.form['annee_ac'].strip(),id_app=last_id(),id_classe=request.form['classe'])
            db.session.add(student)
            db.session.commit()
            db.session.add(inscrire)
            db.session.commit()
            flash("SUCCESS : Apprenant ajouté avec succès!!!")
            return redirect(url_for('index'))
        else:
            flash("WARNING : L'apprenant existe déjà")
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("ajouter_apprenant.html",gen_mat=genere_matricule(), annee_academy=genere_annee_aca(),filieres=filiere_find_all(),date_ins=datetime.date.today())

@app.route('/listfiliere', methods = ['GET','POST'])
def liste_filiere():
    liste_fil = Filiere.query.all()
    liste_filiere=[]
    for val in liste_fil:
        mon_dict= { "id":val.id , "libelle":val.nom_fil}
        liste_filiere.append(mon_dict)
    print(liste_filiere)  
    return jsonify(liste_filiere)

@app.route('/filiere&<string:ide>', methods = ['GET','POST'])
def action_filiere(ide):
    print(ide)

    classe = Classe.query.filter_by(id_fil=ide).all()
    liste_classe=[]
    for val in classe:
        mon_dict= { "id":val.id , "libelle":val.libelle }
        liste_classe.append(mon_dict)
    print(liste_classe)  
    return jsonify(liste_classe)

@app.route('/classe&<string:ide>', methods = ['GET','POST'])
def action_classe(ide):
    print(ide)

    ele_classe = Classe.query.filter_by(id=ide).all()
    liste_ele_classe=[]
    for val in ele_classe:
        mon_dict= {"mont_ins":val.mont_ins, "mensualite":val.mensualite }
        liste_ele_classe.append(mon_dict)
    print(liste_ele_classe)    
    return jsonify(liste_ele_classe)

@app.route('/search&<string:ide>', methods = ['GET','POST'])
def search_mat(ide):
    print(str(ide).upper())
    mat=str(ide).upper()
    mat_search=Apprenant.query.all()
    apprenant_find=[]
    liste_mat=[]
    for val in mat_search:
        liste_mat.append(val.matricule)
    if (mat in liste_mat):
        app_search = Apprenant.query.filter_by(matricule=mat).all()
        
        for val in app_search:
            id_apprenant=val.id
            mon_dict_app = {"id":val.id, "prenom":val.prenom , "nom":val.nom, "sexe":val.sexe, "date_naiss":val.date_naiss,
                        "lieu_naiss":val.lieu_naiss,"adresse":val.adresse,"email":val.email,"tel":val.tel }
            
        ins_find=[]
        ins_search = db.session.query(Inscription).join(Classe).filter(Inscription.id_app == id_apprenant).all()
        iclass=None
        for val in ins_search:
            mon_dict_ins = {"date_ins":val.date_ins,"anne_aca":val.annee_aca,"iclass":val.id_classe}
            iclass=val.id_classe
            ins_find.append(mon_dict_ins)
        print(ins_find)
        print("iclas:",iclass)
        
        class_name=Classe.query.filter_by(id =iclass ).all()
        for val in class_name:
            id_filiere=val.id_fil
        print("idfil",id_filiere)

        nom_filiere=None
        fil_name = Filiere.query.filter_by(id = id_filiere).all()
        print(fil_name)
        
        for val in fil_name:
            nom_filiere=val.nom_fil
        print(nom_filiere)
        print(mon_dict_app)

        fil_search = Classe.query.join(Filiere, Classe.id_fil == Filiere.id).filter(Classe.id == iclass).all()
        for val in fil_search:
            mon_dict_app.update({"id_class":val.id,"lib_classe":val.libelle,"mont_ins":val.mont_ins,"mensualite":val.mensualite,"id_fil":val.id_fil,"nom_fil":nom_filiere})
            apprenant_find.append(mon_dict_app)
        print(apprenant_find)
        return jsonify(apprenant_find)
    else:
        return jsonify([{'vide':'WARNING: Le matricule saisit n\'existe pas'}])


#****************************************************LES FONCTIONS******************************
def genere_matricule():
    date_actu=datetime.datetime.today().strftime('%Y')
    matricule = Apprenant.query.count()
    if matricule == 0:
        num=1
        val='-'+str(num)+'-'
        gen_mat = "SA"+val+str(date_actu)
        return gen_mat
    else:
        num=matricule+1
        val='-'+str(num)+'-'
        gen_mat="SA"+val+str(date_actu)
        return gen_mat
#-----------------------------------Génération Année Académique-----------------------------------
def genere_annee_aca():
    mois=int(datetime.datetime.today().strftime('%m'))
    annee1=0
    annee2=0
    annee_academy=None
    if mois>=8:
        annee1 = int(datetime.datetime.today().strftime('%Y'))
        print(annee1)
        annee2 = annee1+1
        annee_academy = str(annee1)+"/"+str(annee2)
        return annee_academy
    else:
        annee1=int(datetime.datetime.today().strftime('%Y'))
        annee2=annee1-1
        annee_academy=str(annee2)+"/"+str(annee1)
        return annee_academy
#-----------------------------------Liste des filières-----------------------------------
def filiere_find_all():
    result=db.session.query(Filiere).all()
    filieres=[]
    for row in result:
        ma_liste = [row.id, row.nom_fil]  
        filieres.append(ma_liste)  
    print(filieres)
    return filieres

#----------------------------------RETOUR DERNIERE ID DE LA BASE--------------------------------------
def last_id():
    search_id_app = Apprenant.query.all()
    for val in search_id_app:
        id_app=val.id + 1
    return id_app
#***********************************************************************************************
if __name__ == '__main__': #si le fichier est executer alors execute le bloc
    app.run(debug=True) #debug=True relance le serveur à chaque modification



