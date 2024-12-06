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
api_base_urls = []
# list to house api versions
api_versions = []

# the number of version typess
endpoint_versions_count = {
    "sem_ver_3": 0,
    "sem_ver_2": 0,
    "v_star": 0,
    "integer": 0,
    "date_yyyy_mm_dd": 0,
    "others": 0,
    "url": 0,
    "non-url": 0,
    "total": 0,
}

api_versions_count = {
    "sem_ver_3": 0,
    "sem_ver_2": 0,
    "v_star": 0,
    "integer": 0,
    "date_yyyy_mm_dd": 0,
    "others": 0,
    "url": 0,
    "non-url": 0,
    "total": 0,
}

overall_info = {
    "apis": 0,
    "specifications": 0,
    "endpoints": 0
}

# version identifiers regex queries
identifiers = {
    "sem_ver_3": r"^(v|)\d+\.\d+\.\d+$",
    "sem_ver_2": r"^(v|)\d+\.\d+$",
    "v_star":  r"v\d+(\.\d+)*(\([a-zA-Z]+\))?",
    "integer2": r"^(d\{3}|\d{2}|\d{1})+$",
    "integer": r"^\d+$",
    "date_yyyy_mm_dd": r"^(?:\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2})$"
}

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
    # get the total number of APIs in the dataset
    overall_info["apis"] = len(item)
    # access the json object to locate "versions" header and the "swaggerURL" header
    for key, value in item.items():
        try:
            sub = value["versions"]  # a list of versions
            # get the versions and add the versions to api_versions
            api_versions.append(versions)
            for k, v in sub.items():
                overall_info["specifications"] += 1
                try:
                    links_list.append(v["swaggerUrl"])
                except:
                    pass
                finally:
                    pass
        except:
            pass
        finally:
            pass

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
        api_base_urls.append(f"{url}")
    except:
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
    overall_info["endpoints"] = len(api_endpoints)


def extract_version_location(urls, versions_count):
    """
    Extract version location in each URLs
    """
    for l in urls:
        if locate_and_identify_version(l, versions_count):
            versions_count["url"] += 1
        else:
            versions_count["non-url"] += 1
        versions_count["total"] += 1


def find_version_location(key, versions_count):
    """
    Function to locate the version identifier in the URL
    """
    if key in versions_count:
        versions_count[key] += 1
    else:
        versions_count[key] = 1


def locate_and_identify_version(link, versions_count):
    """
    Split a given url into multiple segments and check if the version is in the URL
    If the version is in the URL, identify it's type
    Parameters:
    link    :   swaggerURL
    return  :   True if the version information exists in the URL, False if not
    """

    # split the url by "/" to look for version information
    sub_strings = link.split("/")
    # location = 1
    for s in sub_strings:
        if look_for_version(s):
            identify(f"{s}", versions_count)
            return True
        else:
            sub_s = s.split(".")
            for s_ in sub_s:
                if look_for_version(s_):
                    identify(f"{s}", versions_count)
                    return True
        # location += 1
    return False


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
    elif re.match(identifiers["integer2"], version):
        versions_count["integer"] += 1
    elif re.match(identifiers["sem_ver_3"], version):
        versions_count["sem_ver_3"] += 1
    elif re.match(identifiers["sem_ver_2"], version):
        versions_count["sem_ver_2"] += 1
    else:
        versions_count["others"] += 1


def look_for_version(checked_string):
    """
    Check if a versioning format exists in the given input string
    Parameters: 
    checked_string  :   the input string to checked
    return          :   True if a versioning format exists in the string, False if not
    """
    conditions = [re.search(identifiers["sem_ver_3"], checked_string),
                  re.search(identifiers["sem_ver_2"], checked_string),
                  re.search(identifiers["v_star"], checked_string),
                  re.search(identifiers["integer2"], checked_string),
                #   re.search(identifiers["integer"], checked_string),
                  re.search(identifiers["date_yyyy_mm_dd"], checked_string)]
    return any(conditions)


def compile_version_data():
    """
    Prepare and compile version infomration to send to the javascript files
    Parameters:
    return  :   list [overall info, api versions info, endpoint versions info]
    """
    version_information = []  # the list for returning purpose
    version_information.append(overall_info)
    version_information.append(api_versions_count)
    version_information.append(endpoint_versions_count)
    return version_information


def reset_data():
    """
    Reset values of the global varaibles to the original states
    """
    global api_base_urls
    api_base_urls = []
    global api_endpoints
    api_endpoints = []
    global api_versions_count
    api_versions_count = {
        "sem_ver_3": 0,
        "sem_ver_2": 0,
        "v_star": 0,
        "integer": 0,
        "date_yyyy_mm_dd": 0,
        "others": 0,
        "url": 0,
        "non-url": 0,
        "total": 0
    }
    global endpoint_versions_count
    endpoint_versions_count = {
        "sem_ver_3": 0,
        "sem_ver_2": 0,
        "v_star": 0,
        "integer": 0,
        "date_yyyy_mm_dd": 0,
        "others": 0,
        "url": 0,
        "non-url": 0,
        "total": 0
    }
    global overall_info
    overall_info = {
        "apis": 0,
        "specifications": 0,
        "endpoints": 0
    }


def execute(url):
    reset_data()
    links = get_links(url)
    asyncio.run(get_all_data(links))
    extract_version_location(api_endpoints, endpoint_versions_count)
    extract_version_location(api_base_urls, api_versions_count)
    result = compile_version_data()  # prepare data to send to the JS file
    return result

# execute the script
# execute("https://api.apis.guru/v2/list.json")


############################## Functions for printing information and testing #########################
