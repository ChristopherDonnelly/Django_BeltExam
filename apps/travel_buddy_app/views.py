from __future__ import unicode_literals 
 
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.utils.html import escape 
from django.contrib import messages
from ..users_app.models import User
from .models import TripPlan
 
class Route(object):
    REDIRECT_ROUTE = '/'
    
def index(request):
    if not 'user_session' in request.session:
        return redirect(Route.REDIRECT_ROUTE)
    else:
        user = User.objects.get(id = request.session['user_session'])
        trips = TripPlan.objects.all().exclude(joined_users = user)
        schedules = TripPlan.objects.filter(joined_users = user)
        context = {
            'user': user,
            'schedules': schedules,
            'trips': trips

        }
        return render(request, "travel_buddy_app/index.html", context) 

def add_plan(request):
    if not 'user_session' in request.session:
        return redirect(Route.REDIRECT_ROUTE)
    else:
        return render(request, "travel_buddy_app/add.html") 

def add_new_trip(request):
    if not 'user_session' in request.session:
        return redirect(Route.REDIRECT_ROUTE)
    else:
        goto = '/travels/'
        response = TripPlan.objects.trip_validator(request.POST, request.session['user_session'])

        if not response['status']:
            for tag, error in response['errors'].iteritems():
                messages.error(request, error, extra_tags=tag)
            
            goto = '/travels/add/'
        
        return redirect(goto)

def destination(request, plan_id):
    if not 'user_session' in request.session:
        return redirect(Route.REDIRECT_ROUTE)
    else:
        trip_exist = TripPlan.objects.filter(id = plan_id)

        if len(trip_exist) > 0:
            trip = trip_exist[0]
            users = User.objects.filter(joined_trips = trip).exclude(id = trip.trip_planner.id)

            context = {
                'trip': trip,
                'users': users
            }
        else:
            context = {
                'trip': {
                    'destination': 'Trip ID not found',
                    'trip_planner': {
                        'name': '-----',
                    },
                    'description': '-----',
                    'start_date': '-----',
                    'end_date': '-----'
                },
                'users': {}
            }
        return render(request, "travel_buddy_app/destination.html", context) 

def join(request, plan_id):
    if not 'user_session' in request.session:
        return redirect(Route.REDIRECT_ROUTE)
    else:
        trip_exist = TripPlan.objects.filter(id = plan_id)

        if len(trip_exist) > 0:
            response = TripPlan.objects.join_validator(plan_id, request.session['user_session'])

            if not response['status']:
                for tag, error in response['errors'].iteritems():
                    messages.error(request, error, extra_tags=tag)
        
        return redirect('/travels/')
