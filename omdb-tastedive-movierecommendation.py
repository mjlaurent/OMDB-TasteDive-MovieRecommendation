import requests_with_caching
import json
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_movies_from_tastedive("Bridesmaids")
def get_movies_from_tastedive(movie):
    parameter = {'q':movie,'type':"movies",'limit':5}
    response = requests_with_caching.get('https://tastedive.com/api/similar',params=parameter)
    converted_response = json.loads(response.text)
    return converted_response


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# extract_movie_titles(get_movies_from_tastedive("Tony Bennett"))
# extract_movie_titles(get_movies_from_tastedive("Black Panther"))

def extract_movie_titles(movie_title):
    results = []
    for i in range(len(movie_title['Similar']['Results'])):
        results.append(movie_title['Similar']['Results'][i]["Name"])
    return results

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_related_titles(["Black Panther", "Captain Marvel"])
# get_related_titles([])

def get_related_titles(list_of_titles):
    result_list = []
    for title in list_of_titles:
        get_values = extract_movie_titles(get_movies_from_tastedive(title))
        for extracted_titles in get_values:
            if extracted_titles not in result_list:
                result_list.append(extracted_titles)
    return result_list

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_movie_data("Venom")
# get_movie_data("Baby Mama")

def get_movie_data(title):
    parameter = {'t':title , "r":'json'}
    get_request = requests_with_caching.get("http://www.omdbapi.com/",params= parameter)
    result = json.loads(get_request.text)
    return result
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_movie_rating(get_movie_data("Deadpool 2"))

def get_movie_rating(api_result):
    rating = 0
    for internet_rating in api_result['Ratings']:
        if internet_rating['Source'] == 'Rotten Tomatoes':
            rating = int(internet_rating['Value'].strip('%'))
    return rating
    

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

def get_sorted_recommendations(value):
    result_dict = {}
    for movie in value:
        recommendation = extract_movie_titles(get_movies_from_tastedive(movie))
        for i in recommendation:
            rating = get_movie_rating(get_movie_data(i))
            result_dict[i] = rating
    
    return sorted(result_dict,key=lambda x:(result_dict[x],x[0]),reverse=True)
    
            
