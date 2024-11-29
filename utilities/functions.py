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


# return the number of versions in the file


##################################################################################################
##################################### This is the serious code ###################################
##################################################################################################


# lock to ensure data integrity when accessisng the shared data
lock = asyncio.Lock()
# list to house api endpoints
api_endpoints = []
api_base_ulr = []

api_versions = []

# Url, Non-U, total
version_location_data = [0, 0, 0]

# the number of version typess
versions_count = {
    "total": 0,
    "sem_ver_3": 0,
    "sem_ver_2": 0,
    "v_star": 0,
    "integer": 0,
    "date_yyyy_mm_dd": 0,
    "others": 0
}

endpoints = []

# version identifiers regex queries
identifiers = {
    "sem_ver_3": r"^(v|)\d+\.\d+\.\d+$",
    "sem_ver_2": r"^(v|)\d+\.\d+$",
    "v_star": r"v\d+$",
    "integer2": r"^(d\{3}|\d{2}|\d{1})+$",
    "integer": r"^\d+$",
    "date_yyyy_mm_dd": r"^(?:\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2})$"
}


def identify_all_versions(endpoints):
    """
    Identify all versions in a list of api endpoints
    """
    for endpoint in endpoints:
        sub_strings = endpoint.split("/")

   
def identify(version):
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
    count = 10

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
                    endpoints.append(k)
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
        servers = data["servers"]
        url = servers[0]["url"]
    except:
        try:
            base_url = data["host"]
            api_base_ulr.append(f"{base_url}")
        except:
            pass
        finally:
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
        pass
    finally:
        pass


def extract_version_location(collection):
    """
    Extract version location in each URLs
    """

    for l in collection:
        if locate_and_identify_endpoint_version(l):
            version_location_data[0] += 1
        else:
            version_location_data[1] += 1
        version_location_data[2] += 1


def locate_and_identify_endpoint_version(link):
    """
    Split a url into multiple segments and check if the version is in the URL
    Parameters:
    link    :   swaggerURL
    return  :   True if the version information exists in the URL, False if not
    """

    sub_strings = link.split("/")
    for s in sub_strings:
        conditions = [re.search(identifiers["sem_ver_3"], s),
                      re.search(identifiers["sem_ver_2"], s),
                      re.search(identifiers["v_star"], s),
                      re.search(identifiers["integer2"], s),
                      re.search(identifiers["integer"], s),
                      re.search(identifiers["date_yyyy_mm_dd"], s)]
        if any(conditions):
            identify(f"{s}")
            return True
    return False


def compile_version_data():
    """
    Prepare and compile version infomration to send to the javascript files
    Parameters:
    return  :   list [[url, non-url, total], version types]
    """
    version_information = [] # the list for returning purpose
    identify_all_versions(api_endpoints)
    version_information.append(version_location_data)
    version_information.append(versions_count)
    return version_information


def reset_data():
    """
    Reset values of the global varaibles to the original states
    """
    global api_endpoints
    api_endpoints = []
    global version_location_data
    version_location_data = [0, 0, 0]
    global versions_count
    versions_count = {
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
    extract_version_location(api_endpoints)
    result = compile_version_data()
    # print(result)
    # print(api_endpoints)
    all_versions = list(itertools.chain(*api_versions))
    print(all_versions)
    print(len(all_versions))
    return result

def p():
    for i in api_versions:
        print(f"{i}")

##### Functions for printing information #####

execute("https://api.apis.guru/v2/list.json")

