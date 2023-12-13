import pickle
import asyncio
from django.views.decorators.http import require_GET
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.shortcuts import render
from django.http import HttpResponse
from .root.gate_checker import Gate_checker
from .root.gate_scrape import Gate_scrape_thread
from .root.MET_TAF_parse import Metar_taf_parse
from .root.dep_des import Pull_flight_info
from time import sleep
from django.shortcuts import render
from django.http import JsonResponse

'''
views.py runs as soon as the base web is requested. Hence, GateCheckerThread() is run in the background right away.
It will then run 
'''
run_lengthy_web_scrape = False 

if run_lengthy_web_scrape:
    print('Running Lengthy web scrape')
    gc_thread = Gate_scrape_thread()
    gc_thread.start()

current_time = Gate_checker().date_time()


def home(request):
    # Homepage first skips a "POST", goes to else and returns home.html since the query is not submitted yet.
    if request.method == "POST":
        main_query = request.POST.get('query','')
        
        # This one adds similar queries to the admin panel in SearchQuerys.
        # Make it such that the duplicates are grouped using maybe unique.
        # search_query = SearchQuery(query=main_query)      # Adds search queries to the database
        # search_query.save()                               # you've got to save it otherwise it wont save
        
        return parse_query(request, main_query)

    else:
        return render(request, 'home.html')


def parse_query(request, main_query):
    main_query = main_query
    query_in_list_form = []     # Global variable since it is used outside of the if statement in case it was not triggered. purpose: Handeling Error
                                    # if .split() method is used outside here it can return since empty strings cannot be split.
                                    
    if main_query == '':        # query is empty then return all gates
        print('Empty query: Inside just prior to the gate_info func')
        return gate_info(request, main_query='')
    if 'DUMM' in main_query.upper():
        return dummy(request)
    if main_query == 'ext d':
        return dummy2(request)
    
    if main_query != '':
        query_in_list_form = main_query.split()
        if len(query_in_list_form) == 1:            # If query is only one word or item  
            query = query_in_list_form[0].upper()           # this is string form instead of list
            if query[:2] == 'UA' or query[:3] == 'GJS':         # Here you can also account for other airlines
                airline_code = None         
                if query[0] == 'G':
                    airline_code, flgiht_digits = query[:3], query[3:]          # Its GJS
                else:
                    flgiht_digits = query[2:]       # Its UA
                print('\nSearching for:', airline_code,flgiht_digits)
                return flight_deets(request, airline_code=airline_code,flight_number_query=flgiht_digits)
            elif 'A' in query or 'B' in query or 'C' in query or len(query) == 1:     # Accounting for 1 letter only
                # When the length of query_in_list_form is only 1 it returns gates table for that particular query.
                gate_query = query
                return gate_info(request, main_query=gate_query)
            elif len(query) == 4 or len(query) == 3 or len(query) == 2:
                if query.isdigit():
                    query = int(query)
                    if 1 <= query <= 35 or 40 <= query <= 136:
                        return gate_info(request, main_query=str(query))
                    else:
                        return flight_deets(request,airline_code=None,flight_number_query=query)
                else:
                    return gate_info(request, main_query=str(query))
            else:
                gate_query = query
                return gate_info(request, main_query=gate_query)


    if len(query_in_list_form) > 1:
        first_letter = query_in_list_form[0].upper()        # Making it uppercase for compatibility issues and error handling
        if first_letter == 'W':
            weather_query_airport  = query_in_list_form[1]
            weather_query_airport = weather_query_airport.upper()       # Making query uppercase for it to be compatible
            return metar_display(request, weather_query_airport)

        if first_letter == 'I':        
            return flight_deets(request,airline_code=None,query_in_list_form=query_in_list_form)
        else:       # If the query is not recognized:
            return gate_info(request, main_query=main_query)
            '''
            # Attempting to pull all airports for easier search access
            florida_airports = airports['Florida'][1]
            for each_airport in florida_airports:
                if each_query in each_airport:
                    print(each_airport)
                flights = Gate_checker().departures_ewr_UA()
                print(3)
                for flt in flights:
                    # print(flt)
                    if each_query in flt:
                        print(4)
                        return flight_deets(request, abs_query, flt)
                    else:
                        # return a static html saying no information found for flight number ****
                        pass'''


def dummy(request):
    try:
        bulk_flight_deets_path = r"C:\Users\ujasv\OneDrive\Desktop\codes\Cirrostrats\dj\latest_bulk_11_30.pkl"
        bulk_flight_deets = pickle.load(open(bulk_flight_deets_path, 'rb'))
    except:
        bulk_flight_deets = pickle.load(open(r'/Users/ismailsakhani/Desktop/Cirrostrats/dj/latest_bulk_11_30.pkl', 'rb'))
    
    # print('OLD with html highlights', bulk_flight_deets)

    try: # UJ PC PATH
        ind = r"C:\Users\ujasv\OneDrive\Desktop\codes\Cirrostrats\dj\raw_weather_dummy_dataKIND.pkl"
        ord = r"C:\Users\ujasv\OneDrive\Desktop\codes\Cirrostrats\dj\raw_weather_dummy_dataKORD.pkl"
        with open(ind, 'rb') as f:
            dep_weather = pickle.load(f)
        with open(ord, 'rb') as f:
            dest_weather = pickle.load(f)
        
        weather = Metar_taf_parse()
        bulk_flight_deets['dep_weather'] = weather.scrape(dummy=dep_weather)
        weather = Metar_taf_parse()
        bulk_flight_deets['dest_weather'] = weather.scrape(dummy=dest_weather)

    except Exception as e:     # ISMAIL MAC PATH
        print(e)
        is_ind = r"/Users/ismailsakhani/Desktop/Cirrostrats/dj/raw_weather_dummy_dataKIND.pkl"
        is_ord = r"/Users/ismailsakhani/Desktop/Cirrostrats/dj/raw_weather_dummy_dataKORD.pkl"
        with open(is_ind, 'rb') as f:
            dep_weather = pickle.load(f)
        with open(is_ord, 'rb') as f:
            dest_weather = pickle.load(f)
        weather = Metar_taf_parse()
        bulk_flight_deets['dep_weather'] = weather.scrape(dummy=dep_weather)
        weather = Metar_taf_parse()
        bulk_flight_deets['dest_weather'] = weather.scrape(dummy=dest_weather)
    
    # print('NEW WEATHER WITH NEW: HIGHLIGHTS', bulk_flight_deets)
    
    return render(request, 'flight_deet.html', bulk_flight_deets)


def gate_info(request, main_query):
    gate = main_query
    # In the database all the gates are uppercase so making the query uppercase    
    gate = gate.upper()

    # Dictionary format a list with one or many dictionaries each dictionary containing 4 items:gate,flight,scheduled,actual

    current_time = Gate_checker().date_time()
    gate_data_table = Gate_checker().ewr_UA_gate(gate)

    # showing info if the info is found else it falls back to `No flights found for {{gate}}`on flight_info.html
    if gate_data_table: 
        # print(gate_data_table)
        return render(request, 'flight_info.html',{'gate_data_table': gate_data_table, 'gate': gate, 'current_time': current_time})
    else:       # Returns all gates since query is empty. Maybe this is not necessary. Try deleting else statement.
        return render(request, 'flight_info.html', {'gate': gate})


def flight_deets(request,airline_code=None, flight_number_query=None):
    # given a flight number it returns its, gates, scheduled and actual times of departure and arrival

    flt_info = Pull_flight_info()           # from dep_des.py file
    weather = Metar_taf_parse()         # from MET_TAF_parse.py
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures1 = executor.submit(flt_info.fs_dep_arr_timezone_pull, flight_number_query)
        futures2 = executor.submit(flt_info.fa_data_pull, airline_code, flight_number_query)
        futures_dep_des = executor.submit(flt_info.united_departure_destination_scrape, flight_number_query)
    
    results = []
    for future in as_completed([futures1,futures2, futures_dep_des]):
        results.append(future.result())
    bulk_flight_deets = {}
    for i in results:
        if 'origin' in i.keys():
            flight_aware_data_pull = i
        else:
            bulk_flight_deets.update(i)
    
    UA_departure_ID, UA_destination_ID = bulk_flight_deets['departure_ID'], bulk_flight_deets['destination_ID']
    fa_departure_ID, fa_destination_ID = flight_aware_data_pull['origin'], flight_aware_data_pull['destination']
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures3 = executor.submit(weather.scrape, fa_departure_ID)
        futures4 = executor.submit(weather.scrape, fa_destination_ID)
        futures5 = executor.submit(flt_info.nas_final_packet, fa_departure_ID, fa_destination_ID) # NAS
        futures6 = executor.submit(flt_info.flight_view_gate_info, flight_number_query, fa_departure_ID) # Takes forever to load
    
    for future in as_completed([futures5,futures6]):
        bulk_flight_deets.update(future.result())
    bulk_flight_deets['dep_weather'] = futures3.result()
    bulk_flight_deets['dest_weather'] = futures4.result()
    
    # Here associating None values for fa_data seems unnecessary. could rather use it and dump unreliable data.
    if  UA_departure_ID != fa_departure_ID and UA_destination_ID != fa_destination_ID:
        for keys in flight_aware_data_pull.keys():
            flight_aware_data_pull[keys]= 'N/A'

    bulk_flight_deets.update(flight_aware_data_pull)
    
    # Extracting metar for a dummy file
    # with open('latest_bulk_11_28.pkl', 'wb') as f:
        # print("**DUMPING BULK_FLIGHT_DEETS AS latest_bulk PKL FILE**")
        # pickle.dump(bulk_flight_deets, f)
    # extracting metar for a dummy file
    # with open('lifr.pkl', 'wb') as f:
        # pickle.dump(bulk_flight_deets, f)
    
    return render(request, 'flight_deet.html', bulk_flight_deets)


def metar_display(request,weather_query):
    
    weather_query = weather_query.strip()       # remove leading and trailing spaces. Seems precautionary.
    airport = weather_query[-4:]
    
    weather = Metar_taf_parse()
    weather = weather.scrape(weather_query)
    
    return render(request, 'metar_info.html', {'airport': airport, 'weather': weather})


class Menu_pages:
    def __init__(self) -> None:
        pass
    
def contact(request):
    return render(request, 'contact.html')


def ourstory(request):
    return render(request, 'ourstory.html')


def source(request):
    return render(request, 'source.html')


def gate_check(request):
    return render(request, 'gate_check.html')


def flight_lookup(request):
    return render(request, 'home.html', {'flight_lookup': True})


def weather(request):
    return render(request, 'weather.html')
    

def guide(request):
    return render(request, 'guide.html')


def report_an_issue(request):
    return render(request, 'report_an_issue.html')

def live_map(request):
    return render(request, 'live_map.html')

def dummy2(request):
    print("dummy2 area")
    return(render(request, 'dummy2.html'))

# This function gets loaded within the dummy2 page whilst dummy2 func gets rendered.
@require_GET
def data_v(request):        
    
    sleep(0.5)
    try:
        bulk_flight_deets_path = r"C:\Users\ujasv\OneDrive\Desktop\codes\Cirrostrats\dj\latest_bulk_11_30.pkl"
        bulk_flight_deets = pickle.load(open(bulk_flight_deets_path, 'rb'))
    except:
        bulk_flight_deets = pickle.load(open('/Users/ismailsakhani/Desktop/Cirrostrats/dj/latest_bulk_11_30.pkl', 'rb'))
    for a, b in bulk_flight_deets.items():
        print(a,type(b))
        if a=='registration':
            print(b)
    return JsonResponse(bulk_flight_deets)