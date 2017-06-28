# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import User, Trip

# Create your views here.
def index(request):
	return render(request, 'travel_app/index.html')

def register(request):
	post_data = request.POST.copy()
	result = User.objects.register(post_data)
	if isinstance(result, list):
		for err in result:
			messages.error(request, err)
		return redirect(reverse('travel:index'))
	else:
		request.session['user'] = result
		return redirect(reverse('travel:travels'))


def login(request):
    post_data = request.POST.copy()
    result = User.objects.login(post_data)
    if isinstance(result,list):
        for err in result:
            messages.error(request, err)
        return redirect(reverse('travel:index'))
    else:
        request.session['user'] = result
        return redirect(reverse('travel:travels'))

def travels(request):
	user = User.objects.get(id=request.session['user'])
	user_trips = Trip.objects.filter(planner=user)
	other_trips = Trip.objects.exclude(id__in=user_trips)
	attendee_list = Attendee.objects.all()
	context ={
		"user" : user,
		"user_trips" : user_trips,
		"other_trips" : other_trips,
		"attendee_list" : attendee_list
	}
	return render(request, 'travel_app/travels.html', context)

def join(request, destination_id):
	user = User.objects.get(id=request.session['user'])
	new_attendee = Attendee.objects.create(id=user)
	return redirect(reverse('travel:travels'))

def destination(request, destination_id):
	trip = Trip.objects.get(id=destination_id)
	context = {
		"trip" : trip
	}
	return render(request, 'travel_app/destination.html', context)

def post_trip(request):
	post_data = request.POST.copy()
	result = Trip.objects.validate(post_data, request.session['user'])
	if isinstance(result, list):
		for err in result:
			messages.error(request, err)
		return redirect(reverse('travel:add'))
	else:
		return redirect(reverse('travel:travels'))

def add(request):
	return render(request, 'travel_app/add.html')

def logout(request):
	request.session.pop('user')
	return redirect(reverse('travel:index'))