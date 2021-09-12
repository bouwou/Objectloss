from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from .models import Personne
from .models import Objet
from .forms import PersonneForm, PersonneForm1, UserForm, TrouveurForm, AgenceForm
from .forms import ObjetForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Trouveur, Agence
from django import forms
import logging
from django.views.decorators.csrf import csrf_exempt

import logging
import string
from django.utils.crypto import get_random_string
import json
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

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
def registerPage(request):
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
    _type = request.data.get('type')
    print(f'request.data : {(request.data)}')
    if _type != 'None':
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
            _user = User(
                username=_username,
                password=_password,
                roles='client'
            )
            _user.save()
            print(f'request : {_user}')

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
    # else:
    #     print(f'_trouveur : {_trouveur}')

    else:
        if 'logged_user_id' in request.session:
            return redirect('home')  # vous ne pouvez pas créer de compte si vous etes connecté
        if len(request.POST) > 0 and 'profileType' in request.POST:
            form = UserForm(prefix="tr")
            form1 = PersonneForm1(prefix="tr")
            form2 = TrouveurForm(prefix="tr")
            form3 = AgenceForm(prefix="ag")
            form4 = UserForm(prefix="ag")

            if request.POST['profileType'] == 'trouveur':
                form = UserForm(request.POST, prefix="tr")
                form1 = PersonneForm1(request.POST, prefix="tr")
                form2 = TrouveurForm(request.POST, prefix="tr")
                if form.is_valid():
                    if form1.is_valid():
                        if form2.is_valid():
                            form.save()
                            form1.save()
                            new_trouveur = Trouveur(
                                personne=Personne.objects.last(),
                                user=User.objects.last(),
                                profession=form2.cleaned_data['profession']
                            )
                            new_trouveur.save()
                            return redirect('login')
            elif request.POST['profileType'] == 'agence':
                form3 = AgenceForm(request.POST, prefix="ag")
                form4 = UserForm(request.POST, prefix="ag")
                if form3.is_valid():
                    if form4.is_valid():
                        form4.save()
                        new_personne = Personne(
                            nom=form3.cleaned_data['nom'],
                            prenom=form3.cleaned_data['nom'],
                            lieu_de_residence=form3.cleaned_data['localisation'],
                            telephone=form3.cleaned_data['telephone'],
                            email=form3.cleaned_data['email']
                        )
                        new_personne.save()
                        new_trouveur = Trouveur(
                            personne=Personne.objects.last(),
                            user=User.objects.last(),
                            profession='agenge'
                        )
                        new_trouveur.save()
                        new_agence = Agence(
                            user=User.objects.last(),
                            nom=form3.cleaned_data['nom'],
                            ville=form3.cleaned_data['ville'],
                            localisation=form3.cleaned_data['localisation'],
                            telephone=form3.cleaned_data['telephone'],
                            email=form3.cleaned_data['email']
                        )
                        new_agence.save()
                        return redirect('login')

            return render(request, 'fr/public/register.html',
                          {
                              'form': form,
                              'form1': form1,
                              'form2': form2,
                              'form3': form3,
                              'form4': form4,

                          })
        else:
            form = UserForm(prefix="tr")
            form1 = PersonneForm1(prefix="tr")
            form2 = TrouveurForm(prefix="tr")
            form3 = AgenceForm(prefix="ag")
            form4 = UserForm(prefix="ag")
            return render(request, 'fr/public/register.html',
                          {
                              'form': form,
                              'form1': form1,
                              'form2': form2,
                              'form3': form3,
                              'form4': form4,

                          })


@csrf_exempt
@api_view(['GET', 'POST'])
def loginPage(request):
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
                    return Response("error")
            else:
                error = 'Username or password incorrect'
                return Response("error")
        except ObjectDoesNotExist:
            return Response("error")

        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = None
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
                    return redirect('home')
                else:
                    error = 'Username or password incorrect'
                    return render(request, 'fr/public/login.html', {'form': form_login, 'error': error})
            else:
                error = 'Username or password incorrect'
                return render(request, 'fr/public/login.html', {'form': form_login, 'error': error})
        else:
            return render(request, 'fr/public/login.html', {'form': form_login})
    else:
        return render(request, 'fr/public/login.html')
        # messages.error(request, 'Invalid Credentials')

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

        return render(request, 'fr/public/home.html',
                      {'personne_form': form1, 'objet_form': form2, 'logged_user': logged_user})
    else:
        form1 = PersonneForm(request.POST)
        form2 = ObjetForm(request.POST)

        if form1.is_valid():
            if form2.is_valid():
                form1.save()
                form2.save()
        return render(request, 'fr/public/home.html', {'logged_user': logged_user})


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
