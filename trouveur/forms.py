from django import forms
from .models import Personne
from .models import Objet, ObjetTrouve


class PersonneForm(forms.ModelForm):

    class Meta:
        model = Personne
        #fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('nom', 'prenom') # afficher dans le formulaire avec l'ordre de fields
        labels = {
            'nom': 'Nom propriétaire',
            'prenom': 'Prenom propriétaire',
        }
    def __init__(self, *args, **kwargs):
        super(PersonneForm, self).__init__(*args, **kwargs)
        self.fields['nom'].required = True
        self.fields['prenom'].required = True


class ObjetForm(forms.ModelForm):

    class Meta:
        model = Objet
        #fields = '__all__' pour pouvoir afficher tous les champs de ta table dans un formulaire
        fields = ('nom_objet', 'type_objet', 'id_objet') # afficher dans le formulaire avec l'ordre de fields
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

class ObjetTrouveForm(forms.ModelForm):
    class Meta:
        model = ObjetTrouve
        fields = ('lieu_trouver','description')
        labels = {
            'lieu_trouver': 'Lieu où vous avez trouvé',
            'description': 'Description'
        }

    def __init__(self, *args, **kwargs):
        super(ObjetTrouveForm, self).__init__(*args, **kwargs)
        self.fields['lieu_trouver'].required = True
        self.fields['description'].required = False

