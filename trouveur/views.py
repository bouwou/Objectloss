from django.shortcuts import render, redirect

from trouveur.forms import PersonneForm, ObjetForm, ObjetTrouveForm
from trouveur.models import User, Objet, ObjetTrouve, Personne, ObjetReceptionne, ObjetDelivre


def index(request):
    return redirect('signaler_objet')

def signaler(request, id=0):
    form1 = PersonneForm()
    form2 = ObjetForm()
    form3 = ObjetTrouveForm()

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
    if request.method == "GET":
        if id == 0:
            form1 = PersonneForm()
            form2 = ObjetForm()  # si on n'a pas passé d'id le formulaire sera vide
            form3 = ObjetTrouveForm()
        else:
            objet = ObjetTrouve.objects.get(pk=id)
            form1 = PersonneForm(instance=objet.objet.personne)
            form2 = ObjetForm(instance=objet.objet)  # si on n'a pas passé d'id le formulaire sera vide
            form3 = ObjetTrouveForm(instance=objet)

        return render(request, 'fr/public/trouveur/signaler_objet.html',
                      {'personne_form': form1, 'objet_form': form2, 'objet_trouve_form': form3, 'logged_user': logged_user})
    else:
        if id == 0:
            form1 = PersonneForm(request.POST)
            form2 = ObjetForm(request.POST)  # si on n'a pas passé d'id le formulaire sera vide
            form3 = ObjetTrouveForm(request.POST)
        else:
            objet = ObjetTrouve.objects.get(pk=id)
            form1 = PersonneForm(request.POST, instance=objet.objet.personne)
            form2 = ObjetForm(request.POST, instance=objet.objet)  # si on n'a pas passé d'id le formulaire sera vide
            form3 = ObjetTrouveForm(request.POST, instance=objet)

        if form1.is_valid():
            if form2.is_valid():
                if form3.is_valid():
                    form1.save()
                    if id == 0:
                        new_objet = Objet(
                            personne=Personne.objects.last(),
                            statut='Retrouvé',
                            situation='trouvé',
                            nom_objet=form2.cleaned_data['nom_objet'],
                            type_objet=form2.cleaned_data['type_objet'],
                            id_objet=form2.cleaned_data['id_objet'],
                        )
                        new_objet.save()
                        new_objet_trouve = ObjetTrouve(
                            objet=Objet.objects.all().last(),
                            lieu_trouver=form3.cleaned_data['lieu_trouver'],
                            description=form3.cleaned_data['description'],
                        )
                        new_objet_trouve.save()
                    else:
                        form2.save()
                        form3.save()
                    return redirect('signaler_objet')
    return render(request, 'fr/public/trouveur/signaler_objet.html',
                  {'personne_form': form1, 'objet_form': form2, 'objet_trouve_form': form3, 'logged_user': logged_user})

def objets(request):
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
                    return redirect('home')

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


        return render(request, 'fr/public/trouveur/mes_objets.html', {'objets': mes_objets, 'objets_retr': mes_objets_retr, 'logged_user': logged_user})


def objet_delete(request, id):
    objet = ObjetTrouve.objects.get(pk=id, supprimer=0)
    objet.supprimer = 1
    objet.save()
    return redirect('mes_objets')

def solde(request):
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

    return render(request, 'fr/public/trouveur/solde.html',
                  {'objets': mes_objets, 'prix_total': prix_total, 'prix_attente': prix_attente, 'logged_user': logged_user})

