from datetime import datetime

import json

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.forms import ObjetForm, PersonneForm
from trouveur.models import User, Objet, ObjetTrouve, Personne, ObjetReceptionne, ObjetDelivre, Trouveur, Agence

import logging
import string

from trouveur.forms import ObjetTrouveForm

logger = logging.getLogger('django.security.csrf')

REASON_NO_REFERER = "Referer checking failed - no Referer."
REASON_BAD_REFERER = "Referer checking failed - %s does not match any trusted origins."
REASON_NO_CSRF_COOKIE = "CSRF cookie not set."
REASON_BAD_TOKEN = "CSRF token missing or incorrect."
REASON_MALFORMED_REFERER = "Referer checking failed - Referer is malformed."
REASON_INSECURE_REFERER = "Referer checking failed - Referer is insecure while host is secure."

CSRF_SECRET_LENGTH = 32
CSRF_TOKEN_LENGTH = 2 * CSRF_SECRET_LENGTH
CSRF_ALLOWED_CHARS = string.ascii_letters + string.digits
CSRF_SESSION_KEY = '_csrftoken'


class FormLogin(forms.Form):
    username = forms.CharField(label="Identifiant", required=True)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=True)

@csrf_exempt
@api_view(['GET', 'POST'])
def register(request):
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

    print(f'request.data : {(request.data)}')
    if len(request.POST) > 0 and request.data.get('type') in request.POST:
        _type = request.data.get('type')
        _nom = request.data.get('nom')
        _nomagence = request.data.get('nomagence')
        _prenom = request.data.get('prenom')
        _username = request.data.get('username')
        _password = request.data.get('password')
        _passwordconfirm = request.data.get('passwordconfirm')
        _lieuResidence = request.data.get('lieuResidence')
        _datenaiss = request.data.get('dateNaissance')
        _description = request.data.get('description')
        _profession = request.data.get('profession')
        _phone = request.data.get('phone')
        _ville = request.data.get('ville')
        _localisation = request.data.get('localisation')
        _nbrcni = request.data.get('nbrcni')
        _email = request.data.get('email')
        _datedelivrance = request.data.get('datedelivrance')
        print(f'request 1')
        if (_type == 'Trouveur'):
            print(f'_personne')
            _personne = Personne(
                nom=_nom,
                prenom=_prenom,
                email=_email,
                telephone=_phone,
                date_naissance=_datenaiss,
                lieu_de_residence=_lieuResidence,
                date_delivrance=_datedelivrance,
                numero_cni=_nbrcni,
            )
            _personne.save()
            print(f'_personne : {_personne}')

            _user = User(
                username=_username,
                password=_password,
                roles='client'
            )
            _user.save()
            print(f'request : {_user}')

            _trouveur = Trouveur(
                user=_user,
                personne=_personne,
                profession=_profession,
                date_creation=datetime.today()
            )
            _trouveur.save()
            print(f'_trouveur : {_trouveur}')
            return Response("success")
        elif _type == 'Agence':
            print(f'_agence')
            _personne = Personne(
                nom=_nomagence,
                prenom=_nomagence,
                email=_email,
                telephone=_phone,
                lieu_de_residence=_localisation,
            )
            _personne.save()
            print(f'_personne : {_personne}')
            _user = User(
                username=_username,
                password=_password,
                roles='agence'
            )
            _user.save()
            print(f'_user : {_user}')

            _trouveur = Trouveur(
                user=_user,
                personne=_personne,
                profession='agence',
            )
            _trouveur.save()

            _agence = Agence(
                nom=_nomagence,
                user=_user,
                ville=_ville,
                localisation=_localisation,
                telephone=_phone,
                email=_email,
                date_creation=datetime.today(),
            )
            _agence.save()
            print(f'_agence : {_agence}')
            return Response("success")

@csrf_exempt
@api_view(['GET', 'POST'])
def login(request):
    username = None  # default value
    error = ''

    if request.method == 'POST':
        print(f'request : {request.body}')  # can see output
        # logging.debug('This is a debug message')
        # logging.info('This is an info message')
        # logging.warning('This is a warning message')
        # logging.error('')
        # logging.critical('This is a critical message')
        form_login = FormLogin()
        print("form_login.", form_login)
        form_login = FormLogin(request.POST)
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        # content = body['username']
        received_json_data = json.loads(request.body)
        print("content.", received_json_data.get('username'))

        print("request.POST.", request.POST)

        print("request.body : ", request.body)

        _username = received_json_data.get('username')
        _password = received_json_data.get('password')
        print("username : ", _username)
        print("password : ", _password)

        print("Hello world.", form_login.is_valid())
        # print(" User.objects.get(username=username) : ",  User.objects.get(username=_username,password=_password))
        try:
            User.objects.filter(password=_password).exists()
            User.objects.filter(username=_username).exists()
            User.objects.filter(username=_username, password=_password).exists()
            username = _username
            password = _password
            user = User.objects.get(username=username)
            if user is not None:
                if username.strip() == user.username and password.strip() == user.password:
                    # request.session['username'] = username
                    request.session['logged_user_id'] = user.id
                    print("Hello world.")
                    # trouveur = Trouveur.objects.get(user=user)
                    # agence = Agence.objects.get(user=user)
                    return Response("success")
                else:
                    error = 'Username or password incorrect'
                    return Response("error_pass")
            else:
                error = 'Username or password incorrect'
                return Response("error_pass")
        except ObjectDoesNotExist:
            return Response("error")

@api_view(['GET', 'POST'])
def index(request):
    # return render(request, 'fr/public/home.html',{'personne_form': form1, 'objet_form': form2})
    form1 = PersonneForm()
    form2 = ObjetForm()
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
        logged_user = User.objects.get(id=logged_user_id)
    if request.method == "GET":
        form1 = PersonneForm()
        form2 = ObjetForm()  # si on n'a pas passé d'id le formulaire sera vide

        return Response("Vide")
    else:
        _type = request.data.get('type')
        _nom = request.data.get('nom')
        _prenom = request.data.get('prenom')
        _lieuResidence = request.data.get('lieuResidence')
        _datenaiss = request.data.get('dateNaissance')
        _phone = request.data.get('phone')
        _nbrcni = request.data.get('nbrcni')
        _email = request.data.get('email')
        _datedelivrance = request.data.get('datedelivrance')

        _personne = Personne(
            nom=_nom,
            prenom=_prenom,
            email=_email,
            telephone=_phone,
            date_naissance=_datenaiss,
            lieu_de_residence=_lieuResidence,
            date_delivrance=_datedelivrance,
            numero_cni=_nbrcni,
        )
        _personne.save()

        _type = request.data.get('type')
        _nomObjet = request.data.get('nomObjet')
        _idObjet = request.data.get('idObjet')

        _objet = Objet(
            personne=Personne.objects.last(),
            statut='Retrouvé',
            situation='trouvé',
            nom_objet=_nomObjet,
            type_objet=_type,
            id_objet=_idObjet,
        )
        _objet.save()

        return Response('Success register')

def _get_new_csrf_string():
    return get_random_string(CSRF_SECRET_LENGTH, allowed_chars=CSRF_ALLOWED_CHARS)

def _salt_cipher_secret(secret):
    """
    Given a secret (assumed to be a string of CSRF_ALLOWED_CHARS), generate a
    token by adding a salt and using it to encrypt the secret.
    """
    salt = _get_new_csrf_string()
    chars = CSRF_ALLOWED_CHARS
    pairs = zip((chars.index(x) for x in secret), (chars.index(x) for x in salt))
    cipher = ''.join(chars[(x + y) % len(chars)] for x, y in pairs)
    return salt + cipher

def _unsalt_cipher_token(token):
    """
    Given a token (assumed to be a string of CSRF_ALLOWED_CHARS, of length
    CSRF_TOKEN_LENGTH, and that its first half is a salt), use it to decrypt
    the second half to produce the original secret.
    """
    salt = token[:CSRF_SECRET_LENGTH]
    token = token[CSRF_SECRET_LENGTH:]
    chars = CSRF_ALLOWED_CHARS
    pairs = zip((chars.index(x) for x in token), (chars.index(x) for x in salt))
    secret = ''.join(chars[x - y] for x, y in pairs)  # Note negative values are ok
    return secret

def get_token(request):
    """
    Returns the CSRF token required for a POST form. The token is an
    alphanumeric value. A new token is created if one is not already set.

    A side effect of calling this function is to make the csrf_protect
    decorator and the CsrfViewMiddleware add a CSRF cookie and a 'Vary: Cookie'
    header to the outgoing response.  For this reason, you may need to use this
    function lazily, as is done by the csrf context processor.
    """
    if "CSRF_COOKIE" not in request.META:
        csrf_secret = _get_new_csrf_string()
        request.META["CSRF_COOKIE"] = _salt_cipher_secret(csrf_secret)
    else:
        csrf_secret = _unsalt_cipher_token(request.META["CSRF_COOKIE"])
    request.META["CSRF_COOKIE_USED"] = True
    return _salt_cipher_secret(csrf_secret)



@api_view(['GET', 'POST'])
def signaler(request, id=0):
    print(f'request : {(request)}')
    print(f'request.data : {len(request.data)}')
    if len(request.data) == 12 :
        _type = request.data.get('type')
        _nomObjet = request.data.get('nomObjet')
        _idObjet = request.data.get('idObjet')
        _lieuObjetRetrouver = request.data.get('lieuObjetRetrouver')
        _descriptionObjetRetrouver = request.data.get('descriptionObjetRetrouver')
        _nom = request.data.get('nom')
        _prenom = request.data.get('prenom')
        if _type == 'Passeport (8)':
            _type = 2
        else:
            _type = 1
        new_objet = Objet(
            personne=Personne.objects.last(),
            statut='Retrouvé',
            situation='trouvé',
            nom_objet=_nomObjet,
            type_objet=_type,
            id_objet=_idObjet,
        )
        new_objet.save()
        new_objet_trouve = ObjetTrouve(
            objet=Objet.objects.all().last(),
            lieu_trouver=_lieuObjetRetrouver,
            description=_descriptionObjetRetrouver,
        )
        new_objet_trouve.save()
        return Response('success signaler')
    else:
        return Response('error signaler')

def objets(request):
    print('Objet')
    logged_user = None
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        logged_user = User.objects.get(id=logged_user_id)
    else:
        return redirect('login')

    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'logout':
                if request.session.has_key('logged_user_id'):
                    request.session.flush()
                    return Response('Object back home')

    mes_objets = list()
    mes_objets_retr = list()
    i = 1
    if 'logged_trouveur_id' in request.session:
        objets_all = ObjetTrouve.objects.filter(trouveur=request.session['logged_trouveur_id'], supprimer=0)
        objets = ObjetTrouve.objects.filter(trouveur=request.session['logged_trouveur_id'], supprimer=0, objet__situation='trouvé')
        for obj in objets:
           objet = {
               'numero': i,
               'prenom': obj.objet.personne.prenom,
               'nom': obj.objet.personne.nom,
               'type_objet': obj.objet.type_objet,
               'lieu_trouver': obj.lieu_trouver,
               'id': obj.id,
           }
           mes_objets.append(objet)
           i+=1

        i = 1

        objets_retr = ObjetReceptionne.objects.filter(objet_trouve__in=objets_all, supprimer=0, objet_trouve__objet__situation='déposé')
        for obj in objets_retr:
            objet = {
                'numero': i,
                'prenom': obj.objet_trouve.objet.personne.prenom,
                'nom': obj.objet_trouve.objet.personne.nom,
                'type_objet': obj.objet_trouve.objet.type_objet,
                'lieu_trouver': obj.objet_trouve.lieu_trouver,
                'id': obj.id,
            }
            mes_objets_retr.append(objet)
            i += 1


        return  Response({'objets': mes_objets, 'objets_retr': mes_objets_retr, 'logged_user': logged_user})

def objet_delete(request,id):
    print('delete objet')
    objet = ObjetTrouve.objects.get(pk=id, supprimer=0)
    objet.supprimer = 1
    objet.save()
    return Response('mes_objets')

def solde(request):
    print('solde')
    mes_objets = list()
    i = 1
    objets = ObjetTrouve.objects.filter(trouveur=1, supprimer=0)
    objets_retr = ObjetReceptionne.objects.filter(objet_trouve__in=objets, supprimer=0)
    objets_payer1 = ObjetDelivre.objects.filter(objet_receptionne__in=objets_retr, supprimer=0).order_by('date_delivrance')
    # charge les dix dernières paiements reçus par le troveur
    objets_payer = ObjetDelivre.objects.filter(objet_receptionne__in=objets_retr, supprimer=0).order_by('date_delivrance')[:10]
    for obj in objets_payer:
        objet = {
            'numero': i,
            'prenom': obj.objet_receptionne.objet_trouve.objet.personne.prenom,
            'nom': obj.objet_receptionne.objet_trouve.objet.personne.nom,
            'type_objet': obj.objet_receptionne.objet_trouve.objet.type_objet,
            'Agence': obj.objet_receptionne.agence.nom,
            'Date_du_retrait': obj.date_delivrance,
            'Valeur': obj.objet_receptionne.objet_trouve.objet.type_objet.prix,
            'id': obj.id,
        }
        mes_objets.append(objet)
        i += 1
    # calcul de la somme totale perçu par le trouveur
    prix_total = 0
    for obj in objets_payer1:
        prix_total = prix_total + obj.objet_receptionne.objet_trouve.objet.type_objet.prix

    # calcul de la somme totale des objets déposés en agence en attente de paiements
    prix_attente = 0
    for obj in objets_retr:
        prix_attente = prix_attente + obj.objet_trouve.objet.type_objet.prix

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
        logged_user = User.objects.get(id=logged_user_id)
    else:
        return redirect('login')

    return Response({'objets': mes_objets, 'prix_total': prix_total, 'prix_attente': prix_attente, 'logged_user': logged_user})



def receptionner(request):

    if request.method == 'POST':
        username = request.data.get('username')
        # username = request.POST.get('username')

        if username != '':
            user = None
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                error = 'Utilisateur inconnu'
                print("Either the blog or User doesn't exist.")
            if user is not None:
                trouveur = None
                try:
                    trouveur = Trouveur.objects.get(user=user)
                except ObjectDoesNotExist:
                    error = 'Trouveur inconnu'
                    print("Either the blog or entry doesn't exist.")
                if trouveur is not None:
                    objets = ObjetTrouve.objects.filter(trouveur=trouveur, objet__situation='trouvé', supprimer=0)
                    i = 1
                    mes_objets = list()
                    for obj in objets:
                        objet = {
                            'numero': i,
                            'prenom': obj.objet.personne.prenom,
                            'nom': obj.objet.personne.nom,
                            'type_objet': obj.objet.type_objet,
                            'lieu_trouver': obj.lieu_trouver,
                            'situation': obj.objet.situation,
                            'id': obj.id,
                        }
                        mes_objets.append(objet)
                        i += 1
                    return Response({'objets': mes_objets, 'error': error.replace("%20", " "), 'username': username})
    else:
        Response('hello')

def valider_reception(request, id=0):
    obj = ObjetTrouve.objects.get(pk=id, supprimer=0)
    obj.objet.situation = 'déposé'
    obj.objet.save()
    code = get_random_string(5, allowed_chars=string.ascii_uppercase + string.digits)
    print(code)
    new_objet_receptionne = ObjetReceptionne(
        objet_trouve=obj,
        agence=Agence.objects.get(pk=request.session['logged_agence_id'], supprimer=0),
        code_genere=code,
    )
    new_objet_receptionne.save()
    return redirect('receptionner_trouveur', username=obj.trouveur.user.username, error=None)

def restituer(request):
    logged_agence_id = request.session['logged_agence_id']
    agence = Agence.objects.get(pk=logged_agence_id)

    objets = list()
    i = 0
    objets_recep = ObjetReceptionne.objects.filter(agence=agence, objet_trouve__objet__situation='déposé')
    for obj in objets_recep:
        obj = {
            'numero': i,
            'nom': obj.objet_trouve.objet.personne.nom,
            'prenom': obj.objet_trouve.objet.personne.prenom,
            'type_objet': obj.objet_trouve.objet.type_objet,
            'lieu_trouver': obj.objet_trouve.lieu_trouver,
            'date_depot': obj.date_depot,
            'id': obj.id,
            'id_retr': obj.objet_trouve.id,
        }
        objets.append(obj)
        i += 1
    Response('success')