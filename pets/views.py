from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MedicalRecordForm, PetForm
from .models import Pet
import json

from orders.models import Order

DOG_BREEDS = [
    "Mestizo / Criollo", "Labrador Retriever", "Golden Retriever", "Pastor Alemán",
    "Bulldog Francés", "Bulldog Inglés", "Caniche / Poodle", "Chihuahua", "Schnauzer",
    "Beagle", "Boxer", "Rottweiler", "Husky Siberiano", "Yorkshire Terrier", "Shih Tzu",
    "Pug", "Dálmata", "Doberman", "Salchicha", "Cocker Spaniel", "Border Collie",
]

CAT_BREEDS = [
    "Gato Criollo", "Gato Persa", "Gato Siamés", "Gato Angora",
    "Maine Coon", "Gato Sphynx", "Bengalí", "Ragdoll", "Británico de Pelo Corto",
]

BREED_CHOICES = DOG_BREEDS + CAT_BREEDS


def home_view(request):
    lost_pets = (
        Pet.objects.filter(status="approved", is_lost=True)
        .order_by("-last_seen_date")[:8]
    )
    return render(request, "home.html", {"lost_pets": lost_pets})


@login_required
def create_pet_view(request, order_id):
    from datetime import date, timedelta
    from django.utils import timezone
    from .emails import send_admin_notification, send_owner_status_email
    from .utils import generate_qr_for_pet

    order = get_object_or_404(Order, id=order_id, user=request.user, payment_status="paid")

    if order.pets_remaining <= 0:
        return redirect("pets:my_pets")

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.status = "approved"
            pet.approved_at = timezone.now()
            pet.order = order
            pet.clinical_history_enabled = order.includes_medical_history
            pet.renewal_due_date = date.today() + timedelta(days=365)
            pet.subscription_active = True
            pet.save()

            generate_qr_for_pet(pet)
            pet.save()
            send_admin_notification(pet)
            send_owner_status_email(pet)

            if order.pets_remaining > 0:
                return redirect("pets:create_pet", order_id=order.id)
            return redirect("pets:pet_created", public_code=pet.public_code)
    else:
        form = PetForm()

    return render(request, "pets/create_pet.html", {
        "form": form, "breed_choices": BREED_CHOICES, "order": order,
        "dog_breeds_json": json.dumps(DOG_BREEDS), "cat_breeds_json": json.dumps(CAT_BREEDS),
    })


def pet_created_view(request, public_code):
    return render(request, "pets/pet_created.html", {"public_code": public_code})


@login_required
def my_pets_view(request):
    pets = Pet.objects.filter(owner=request.user)
    paid_orders = Order.objects.filter(user=request.user, payment_status="paid")
    available_orders = [o for o in paid_orders if o.pets_remaining > 0]
    return render(request, "pets/my_pets.html", {"pets": pets, "available_orders": available_orders})


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
        "dog_breeds_json": json.dumps(DOG_BREEDS), "cat_breeds_json": json.dumps(CAT_BREEDS),
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
    if not pet.is_subscription_valid:
        return render(request, "pets/profile_inactive.html", {"pet": pet})
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