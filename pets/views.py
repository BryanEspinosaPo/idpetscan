from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PetForm
from .models import Pet

BREED_CHOICES = [
    "Mestizo / Criollo", "Labrador Retriever", "Golden Retriever", "Pastor Alemán",
    "Bulldog Francés", "Bulldog Inglés", "Caniche / Poodle", "Chihuahua", "Schnauzer",
    "Beagle", "Boxer", "Rottweiler", "Husky Siberiano", "Yorkshire Terrier", "Shih Tzu",
    "Pug", "Dálmata", "Doberman", "Gato Criollo", "Gato Persa", "Gato Siamés",
    "Gato Angora", "Maine Coon",
]


def home_view(request):
    lost_pets = (
        Pet.objects.filter(status="approved", is_lost=True)
        .order_by("-last_seen_date")[:8]
    )
    return render(request, "home.html", {"lost_pets": lost_pets})


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

    return render(request, "pets/create_pet.html", {"form": form, "breed_choices": BREED_CHOICES})


def pet_created_view(request, public_code):
    return render(request, "pets/pet_created.html", {"public_code": public_code})


@login_required
def my_pets_view(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, "pets/my_pets.html", {"pets": pets})


@login_required
def edit_pet_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect("pets:my_pets")
    else:
        form = PetForm(instance=pet)

    return render(request, "pets/edit_pet.html", {
        "form": form, "pet": pet, "breed_choices": BREED_CHOICES,
    })


def public_profile_view(request, public_code):
    pet = get_object_or_404(Pet, public_code=public_code, status="approved")
    return render(request, "pets/public_profile.html", {"pet": pet})