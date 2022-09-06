# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.timezone import now


class Agence(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    nom = models.CharField(max_length=200)
    ville = models.CharField(max_length=100, blank=True, null=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    supprimer = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agence'


class AutreType(models.Model):
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'autre_type'


class Objet(models.Model):
    personne = models.ForeignKey('Personne', models.DO_NOTHING, blank=True, null=True)
    type_objet = models.ForeignKey('TypeObjet', models.DO_NOTHING, blank=True, null=True)
    autre_type = models.ForeignKey('AutreType', models.DO_NOTHING, blank=True, null=True)
    nom_objet = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)
    id_objet = models.CharField(max_length=50, blank=True, null=True)
    situation = models.CharField(max_length=50, blank=True, null=True)
    lieu_perte = models.CharField(max_length=255, blank=True, null=True)
    lieu_trouver = models.CharField(max_length=255, blank=True, null=True)
    date_perte = models.DateField(blank=True, null=True)
    date_enregistrement = models.DateTimeField(default=now, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    supprimer = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objet'


class ObjetDelivre(models.Model):
    objet_receptionne = models.ForeignKey('ObjetReceptionne', models.DO_NOTHING, blank=True, null=True)
    personne = models.ForeignKey('Personne', models.DO_NOTHING, blank=True, null=True)
    autre_personne = models.CharField(max_length=255, blank=True, null=True)
    date_delivrance = models.DateField(default=now, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    supprimer = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objet_delivre'


class ObjetReceptionne(models.Model):
    objet_trouve = models.ForeignKey('ObjetTrouve', models.DO_NOTHING, blank=True, null=True)
    agence = models.ForeignKey(Agence, models.DO_NOTHING, blank=True, null=True)
    date_depot = models.DateField(default=now, blank=True, null=True)
    code_genere = models.CharField(max_length=100, blank=True, null=True)
    supprimer = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objet_receptionne'


class ObjetTrouve(models.Model):
    trouveur = models.ForeignKey('Trouveur', models.DO_NOTHING, blank=True, null=True)
    objet = models.ForeignKey('Objet', models.DO_NOTHING, blank=True, null=True)
    date_trouver = models.DateField(default=now, blank=True, null=True)
    lieu_trouver = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    supprimer = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objet_trouve'


class Personne(models.Model):
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    lieu_de_residence = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    numero_cni = models.CharField(max_length=50, blank=True, null=True)
    numero_passeport = models.CharField(max_length=50, blank=True, null=True)
    date_delivrance = models.CharField(max_length=100, blank=True, null=True)
    lieu_delivrance = models.CharField(max_length=100, blank=True, null=True)
    supprimer = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personne'


class Trouveur(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    personne = models.ForeignKey('Personne', models.DO_NOTHING, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    date_creation = models.DateTimeField(default=now, blank=True, null=True)
    supprimer = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trouveur'


class TypeObjet(models.Model):
    nom = models.CharField(max_length=100, blank=True, null=True)
    perremption = models.IntegerField(blank=True, null=True)
    prix = models.IntegerField(blank=True, null=True)
    etat = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    supprimer = models.IntegerField()

    def __str__(self):
        return '%s (%s)' % (self.nom, self.perremption)

    class Meta:
        managed = False
        db_table = 'type_objet'


class User(models.Model):
    enabled = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    roles = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
