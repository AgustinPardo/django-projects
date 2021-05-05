from django.shortcuts import render, redirect
from .forms import RegForm
# Create your views here.
def inicio(request):
    titulo = "Hola"
    if request.user.is_authenticated:
        titulo = "Bienvenido %s" %(request.user)

    if request.method == 'POST':
        form = RegForm(request.POST)
        #print(form["email"].value())
        if form.is_valid():
            instance = form.save(commit=False)
            if not instance.nombre:
                instance.nombre="Persona"
            instance.save()
            return redirect('inicio')
        else:
            context={"form":form, "titulo":titulo}
            return render(request, 'boletin/inicio.html', context)
    else:
        form = RegForm()
        context={"form":form, "titulo":titulo}
        return render(request, 'boletin/inicio.html', context)