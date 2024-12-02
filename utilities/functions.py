import requests
import re
import json
import aiohttp
import asyncio
import itertools


# lists of versioning group
versions = {
    "sem_ver_3": [],
    "sem_ver_2": [],
    "v_star": [],
    "integer": [],
    "date_yyyy_mm_dd": [],
    "others": []
}


##################################################################################################
##################################### This is the serious code ###################################
##################################################################################################


# lock to ensure data integrity when accessisng the shared data
lock = asyncio.Lock()
# list to house api endpoints
api_endpoints = []
# list to house api base urls
api_base_url = []
# list to house api versions
api_versions = []

# Url, Non-U, total
version_location_data = [0, 0, 0]

# the number of version typess
endpoint_versions_count = {
    "sem_ver_3": 0,
    "sem_ver_2": 0,
    "v_star": 0,
    "integer": 0,
    "date_yyyy_mm_dd": 0,
    "others": 0
}

api_versions_count = {
    "sem_ver_3": 0,
    "sem_ver_2": 0,
    "v_star": 0,
    "integer": 0,
    "date_yyyy_mm_dd": 0,
    "others": 0
}


# version identifiers regex queries
identifiers = {
    "sem_ver_3": r"^(v|)\d+\.\d+\.\d+$",
    "sem_ver_2": r"^(v|)\d+\.\d+$",
    "v_star":  r"^v(\d+)(\.\d+)?(\.\d+)?(\([a-zA-Z]+\))?$",
    "integer2": r"^(d\{3}|\d{2}|\d{1})+$",
    "integer": r"^\d+$",
    "date_yyyy_mm_dd": r"^(?:\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2})$"
}


def identify_api_versions():
    """
    Identify all versions in a list of api endpoints
    """
    all_versions = list(itertools.chain(*api_versions))
    for version in all_versions:
        identify(version, api_versions_count)


def identify(version, versions_count):
    """
    Identify the version type of the provided "version" and keep track of the version type count
    Parameters: 
    version : version of an api

    """
    if re.match(identifiers["date_yyyy_mm_dd"], version):
        versions_count["date_yyyy_mm_dd"] += 1
    elif re.match(identifiers["v_star"], version):
        versions_count["v_star"] += 1
    elif re.match(identifiers["integer"], version):
        versions_count["integer"] += 1
    elif re.match(identifiers["sem_ver_3"], version):
        versions_count["sem_ver_3"] += 1
    elif re.match(identifiers["sem_ver_2"], version):
        versions_count["sem_ver_2"] += 1
    else:
        versions_count["others"] += 1


def get_links(link):
    """
    Get all the links from the provided url
    Parameters:
    link    :   the url that contains the apis in APIsguru
    return  :   the list of API links collected from APIsguru
    """

    response = requests.get(link)
    item = response.json()
    links_list = []
    count = 1000000000

    # access the json object to locate "versions" header and the "swaggerURL" header
    for key, value in item.items():
        if count > 0:
            try:
                sub = value["versions"]  # a list of versions
                # get the versions and add the versions to api_versions
                versions = list(map(str, value["versions"].keys()))
                api_versions.append(versions)
            except:
                pass
            finally:
                pass

            for k, v in sub.items():
                try:
                    links_list.append(v["swaggerUrl"])
                except:
                    pass
                finally:
                    pass
        count -= 1
    return links_list  # the list of swagger links of each version of each api


async def get_all_data(links):
    """
    Access each link asynchronouslly to gather API endpoints
    Parameters:
    links   :   swaggerURLs for each API service provider
    """

    # Access all the collected swaggerURLs asynchronously
    async with aiohttp.ClientSession() as session:
        jobs = [get_data(session, link) for link in links]
        await asyncio.gather(*jobs)


async def get_data(session, link):
    """
    Accessing each swaggerURL to extract API endpoints
    Parameters:
    session :   each session for handling individual swaggerURL
    link    :   swaggerURL
    """

    async with session.get(link) as response:
        data = await response.json()

        # lock to prevent simultaneous accessing of the shared list
        async with lock:
            retrive_data(data)


def retrive_data(data):
    """
    Extract API endpoints from each swaggerURL
    Parameters:
    data    :   swaggerURL
    """
    # the base URL
    url = ""
    # Get the base URL is such data exists
    try:
        if "servers" in data:
            servers = data["servers"]
            url = servers[0]["url"]
        elif "host" in data:
            url = data["host"]
        elif "basePath" in None:
            url = data["basePath"]
        api_base_url.append(url)
    except:
        # print("Exception Thrown")
        pass
    finally:
        pass

    # Get the endpoit paths if such data exists
    try:
        paths = data["paths"]
        links = paths.keys()
        for l in links:
            api_endpoints.append(f"{l}")
    except:
        # print("Exception Thrown")
        pass
    finally:
        pass


def extract_version_location():
    """
    Extract version location in each URLs
    """

    for l in api_endpoints:
        if locate_and_identify_endpoint_version(l):
            version_location_data[0] += 1
        else:
            version_location_data[1] += 1
        version_location_data[2] += 1


test_value = 0


def locate_and_identify_endpoint_version(link):
    """
    Split a url into multiple segments and check if the version is in the URL
    If the version is in the URL, identify it's type
    Parameters:
    link    :   swaggerURL
    return  :   True if the version information exists in the URL, False if not
    """

    # split the url by "/" to look for version information
    global test_value
    sub_strings = link.split("/")
    for s in sub_strings:
        if look_for_version(s):
            test_value += 1
            identify(f"{s}", endpoint_versions_count)
            return True
        else:
            sub_s = s.split(".")
            for s_ in sub_s:
                if look_for_version(s_):
                    test_value += 1
                    identify(f"{s}", endpoint_versions_count)
                    print(s)
                    return True
    return False


def look_for_version(checked_string):
    conditions = [re.search(identifiers["sem_ver_3"], checked_string),
                  re.search(identifiers["sem_ver_2"], checked_string),
                  re.search(identifiers["v_star"], checked_string),
                  re.search(identifiers["integer2"], checked_string),
                  re.search(identifiers["integer"], checked_string),
                  re.search(identifiers["date_yyyy_mm_dd"], checked_string)]
    return any(conditions)


def compile_version_data():
    """
    Prepare and compile version infomration to send to the javascript files
    Parameters:
    return  :   list [[url, non-url, total], version types]
    """
    version_information = []  # the list for returning purpose
    identify_api_versions()

    version_information.append(version_location_data)
    version_information.append(endpoint_versions_count)
    return version_information


def reset_data():
    """
    Reset values of the global varaibles to the original states
    """
    global api_endpoints
    api_endpoints = []
    global version_location_data
    version_location_data = [0, 0, 0]
    global api_versions_count
    api_versions_count = {
        "total": 0,
        "sem_ver_3": 0,
        "sem_ver_2": 0,
        "v_star": 0,
        "integer": 0,
        "date_yyyy_mm_dd": 0,
        "others": 0
    }
    global endpoint_versions_count
    endpoint_versions_count = {
        "total": 0,
        "sem_ver_3": 0,
        "sem_ver_2": 0,
        "v_star": 0,
        "integer": 0,
        "date_yyyy_mm_dd": 0,
        "others": 0
    }


def execute(url):
    reset_data()
    links = get_links(url)
    asyncio.run(get_all_data(links))
    extract_version_location()
    identify_api_versions()
    result = compile_version_data()

    # print(api_versions_count)
    # print()
    # print()
    # print()
    # print()
    # print(endpoint_versions_count)
    print(test_value)
    return result


def p():
    print(len(api_base_url))
    for i in api_base_url:
        print(i)

##### Functions for printing information #####


# execute("https://api.apis.guru/v2/list.json")

def test(test_str):
    pattern = r"^v(\d+)(\.\d+)?(\.\d+)?(\([a-zA-Z]+\))?$"
    if re.search(pattern, test_str):
        print("Match")
    else:
        print("Doesn't match")


def run():
    coll = ["v1.0.1", "v123", "v1.0",
            "v1.9(alpha)", "v1", "v1aplpha",  "v5(alpha)", "v1.0.1(alpha)", "v1.0.1alpha"]
    print(len(coll))
    for c in coll:
        result = test(c)
        # print(result)


run()

##################  Test Code ####################
########## Will Handle it later ##################
