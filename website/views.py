from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Workout

views = Blueprint("views",__name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html",user=current_user)

@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route("/workout", methods=['GET', 'POST'])
@login_required
def workout():
    if request.method == 'POST':
        exercise_name = request.form.get('exercise_name')
        sets = request.form.get('sets')
        weight = request.form.get('weight')
        
        if exercise_name and sets.isdigit() and weight.replace('.', '', 1).isdigit():
            new_workout = Workout(
                exercise_name=exercise_name,
                sets=int(sets),
                weight=float(weight),
                user_id=current_user.id
            )
            db.session.add(new_workout)
            db.session.commit()
            flash('Workout added successfully!', category='success')
        else:
            flash('Invalid input. Please check your entries.', category='error')

    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return render_template("workout.html", user=current_user, workouts=workouts)

@views.route("/delete-workout/<int:id>")
@login_required
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    if workout.user_id != current_user.id:
        flash('Unauthorized action.', category='error')
    else:
        db.session.delete(workout)
        db.session.commit()
        flash('Workout deleted successfully!', category='success')
    return redirect(url_for('views.workout'))

@views.route("/edit-workout/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_workout(id):
    workout = Workout.query.get_or_404(id)
    if workout.user_id != current_user.id:
        flash('Unauthorized action.', category='error')
        return redirect(url_for('views.workout'))
    
    if request.method == 'POST':
        workout.exercise_name = request.form.get('exercise_name')
        workout.sets = request.form.get('sets')
        workout.weight = request.form.get('weight')
        
        if workout.exercise_name and workout.sets.isdigit() and workout.weight.replace('.', '', 1).isdigit():
            workout.sets = int(workout.sets)
            workout.weight = float(workout.weight)
            db.session.commit()
            flash('Workout updated successfully!', category='success')
            return redirect(url_for('views.workout'))
        else:
            flash('Invalid input. Please check your entries.', category='error')

    return render_template("edit_workout.html", user=current_user, workout=workout)
