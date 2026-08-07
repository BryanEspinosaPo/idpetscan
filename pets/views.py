from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PetForm


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