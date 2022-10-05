import string

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from agence.models import Trouveur, ObjetTrouve, User, ObjetReceptionne, Agence, ObjetDelivre, Personne


def index(request):
    return redirect('receptionner')

def receptionner(request, username=''):

    error=''
    print(username)
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
    if 'logged_user_id' in request.session and 'logged_agence_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        logged_user = User.objects.get(id=logged_user_id)
    else:
        error="Vous n'êtes pas connecté en tant qu'agence"
        return render(request, 'fr/public/agence/receptionner_objet.html', {'objets': None, 'error': error,  'username': username})
    if username != '':
        #username = request.GET.get('username')

        if username != '':
            user = None
            try:
                user = User.objects.get(username=username)
                print('bon pas trouveur')
            except ObjectDoesNotExist:
                error = 'Utilisateur inconnu'
                print("Either the blog or User doesn't exist.")
            if user is not None:
                trouveur = None
                print('bon bien trouveur')
                try:
                    trouveur = Trouveur.objects.get(user=user)
                except ObjectDoesNotExist:
                    error = 'Trouveur inconnu'
                    print("Either the blog or entry doesn't exist.")
                if trouveur is not None:
                    print('bon trouveur')
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
                            'id_obj': obj.objet.id,
                            'id': obj.id,
                        }
                        mes_objets.append(objet)
                        i += 1
                    return render(request, 'fr/public/agence/receptionner_objet.html', {'objets': mes_objets, 'logged_user': logged_user, 'error': error, 'username': username})
    else:
        return render(request, 'fr/public/agence/receptionner_objet.html', {'logged_user': logged_user, 'error': error, 'username': username})
        # messages.error(request, 'Invalid Credentials')
    return render(request, 'fr/public/agence/receptionner_objet.html', {'logged_user': logged_user, 'error': error, 'username': username})

def valider_reception(request, id=0):
    if id != 0:
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
            return HttpResponse('Save successfully')
            #return redirect('receptionner_trouveur', username=obj.trouveur.user.username, error=None)
    else:
        return HttpResponse('There is a problem !!!')

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
            'id_obj': obj.objet_trouve.objet.id,
            'id_person': obj.objet_trouve.objet.personne.id,
            'id_retr': obj.objet_trouve.id,
        }
        objets.append(obj)
        i += 1

    return render(request, 'fr/public/agence/restituer_objet.html', {'logged_user': logged_user, 'objets': objets, 'error': error})

def deliverObject(request):
    if request.method == 'POST':
         if 'id_person' not in request.POST:

             id = request.POST['id']
             obj_recep = ObjetReceptionne.objects.get(id=id)
             phone = request.POST['phone'] if request.POST['phone'] != '' else None
             name = request.POST['name'] if request.POST['name'] != '' else None
             firstname = request.POST['firstname'] if request.POST['firstname'] != '' else None
             autre_personne = name + '-' + firstname
             message = request.POST['message'] if request.POST['message'] != '' else None

             new_obj_delivre = ObjetDelivre(objet_receptionne=obj_recep, autre_personne=autre_personne, contact=phone, message=message)
             new_obj_delivre.save()
             objet = obj_recep.objet_trouve.objet
             objet.situation = 'terminé'
             objet.save()

             return HttpResponse(' Object deliver successfully')
         else:
             id = request.POST['id']
             obj_recep = ObjetReceptionne.objects.get(id=id)
             id_person = request.POST['id_person']
             person = Personne.objects.get(id=id_person)
             phone = request.POST['phone'] if request.POST['phone'] != '' else None
             message = request.POST['message'] if request.POST['message'] != '' else None

             new_obj_delivre = ObjetDelivre(objet_receptionne=obj_recep, personne=person, contact=phone, message=message)
             new_obj_delivre.save()
             objet = obj_recep.objet_trouve.objet
             objet.situation = 'terminé'
             objet.save()

             return HttpResponse(' Object deliver successfully')