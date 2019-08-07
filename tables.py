from views_ajax import db
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

#**************************************TABLE FILIERE************************************
class Filiere(db.Model):
    id = db.Column('id_fil',db.Integer, primary_key = True)
    nom_fil = db.Column(db.String(100))

    def __init__(self, nom_fil):
        self.nom_fil = nom_fil
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
#**************************************TABLE INSCRIPTION************************************
class Inscription(db.Model):
    id = db.Column('id_ins',db.Integer, primary_key = True)
    date_ins = db.Column(db.Date())
    annee_aca = db.Column(db.String(100))
    id_app = db.Column(db.Integer, db.ForeignKey('apprenant.id_app'))
    id_classe = db.Column(db.Integer, db.ForeignKey('classe.id_classe'))

    def __init__(self, date_ins, annee_aca, id_app, id_classe):
        self.date_ins = date_ins
        self.annee_aca = annee_aca
        self.id_app = id_app
        self.id_classe = id_classe

db.create_all()
