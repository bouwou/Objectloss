import string

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from agence.models import Trouveur, ObjetTrouve, User, ObjetReceptionne, Agence


def index(request):
    return redirect('receptionner')

def receptionner(request, username='', error=''):

    if username != '':
        username = username
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'logout':
                if request.session.has_key('logged_user_id'):
                    request.session.flush()
                    return redirect('home')

    logged_user = None
    if 'logged_user_id' in request.session and 'logged_agence_id' in request.session or error != '':
        logged_user_id = request.session['logged_user_id']
        logged_user = User.objects.get(id=logged_user_id)
    else:
        error="Vous n'êtes pas connecté en tant qu'agence"
        error = error.replace(" ", "%20")
        return redirect('receptionner_trouveur', username=None, error=error)
    if request.method == 'POST':
        username = request.POST.get('username')

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
                    return render(request, 'fr/public/agence/receptionner_objet.html', {'objets': mes_objets, 'logged_user': logged_user, 'error': error.replace("%20", " "), 'username': username})
    else:
        return render(request, 'fr/public/agence/receptionner_objet.html', {'logged_user': logged_user, 'error': error.replace("%20", " "), 'username': username})
        # messages.error(request, 'Invalid Credentials')
    return render(request, 'fr/public/agence/receptionner_objet.html', {'logged_user': logged_user, 'error': error.replace("%20", " "), 'username': username})

def valider_reception(request, id=0):
    if 'logged_agence_id' in request.session:
        obj = ObjetTrouve.objects.get(pk=id, supprimer=0)
        obj.objet.situation = 'déposé'
        obj.objet.save()
        code = get_random_string(5, allowed_chars=string.ascii_uppercase + string.digits)
        print(code)
        new_objet_receptionne = ObjetReceptionne(
            objet_trouve=obj,
            agence= Agence.objects.get(pk=request.session['logged_agence_id'], supprimer=0) ,
            code_genere= code,
        )
        new_objet_receptionne.save()
        return redirect('receptionner_trouveur', username=obj.trouveur.user.username, error=None)

def restituer(request):
    error=''
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        logged_user = User.objects.get(id=logged_user_id)
    else:
        return redirect('login')
    if 'logged_user_id' in request.session and 'logged_agence_id' in request.session:
        logged_agence_id = request.session['logged_agence_id']
        agence = Agence.objects.get(pk=logged_agence_id)
    else:
        error = "Vous n'êtes pas connecté en tant qu'agence"
        #error = error.replace(" ", "%20")
        return render(request, 'fr/public/agence/restituer_objet.html', {'logged_user': logged_user, 'error': error})

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

    return render(request, 'fr/public/agence/restituer_objet.html', {'logged_user': logged_user, 'objets': objets, 'error': error})