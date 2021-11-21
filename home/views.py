from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Personne
from .models import Objet
from .forms import PersonneForm, PersonneForm1, UserForm, TrouveurForm, AgenceForm
from .forms import ObjetForm
from django.contrib.auth import login, logout, authenticate
from .models import User, Trouveur, Agence
from django import forms


class FormLogin(forms.Form):
    username = forms.CharField(label="Identifiant", required=True)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, required=True)


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

        if 'logged_user_id' in request.session:
            return redirect('home') # vous ne pouvez pas créer de compte si vous etes connecté
        if len(request.POST) >0 and 'profileType' in request.POST:
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

def loginPage(request):
    username = None # default value
    error = ''
    form_login = FormLogin()

    if request.method == 'POST':
        form_login = FormLogin(request.POST)
        if form_login.is_valid():
            username  = form_login.cleaned_data['username']
            password  = form_login.cleaned_data['password']
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
        #messages.error(request, 'Invalid Credentials')


def index(request):
    #return render(request, 'fr/public/home.html',{'personne_form': form1, 'objet_form': form2})
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
        logged_user = User.objects.get(id = logged_user_id)
    if request.method == "GET":
        form1 = PersonneForm()
        form2 = ObjetForm()# si on n'a pas passé d'id le formulaire sera vide

        return render(request, 'fr/public/home.html',{'personne_form': form1, 'objet_form': form2, 'logged_user': logged_user})
    else:
        form1 = PersonneForm(request.POST)
        form2 = ObjetForm(request.POST)


        if form1.is_valid():
            if form2.is_valid():
                form1.save()
                form2.save()
        if request.POST['type']:
            form1.save()
            form2.save()
            return HttpResponse("Objet enrégistré, vous serrez informé une fois qu'il sera retrouvé")
        else:
            return render(request, 'fr/public/home.html',{'logged_user': logged_user})
