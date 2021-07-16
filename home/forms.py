from django import forms
from .models import Personne
from .models import Objet, User, Trouveur, Agence


class PersonneForm(forms.ModelForm):

    class Meta:
        model = Personne
        #fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('nom', 'prenom', 'email', 'telephone', 'lieu_de_residence', 'date_naissance', 'numero_cni', 'numero_passeport', 'date_delivrance') # afficher dans le formulaire avec l'ordre de fields
        labels = {
            'nom': 'Nom propriétaire',
            'prenom': 'Prenom propriétaire',
            'email': 'Email',
            'telephone': 'Téléphone',
            'lieu_de_residence': 'Lieu de residence',
            'date_naissance': 'Date de naissance',
            'numero_cni': 'Numéro CNI',
            'numero_passeport': 'Numero PASSEPORT',
            'date_delivrance': 'Date de délivrance',
        }
    def __init__(self, *args, **kwargs):
        super(PersonneForm, self).__init__(*args, **kwargs)
        self.fields['nom'].required = True
        self.fields['prenom'].required = True
        self.fields['telephone'].required = True


class PersonneForm1(forms.ModelForm):

    class Meta:
        model = Personne
        #fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('nom', 'prenom', 'date_naissance', 'lieu_de_residence', 'telephone', 'email', 'numero_cni', 'date_delivrance') # afficher dans le formulaire avec l'ordre de fields
        labels = {
            'nom': 'Nom',
            'prenom': 'Prenom',
            'date_naissance': 'Date de naissance',
            'lieu_de_residence': 'Lieu de résidence',
            'telephone': 'Téléphone',
            'numero_cni': 'Numéro de la CNI',
            'date_delivrance': 'Date de délivrance',
        }
    def __init__(self, *args, **kwargs):
        super(PersonneForm1, self).__init__(*args, **kwargs)
        self.fields['nom'].required = True
        self.fields['prenom'].required = True
        self.fields['date_naissance'].required = True
        self.fields['lieu_de_residence'].required = True
        self.fields['telephone'].required = True

class ObjetForm(forms.ModelForm):

    class Meta:
        model = Objet
        #fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('nom_objet', 'type_objet', 'lieu_perte', 'date_perte', 'description') # afficher dans le formulaire avec l'ordre de fields
        labels = {
            'nom_objet': "Nom de l'objet",
            'type_objet': "Type d'objet",
            'lieu_perte': 'Lieu de perte',
            'date_perte': 'Date de perte',
            'description': 'Description',
        }
    def __init__(self, *args, **kwargs):
        super(ObjetForm, self).__init__(*args, **kwargs)
        self.fields['type_objet'].empty_label = "Sélectionner"
        self.fields['nom_objet'].required = True
        self.fields['type_objet'].required = True


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        #fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('username', 'password') # afficher dans le formulaire avec l'ordre de fields
        labels = {
            'username': "Identifiant",
            'password': "Mot de passe",
        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = True
        self.fields['username'].required = True


class TrouveurForm(forms.ModelForm):
    class Meta:
        model = Trouveur
        # fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('user', 'personne', 'profession')  # afficher dans le formulaire avec l'ordre de fields
        labels = {
            'profession': "Profession",
        }

    def __init__(self, *args, **kwargs):
        super(TrouveurForm, self).__init__(*args, **kwargs)
        self.fields['profession'].required = False

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agence
        # fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('nom', 'ville', 'localisation', 'telephone', 'email')  # afficher dans le formulaire avec l'ordre de fields
        labels = {
            'nom': "Nom de l'agence",
            'ville': "Ville",
            'localisation': 'Localisation',
            'telephone': 'Téléphone',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super(AgenceForm, self).__init__(*args, **kwargs)
        self.fields['nom'].required = True
        self.fields['ville'].required = True
        self.fields['localisation'].required = True
        self.fields['telephone'].required = True
        self.fields['email'].required = True
