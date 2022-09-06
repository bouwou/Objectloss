from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Personne
from .models import Objet
from .forms import PersonneForm, PersonneForm1, UserForm, TrouveurForm, AgenceForm
from .forms import ObjetForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Trouveur, Agence, TypeObjet, AutreType
from django import forms


class FormLogin(forms.Form):
    username = forms.CharField(label="Identifiant", required=True)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=True)


def registerTrouveur(request):
    # username = request.POST.get('username')
    # roles = request.POST.get('roles')
    # password = request.POST.get('password')
    # new_user = User(
    #     username=username,
    #     roles=roles,
    #     password=password,
    # )
    # new_user.save()
    # return redirect('/')   autre methode
    if request.method == 'POST':

        if 'id' not in request.POST:
            # Creation personne
            nom_prop = request.POST['nom_prop'] if request.POST['nom_prop'] != '' else None
            prenom_prop = request.POST['prenom_prop'] if request.POST['prenom_prop'] != '' else None
            telephone = request.POST['telephone'] if request.POST['telephone'] != '' else None
            email = request.POST['email'] if request.POST['email'] != '' else None
            date_naissance = request.POST['date_naissance'] if request.POST['date_naissance'] != '' else None
            lieu_residence = request.POST['lieu_residence'] if request.POST['lieu_residence'] != '' else None
            date_delivrance = request.POST['date_delivrance'] if request.POST['date_delivrance'] != '' else None
            cni = request.POST['cni'] if request.POST['cni'] != '' else None

            new_personne = Personne(nom=nom_prop, prenom=prenom_prop, lieu_de_residence=lieu_residence,
                                    telephone=telephone, email=email,
                                    date_naissance=date_naissance, numero_cni=cni, date_delivrance=date_delivrance)
            new_personne.save()
            new_personne = Personne.objects.latest('id')

            # Creation User
            password = request.POST['password']
            new_user = User(
                username=telephone,
                password=password
            )
            new_user.save()

            # Creation Trouveur
            profession = request.POST['profession'] if request.POST['profession'] != '' else None
            new_trouveur = Trouveur(
                personne=new_personne,
                user=User.objects.last(),
                profession=profession
            )
            new_trouveur.save()
            new_objet = Objet.objects.latest('id')
            return HttpResponse('Register successfully')

        else:
            id = request.POST['id']

    return render(request, 'fr/public/register_trouveur.html', )



def registerAgence(request):
    # username = request.POST.get('username')
    # roles = request.POST.get('roles')
    # password = request.POST.get('password')
    # new_user = User(
    #     username=username,
    #     roles=roles,
    #     password=password,
    # )
    # new_user.save()
    # return redirect('/')   autre methode

    if request.method == 'POST':

        if 'id' not in request.POST:
            # Creation personne
            nom_prop = request.POST['nom_prop'] if request.POST['nom_prop'] != '' else None
            telephone = request.POST['telephone'] if request.POST['telephone'] != '' else None
            email = request.POST['email'] if request.POST['email'] != '' else None
            lieu_residence = request.POST['lieu_residence'] if request.POST['lieu_residence'] != '' else None

            new_personne = Personne(nom=nom_prop, prenom=nom_prop, lieu_de_residence=lieu_residence,
                                    telephone=telephone, email=email)
            new_personne.save()
            new_personne = Personne.objects.latest('id')

            # Creation User
            username = request.POST['username']
            password = request.POST['password']
            new_user = User(
                username=username,
                password=password
            )
            new_user.save()

            # Creation Agence
            ville = request.POST['ville'] if request.POST['ville'] != '' else None
            new_agence = Agence(
                nom=nom_prop,
                user=User.objects.last(),
                localisation=lieu_residence,
                telephone=telephone,
                email=email,
                ville=ville
            )
            new_agence.save()
            return HttpResponse('Register successfully')

        else:
            id = request.POST['id']

    return render(request, 'fr/public/register_agence.html', )


def loginPage(request):
    username = None  # default value
    error = ''

    if request.method == 'POST':

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = None
        print('username')
        print(username)
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            print("Either the blog or entry doesn't exist.")

        if user is not None:
            if username.strip() == user.username and password.strip() == user.password:
                # request.session['username'] = username
                request.session['logged_user_id'] = user.id
                trouveur = None
                agence = None
                try:
                    trouveur = Trouveur.objects.get(user=user)
                    agence = Agence.objects.get(user=user)
                except ObjectDoesNotExist:
                    print("Either the blog or entry doesn't exist.")
                if trouveur is not None:
                    request.session['logged_trouveur_id'] = trouveur.id
                if agence is not None:
                    request.session['logged_agence_id'] = agence.id
                return HttpResponse('Connexion successfully')
            else:
                error = 'Username or password incorrect'
                return HttpResponse('Username or password incorrect')
        else:
            error = 'Username or password incorrect'
            return HttpResponse('Username or password incorrect')

    else:
        return render(request, 'fr/public/login.html')
        # messages.error(request, 'Invalid Credentials')


def index(request):
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'logout':
                if request.session.has_key('logged_user_id'):
                    request.session.flush()
                    return redirect('home')

    logged_user = None
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        logged_user = User.objects.get(id = logged_user_id)
    if request.method == "GET":
        form1 = PersonneForm()
        form2 = ObjetForm()  # si on n'a pas passé d'id le formulaire sera vide
        type_objet = TypeObjet.objects.filter(supprimer=0)

        return render(request, 'fr/public/home.html', {'type_objet': type_objet, 'object': None, 'logged_user': logged_user})
    else:
        if 'id' not in request.POST:
            # Creation personne
            nom_prop = request.POST['nom_prop'] if request.POST['nom_prop'] != '' else None
            prenom_prop = request.POST['prenom_prop'] if request.POST['prenom_prop'] != '' else None
            telephone = request.POST['telephone'] if request.POST['telephone'] != '' else None
            email = request.POST['email'] if request.POST['email'] != '' else None
            date_naissance = request.POST['date_naissance'] if request.POST['date_naissance'] != '' else None
            lieu_residence = request.POST['lieu_residence'] if request.POST['lieu_residence'] != '' else None
            cni = request.POST['cni'] if request.POST['cni'] != '' else None
            passeport = request.POST['passeport'] if request.POST['passeport'] != '' else None

            new_personne = Personne(nom=nom_prop, prenom=prenom_prop, lieu_de_residence=lieu_residence,
                                    telephone=telephone, email=email,
                                    date_naissance=date_naissance, numero_cni=cni, numero_passeport=passeport)
            new_personne.save()
            new_personne = Personne.objects.latest('id')

            # Creation Objet
            type_objet = request.POST['type_objet']
            if request.POST['type_objet'] == 'autre':
                type_objet = None
                autre_type = request.POST['autre_type']
                new_autre_type = AutreType(nom=autre_type)
                new_autre_type.save()
                new_autre_type = AutreType.objects.latest('id')
            else:
                new_autre_type = None
            nom_objet = request.POST['nom_objet'] if request.POST['nom_objet'] != '' else None
            lieu_perte = request.POST['lieu_perte'] if request.POST['lieu_perte'] != '' else None
            date_perte = request.POST['date_perte'] if request.POST['date_perte'] != '' else None
            description = request.POST['description'] if request.POST['description'] != '' else None
            statut = 'Déclaré'

            if type_objet is not None:
                type_objet = TypeObjet.objects.get(pk=type_objet, supprimer=0)

            new_objet = Objet(type_objet=type_objet, autre_type=new_autre_type, personne=new_personne,
                              nom_objet=nom_objet, description=description, statut=statut,
                              situation='pas trouvé', lieu_perte=lieu_perte, date_perte=date_perte)
            new_objet.save()
            new_objet = Objet.objects.latest('id')
            data = {
                "response": "New object added successfully",
                "id": new_objet.id
            }
            return JsonResponse(data)
        else:
            id = request.POST['id']
            # update_exploitation = Exploitationobjet.objects.get(pk=id)
            #
            # update_exploitation.statut = request.POST['status']
            # update_exploitation.qte_exploiter = request.POST['qty']
            # update_exploitation.exploitation = request.POST['exploitation']
            # update_exploitation.date_mise_en_service = request.POST['commissioning_date']
            # wallet = request.POST['wlt_id']
            #
            # wallet = Wallet.objects.get(pk=wallet, supprimer=0)
            #
            # update_exploitation.wallet = wallet
            #
            # update_exploitation.save()
            # return HttpResponse('Exploitation object updated successfully')
        return render(request, 'fr/public/home.html',{'logged_user': logged_user})
        #return render(request, 'fr/public/home.html')


def getobjets(request):
    objets = Objet.objects.filter(supprimer=0)
    return JsonResponse({"objets": list(
        objets.values('personne__id', 'personne__nom', 'personne__prenom', 'id_objet', 'type_objet__nom', 'id'))})


def getobjet(request, id=0):
    if id != 0:
        objet = Objet.objects.filter(id=id, supprimer=0)
        return JsonResponse({"objet": list(
            objet.values('personne__id', 'personne__nom', 'personne__prenom', 'id_objet', 'type_objet__nom', 'id',
                         'nom_objet', 'personne__telephone', 'date_enregistrement'))})
