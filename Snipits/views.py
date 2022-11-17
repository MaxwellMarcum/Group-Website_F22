from datetime import datetime
from flask import Blueprint, render_template, request, flash, current_app as app, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Trip, User, Friends
from . import db
import folium
from flask_sqlalchemy import SQLAlchemy
from . import time_till
from . import friendsfuncs
import uuid

views = Blueprint('views', __name__)
@views.route('/trip-summary-map/<tripId>', methods=['GET', 'POST'])
def trip_summary_map(tripId):
    trip = Trip.query.filter_by(id = tripId).first()
    start_coords = (trip.latitude, trip.longitude)
    folium_map = folium.Map(min_zoom = 6, center=start_coords,tiles="Stamen Terrain")
    if trip.trip_type == 1:
        icon_color = "red"
    elif trip.trip_type == 2:
        icon_color = "blue"
    elif trip.trip_type == 3:
        icon_color = "green"
    elif trip.trip_type == 4:
        icon_color = "purple"
    else:
        icon_color = "yellow"
    folium.Marker(location = start_coords,popup=f'<p>{trip.name}</p>', 
    icon = folium.Icon(color = icon_color, icon = "info-sign") ).add_to(folium_map)
    return folium_map._repr_html_()

@views.route('events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        if request.form['submit_button'] == 'create trip':
            date_in = request.form.get('tripDate')
            time_in = request.form.get('tripTime')
            name_in = request.form.get('name')
            desc_in = request.form.get('desc')
            lat_in = request.form.get('lat')
            lon_in = request.form.get('lon')
            tripType_in = request.form.get('tripType')
            num_people_in = request.form.get('num_people')
            date_time = datetime.strptime(date_in + " " + time_in,"%Y-%m-%d %H:%M")
            if len(name_in) < 1:
                flash('Trip name is too short!', category='error')
            else:
                new_trip = Trip(name = name_in, desc = desc_in, trip_type = tripType_in, date = date_time, num_people = num_people_in, user_id=current_user.id, latitude = lat_in, longitude = lon_in)
                db.session.add(new_trip)
                db.session.commit()
                flash('Trip added!', category='success')

    return render_template("events.html", user=current_user, time_till=time_till.count_time)

@views.route('friends', methods=['GET', 'POST'])
@login_required
def friends():
    if request.method == 'POST':
        if request.form['Add_friend_button'] == 'Add Friend':
            username_in = request.form.get('username')
            if len(username_in) < 1:
                flash('Username is too short!', category='error')
            else:
                friend2 = User.query.filter_by(username = username_in).first()
                if friend2:
                    new_friends1 = Friends(friend1_id = current_user.id, friend2_id = friend2.id, status = 2)
                    new_friends2 = Friends(friend2_id = current_user.id, friend1_id = friend2.id, status = 1)
                    db.session.add(new_friends1)
                    db.session.add(new_friends2)
                    db.session.commit()
                    new_friends1.partner_link = new_friends2.id
                    new_friends2.partner_link = new_friends1.id
                    db.session.commit()
                else:
                    flash('not found', category='error')

    return render_template("friends.html", user=current_user, getfriend = friendsfuncs.getfriend)

@views.route('/friend/<friendship_id>', methods=['GET', 'POST'])
def friend(friendship_id):
    friendship = Friends.query.filter_by(id = friendship_id).first()
    friend2 = User.query.filter_by(id = friendship.friend2_id).first()

    if request.method == 'POST':
        if request.form['Friendship_Button'] == 'Accept':
            friendsfuncs.acceptfriend(friendship_id)
        elif request.form['Friendship_Button'] == 'Reject':
            friendsfuncs.rejectfriend(friendship_id)
            return redirect(url_for('views.friends'))

    return render_template("friend.html", friendship = friendship, friend2 = friend2, time_till=time_till.count_time)

@views.route('/map')
def index():
    start_coords = (35, -83)
    folium_map = folium.Map(min_zoom = 4, center=start_coords,tiles="Stamen Terrain")
    list = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.id).all()
    for item in list:
        if item.latitude != None and item.longitude != None:
            marker_coords = (item.latitude,item.longitude)
            if item.trip_type == 1:
                icon_color = "red"
            elif item.trip_type == 2:
                icon_color = "blue"
            elif item.trip_type == 3:
                icon_color = "green"
            elif item.trip_type == 4:
                icon_color = "purple"
            else:
                icon_color = "yellow"
                
            folium.Marker(location = marker_coords,popup=f'<a href="/trip-summary/{item.id}"> {item.name}</a>', 
            icon = folium.Icon(color = icon_color, icon = "info-sign") ).add_to(folium_map)
    return folium_map._repr_html_()