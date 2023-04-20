from django import *
from django.http import * 
from django.shortcuts import render
from .models import *
from django import forms
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages


def index(request):
    context = {}

    return render(request, 'index.html', context)

     
@login_required
def profile(request):
    return render(request,"registration/profile.html")



class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Tu contraseña ha sido cambiada con éxito.')
        return response


@login_required
def classificacio(request,lliga_id=None):
    lliga = Lliga.objects.first()
    if lliga_id:
        lliga = Lliga.objects.get(pk=lliga_id)
    equips = lliga.equips.all()
    classi = []
    for equip in equips:
        punts = 0
        for partit in lliga.partit_set.filter(equip_local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partit_set.filter(equip_visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append( (punts,equip.nom_equip) )
    classi.sort(reverse=True)
    return render(request,"classificacio.html",{"classificacio":classi})


class TriarLligaForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    
@login_required
def menu(request):
    form = TriarLligaForm()
    if request.method == "POST":
        form = TriarLligaForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{"form": form})

def crearPartit(request):
    form = TriarLligaForm()
    if request.method == "POST":
        form = TriarLligaForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('triarEquipsPartit',lliga.id)
    return render(request, "crearPartit.html",{"form": form})


class TriarEquipsPartitForm(forms.ModelForm):
    class Meta: 
        model = Partit
        fields = ["equip_local","equip_visitant"]

def triarEquipsPartit(request,lliga_id):
    lliga = Lliga.objects.get(pk=lliga_id)
    form = TriarEquipsPartitForm()
    message = ""
    if request.method == "POST":
        form = TriarEquipsPartitForm(request.POST)
        if form.is_valid():
            local = form.cleaned_data.get("equip_local")
            visitant = form.cleaned_data.get("equip_visitant")
            if local != visitant:
                partit = form.save(commit=False)
                partit.lliga = lliga
                
                if Partit.objects.filter(equip_local=local,equip_visitant=visitant,lliga = lliga):
                    message = "El partit ja existeix"
                else:
                    partit.save()
                    message = "Partit creat correctament"
            else: 
                message = "Els equips son iguals, no es pot crear el partit"
    return render(request,"crearPartit.html",{"form": form, "message": message})

class LligaForm(forms.ModelForm):
    class Meta:
        model = Lliga
        fields = ["nom_lliga","equips"]

def crearLliga(request):
    form = LligaForm()
    messageError  = ""
    if request.method == "POST":
        form = LligaForm(request.POST)
        if form.is_valid():
            titol = form.cleaned_data.get("nom_lliga")
            if Lliga.objects.filter(nom_lliga = titol):
                messageError = "El nom de la lliga ja existeix"
            else:
                messageError = "La lliga " + titol + " s'ha creat correctament"
                form.save()
    
    return render(request,"crearLliga.html",{"form": form, "message": messageError})


def edita_partit_advanced(request):
    return render(request, 'edita_partit_advanced.html')