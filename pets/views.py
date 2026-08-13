from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MedicalRecordForm, PetForm
from .models import Pet
from orders.models import Order

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
def create_pet_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, payment_status="paid", pet__isnull=True)

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.status = "pending"
            pet.save()
            order.pet = pet
            order.save()
            return redirect("pets:pet_created", public_code=pet.public_code)
    else:
        form = PetForm()

    return render(request, "pets/create_pet.html", {"form": form, "breed_choices": BREED_CHOICES, "order": order})


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
            return redirect("pets:edit_pet", pk=pet.pk)
    else:
        form = PetForm(instance=pet)

    medical_form = MedicalRecordForm()
    medical_records = pet.medical_records.all()

    return render(request, "pets/edit_pet.html", {
        "form": form, "pet": pet, "breed_choices": BREED_CHOICES,
        "medical_form": medical_form, "medical_records": medical_records,
    })


@login_required
def add_medical_record_view(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == "POST":
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.pet = pet
            record.save()
    return redirect("pets:edit_pet", pk=pet.pk)


def public_profile_view(request, public_code):
    pet = get_object_or_404(Pet, public_code=public_code, status="approved")
    session_key = f"medical_unlocked_{public_code}"
    unlocked = request.session.get(session_key, False)
    return render(request, "pets/public_profile.html", {"pet": pet, "medical_unlocked": unlocked})


def unlock_medical_history_view(request, public_code):
    pet = get_object_or_404(Pet, public_code=public_code, status="approved")
    if request.method == "POST":
        code = request.POST.get("access_code", "").strip()
        if code == pet.medical_access_code:
            request.session[f"medical_unlocked_{public_code}"] = True
        else:
            request.session[f"medical_unlock_error_{public_code}"] = True
    return redirect("pets:public_profile", public_code=public_code)