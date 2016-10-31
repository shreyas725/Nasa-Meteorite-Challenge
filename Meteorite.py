import urllib.request, json
import googlemaps
import operator

#API KEY for Google Map Geocoding API
API_KEY =  'AIzaSyDaONMxYlq1ED9U1xQsyKxtL8kJe7VyW_Q' #Please add your own API KEY from google console

def load_json(url):
    '''
    gets the json data from url

    param:url It is a valid URL gives a valid json data
    return json object
    '''
    
    with urllib.request.urlopen(url) as response:
        data =  response.read().decode('utf-8')
    return json.loads(data)

def get_countries():
    '''
    gets the dictionary of country iso code and name from worldbank api and
    returns dictionary of countries
    '''
    url = "http://api.worldbank.org/countries/all/?format=json&per_page=500"
    data = load_json(url)
    data = data[1] #second value has the data
    #print (data)
    countries = dict()
    for row in data:
        countries[row['iso2Code']] = row ['name']
    return countries
    
    
def get_meteor_striked_countries(year, countryCodeList):
    #url = "https://data.nasa.gov/resource/gh4g-9sfh.json?year="+str(year)+"-01-01T00:00:00&$limit=100"
    url = "https://data.nasa.gov/resource/gh4g-9sfh.json?year="+str(year)+"-01-01T00:00:00"
    meteorStikeData = load_json(url)
    meteorStrikeList = []
    counter= dict()
    count= 1
    for meteorStrike in meteorStikeData:
        ##print(meteorStrike)
        meteorRecord = {}

        try:
            meteorRecord ['lat'] = meteorStrike['reclat']
            meteorRecord ['lng'] = meteorStrike['reclong']
            
            country = get_country_reverse_geocode(meteorRecord ['lat'],  meteorRecord ['lng'])
            if country["short_name"] in countryCodeList:
                meteorStrikeList.append(meteorRecord)
                counter[country["short_name"]] = counter.get(country["short_name"], 0) + 1
            
        except KeyError as e:
            #sometiem will return index error because of Lat Long not availabe
            #so we ignore it
            print (meteorStrike),
            print (e)
    print (count)
    count =+1
    return counter

def get_country_reverse_geocode(lat, lng):
    '''
    gets the country name from latitude longitude and
    returns dictionary country code and full name
    '''
    gmaps = googlemaps.Client(key= API_KEY)
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng),result_type=['country'])
    myLocation = reverse_geocode_result

    if (len(myLocation) == 0):
        return {"long_name": "Unknown", "short_name": "UN"}

    
    data =myLocation[0] #Getting First Location
    address = data['address_components'] #Getting  Address component lists
    addressDict = address[0] #Getting first Address
    return addressDict

def get_countries_with_technical_papers(year):
    '''
    gets the country who has publised a scientific paper

    param:year integer a valid year
    
    returns dictionary country code and full name
    '''
    url = "http://api.worldbank.org/countries/indicators/IP.JRN.ARTC.SC?format=json&per_page=500&date=" + str(year)
    data =  load_json (url) #JSON DATA
    data = data[1] #second value has the data
    countries = dict()
    
    for row in data:
        if row['value'] != 0.0:
            countries[row['country']['id']] = row['country']['value']
    return countries


if __name__ == '__main__':
    print ("--- GETTING THE COUNTRY LIST ---")
    countriesList = get_countries()

    print ("--- GETTING COUNTRIES WITH PUBLISHED TECHNICAL PAPER 2008 ---")
    countries2008 = get_countries_with_technical_papers(2008)
    #countries2010 = get_countries_with_technical_papers(2010)

    print ("--- GETTING METEOR STRIKED COUNTRIES WITH PUBLISHED TECHNICAL PAPER 2008 ---")
    meteorList2008 = get_meteor_striked_countries(2008, list(countries2008)) 
    #meteorList2008 = {'MA': 2, 'TN': 10, 'AR': 2, 'LY': 5, 'CN': 1, 'ID': 1, 'RO': 1, 'SE': 2, 'IN': 1, 'AU': 6, 'US': 25, 'CL': 21, 'SA': 5, 'TR': 1, 'EC': 1, 'CA': 1, 'SD': 1, 'OM': 166, 'DZ': 1} 
    
    #print ("--- SORTING THE COUNTRY LIST FOR 2008 ---")
    sortedMeteorList2008 = sorted(meteorList2008.items(), key=operator.itemgetter(1),reverse=True)

    
    print ("--- GETTING TOP 5 COUNTRIES 2008 ---")
    Top5Countries2008 = sortedMeteorList2008[0:5]
 
    print ("--- PRINTING  TOP 5 COUNTRIES 2008 ---")
    i = 1

    for countryCode, noOfStrikes in Top5Countries2008:
        print (str(i) + ") " + countriesList[countryCode] + " had " + str(noOfStrikes) + " strikes") 
        i += 1
    
    print ("--- GETTING COUNTRIES WITH PUBLISHED TECHNICAL PAPER 2010 ---")
    countries2010 = get_countries_with_technical_papers(2010)

    print ("--- GETTING METEOR STRIKED COUNTRIES WITH PUBLISHED TECHNICAL PAPER 2010 ---")
    meteorList2010 = get_meteor_striked_countries(2010, list(countries2010)) 
    #meteorList2010 = {'BR': 1, 'SK': 1, 'US': 14, 'EG': 2, 'SE': 2, 'LY': 4, 'TN': 12, 'MA': 2, 'OM': 199, 'AU': 6, 'CL': 109, 'CN': 1}  
    

    print ("--- SORTING THE COUNTRY LIST FOR 2010 ---")
    sortedMeteorList2010 = sorted(meteorList2010.items(), key=operator.itemgetter(1),reverse=True)

    
    print ("--- GETTING TOP 5 COUNTRIES 2010 ---")
    Top5Countries2010 = sortedMeteorList2010[0:5]
    
    print ("--- PRINTING  TOP 5 COUNTRIES 2010 ---")
    i = 1
    for countryCode, noOfStrikes in Top5Countries2010:
        print (str(i) + ") " + countriesList[countryCode] + " had " + str(noOfStrikes) + " strikes") 
        i += 1
    
    
    ''' SET DIFFENCE'''
    meteorSet2008 =  set (meteorList2008.keys())
    meteorSet2010 =  set (meteorList2010.keys())

    unique2008 = meteorSet2008 - meteorSet2010
    unique2010 = meteorSet2010 - meteorSet2008
    common20082010 = meteorSet2010 & meteorSet2008

  
    print ("--- COUNTRIES UNIQUE TO 2008 ---")

    i = 1
    for countryCode in unique2008:
        print (str(i) + ") " + countriesList[countryCode])
        i += 1
    
    print ("--- COUNTRIES UNIQUE TO 2010 ---")
    i = 1
    for countryCode in unique2010:
        print (str(i) + ") " + countriesList[countryCode])
        i += 1
        
    print ("--- COUNTRIES COMMON TO 2008 & 2010 ---")
    
    i = 1
    for countryCode in common20082010:
        print (str(i) + ") " + countriesList[countryCode])
        i += 1
    

    '''
    1) TOP 5 Countries 2008
        1) Oman had 166 strikes
        2) United States had 25 strikes
        3) Chile had 21 strikes
        4) Tunisia had 10 strikes
        5) Australia had 6 strikes
    2) TOP 5 Countries 2010
        1) Oman had 199 strikes
        2) Chile had 109 strikes
        3) United States had 14 strikes
        4) Tunisia had 12 strikes
        5) Australia had 6 strikes
    3)
        --- COUNTRIES UNIQUE TO 2008 ---
        1) Argentina
        2) India
        3) Saudi Arabia
        4) Turkey
        5) Canada
        6) Sudan
        7) Algeria
        8) Romania
        9) Ecuador
        10) Indonesia
        --- COUNTRIES UNIQUE TO 2010 ---
        1) Egypt, Arab Rep.
        2) Slovak Republic
        3) Brazil
    4)
        --- COUNTRIES COMMON TO 2008 & 2010 ---
        1) Australia
        2) Oman
        3) China
        4) Tunisia
        5) Chile
        6) Morocco
        7) United States
        8) Libya
        9) Sweden
    5) Can you infer anything from this data? Why or why not?  
        a) Oman has highest no of  Meteor Strikes in 2008 and 2010
        b) Total Countries where Meteor Strikes took place dropped in 2010
        c) There were 19 Countries in 2008 and 12 Countries in 2010 where Meteor Strikes took place
        d) Whereas, there were 1003 recorded Meteor strikes in 2010, and 955 recorded Meteor Strikes in 2008

    Additional API used.
    pip install -U googlemaps #googlemaps This package needs to be downloaded
    1) Google Maps Geocoding API
    ---- Used to get Country from GeoLocation of Meteor Strikes
    ---- Limitation of 2500 Requests from API per day
    
    '''
