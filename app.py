
from flask import Flask, url_for, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

pp.config['SECRET_KEY'] = "secretttkeeyyy"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def list_pets():
    """List pets"""
    pets = Pet.query.all()
    return render_template("homepage.html", pets=pets)

@app.route("/add", methods= ["GET","POST"])
def add_pet():
    """show the add pet form or add pet if post"""
    form = AddPetForm()

    if form.validate_on_submit():
        pet = Pet(name=form.name.daga, species = form.species.data, age=form.age.data, photo_url = form.photo_url.data, notes=form.notes.data )
        db.session.add(pet)
        db.session.commit()
        flash(f"New pet {pet.name} added")
        return redirect("/")
    else:
        return render_template("pet_add_form.html", form=form)
    
@app.route("/<int:pet_id>", methods=["GET","POST"])
def edit_pet(pet_id):
    """Edit pet""" 

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"{pet.name} updated")
        return redirect("/")
    else:
        return render_template("pet_edit_form.html",pet=pet, form=form)