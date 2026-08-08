
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PetForm
from .models import Pet


@login_required
def create_pet_view(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.status = "pending"
            pet.save()
            return redirect("pets:pet_created", public_code=pet.public_code)
    else:
        form = PetForm()

    return render(request, "pets/create_pet.html", {"form": form})


def pet_created_view(request, public_code):
    return render(request, "pets/pet_created.html", {"public_code": public_code})



def public_profile_view(request, public_code):
    pet = get_object_or_404(Pet, public_code=public_code, status="approved")
    return render(request, "pets/public_profile.html", {"pet": pet})


@login_required
def my_pets_view(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, "pets/my_pets.html", {"pets": pets})


@login_required
def edit_pet_view(request, pk):
    # get_object_or_404 con owner=request.user asegura que nadie edite
    # una mascota que no es suya, ni adivinando el ID en la URL.
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()  # se publica directo, sin volver a "pending"
            return redirect("pets:my_pets")
    else:
        form = PetForm(instance=pet)

    return render(request, "pets/edit_pet.html", {"form": form, "pet": pet})