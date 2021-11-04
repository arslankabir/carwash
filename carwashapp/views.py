from django.db import models
from django.db.models import fields
from django.views.generic import CreateView,ListView, TemplateView
from .forms import WashOrderForm,WasherProfileForm
from .models import Washer_Profile,Washing_Order
from django.shortcuts import redirect, render,get_object_or_404,HttpResponse
from django.db.models import Q
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic
from .utils import get_geo
# from .hf import distance_1
# Create your views here.


def indexview(request):
    form_order = WashOrderForm(request.POST)

    # washer_location = None
    # washer_distance = None

    # customer_location = None
    # customer_distance = None
    
    # obj = get_object_or_404(Washing_Order, id=1)
    geolocator = Nominatim(user_agent='carwashapp')
    
    ##getting coordinate points of washers
    washers = Washer_Profile.objects.all()
    print('washers: ',washers)
    points_lats = []
    points_longs = []
    # distance_stack = []
    for w in washers:
        points_lats.append(w.lat_w)
        points_longs.append(w.long_w)
    
    points = []
    for item in zip(points_lats,points_longs):
        points.append(item)


    
    print('point coordinates: ',points)
    
    # pointA = (points_lats[0],points_longs[0])
    # print(pointA)
    
    ##customer current location via ip address 
    ip_c = '119.158.121.70' #used for asif ali location
    #ip_c = '119.158.50.70'     #used for babbar azam location
    country, city, lat, lon = get_geo(ip_c)

    #for getting exact city from the dictionary
    # customer_location = geolocator.geocode(city,timeout=None)

    ##current location coordinates
    c_lat = lat
    c_lon = lon
    pointB = (c_lat, c_lon)
    print('point B customer coordinates: ',pointB)


    ##all distances and coordinates calculation
    distance_stack = []
    coords_stack = []
    for p in range(len(points)):
        # distance = round(geodesic(points[p], pointB).km, 2)
        coords = Geodesic.WGS84.Inverse(points[p][0],points[p][1], c_lat, c_lon)
        # print("coords: ",coords)
        distance = coords['s12']
        print("distance from point (a) coordinates to point (b) coordinates: ",distance)
        distance_stack.append(distance)
        coords_stack.append(coords)
    
    # print("distance stack: ",distance_stack)
    # print("coords stack: ",coords_stack)

    #shortest distance calculation
    distance_stack.sort()
    shortest_distance = distance_stack[0]
    # shortest_distance_in_m = shortest_distance*1000
    print('shortest washers distance: ',shortest_distance)
    # print('customer_distance: ',customer_distance)

    #getting coordinates of shortest distance washer
    min_washer_coords = []
    for cr in range(len(coords_stack)):
        if coords_stack[cr]['s12'] == shortest_distance:
            # print (coords_stack[cr]['lat1'])
            # print (coords_stack[cr]['lon1'])
            min_washer_coords.append(coords_stack[cr]['lat1'])
            min_washer_coords.append(coords_stack[cr]['lon1'])

    print('min_washer_coords: ',min_washer_coords)

    #shortest distance washer coordinates
    min_lat, min_lon = min_washer_coords

    #getting washer's other details via lat and lon
    if Washer_Profile.objects.filter(lat_w = min_lat , long_w = min_lon).exists():
            washer = Washer_Profile.objects.filter(lat_w = min_lat , long_w = min_lon)
            print("shortest distance washer: ",washer)

    # print(washer) 
    # print(type(washer))

    #getting washer's id assigning form
    w_values = washer.values()
    w_id = w_values[0]['id']  #dictionary within a list
    # print('nearest washer id:  ',w_id)

    #getting washer's status
    w_status = w_values[0]['is_available']
    # print("status of washer: ",w_status)

    #for shortest_distance round and making it kilometeres from meters
    m_shortest_distance = shortest_distance/1000
    d_shortest_distance = round(m_shortest_distance,2)
    print("shortest distance in km:",d_shortest_distance)

    # assigned_to = form_order.cleaned_data.get('assigned_to')
    # check = Washer_Profile.objects.filter(washer_name=assigned_to.washer_name).exists()
    
    print("washer status before: ",w_status)
    # washingorders = Washing_Order.objects.values()
    # print(washingorders)
    # check = Washing_Order.objects.filter(assigned_to = washer.get(pk=w_id)).exists()
    # check_false_washer = Washer_Profile.objects.filter(is_available = False)
    # print("check false washer: ",check_false_washer)
    # check = Washing_Order.objects.filter(assigned_to__is_available = False)
    # check2 = Washer_Profile.objects.filter(washingorder__assigned_to__is_available = False)
    # print("check_false_washer_in_order: ",check2)
    # cond = check.filter()
    
    
    # check2 = Washer_Profile.objects.filter(washingorder__assigned_to__is_available = False ,is_available = False)
    # print(check2)
    # if  check2 and w_status is False:
    #         washer.update(is_available = True)
    #         print("washer status updated: ",washer) 

    

    form_sub_cond = False
    if form_order.is_valid():

        instance = form_order.save(commit=False)
        form_sub_cond = Washer_Profile.objects.filter(is_available = True) and w_status == True
        if form_sub_cond:
            customer_name = form_order.cleaned_data.get('customer_name')
            car_model = form_order.cleaned_data.get('car_model')
            
            instance.customer_name = customer_name
            instance.car_model = car_model
            instance.customer_location = ip_c
            instance.long_c = c_lon
            instance.lat_c = c_lat
            instance.assigned_to = washer.get(pk = w_id)
            instance.distance = d_shortest_distance
            instance.save()


            washer.update(is_available = False)
            print("washer status updated: ",washer)  


            print('form submitted')
        else:
            print('washer is not available in your location')


    else:
        print('form not submitted yet')

        form_order = WashOrderForm()


    context = { 
        'form':form_order,
        'form_sub_cond': form_sub_cond,
        'washer_name' : w_values[0]['washer_name'],
        # 'distance': f'{d_shortest_distance}km'
        'distance': d_shortest_distance
     }

    return render(request, 'washing_order_form.html', context)


















# class WashingOrder(CreateView):
#     model = Washing_Order
#     template_name='washing_order_form.html'
#     fields = ['customer_name','car_model','customer_location','assigned_to']
#     def form_valid(self, form):
#         washer_pro = get_object_or_404(Washer_Profile)
#         print(washer_pro)
#         # self.object = form.save()
#         # self.object.assigned_to = self.request.user.userprofile
#         #self.object.post_owner = mypost.uploaded_by
#         # if washer_pro
#         # self.object.assigned_to = washer_pro
#         # self.object.save()
#         return redirect('/')










        # car_model = form.cleaned_data.get('car_model')
        # customer_location = form_order.cleaned_data.get('customer_location')
        ##for later use
        # assigned_to = form_order.cleaned_data.get('assigned_to')
        # if Washer_Profile.objects.filter(washer_name=assigned_to.washer_name).exists():
        #     washer = Washer_Profile.objects.filter(washer_name = assigned_to.washer_name)
        #     washer.update(is_available = False)
        #     print("washer status updated: ",washer)
        



        ##nearest distance calculation
        # customer_distance = form_order.cleaned_data.get('customer_distance')
        # washers = Washer_Profile.objects.all()
        # distance_stack = []
        # for w in washers:
        #     distance_stack.append(w.washer_distance)
        # distance_stack.sort()
        # print('minimum washers distances: ',distance_stack[0])
        # print('customer_distance: ',customer_distance)