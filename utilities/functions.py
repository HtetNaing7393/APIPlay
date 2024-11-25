import requests
import re
import json
import aiohttp
import asyncio


# lists of versioning group
versions = {
    "sem_ver_3": [],
    "sem_ver_2": [],
    "v_star": [],
    "integer": [],
    "date_yyyy_mm_dd": [],
    "others": []
}

versions_count = {
    "total": 0,
    "sem_ver_3": 0,
    "sem_ver_2": 0,
    "v_star": 0,
    "integer": 0,
    "date_yyyy_mm_dd": 0,
    "others": 0
}

# return the number of versions in the file


##################################################################################################
##################################### This is the serious code ###################################
##################################################################################################


# lock to ensure data integrity when accessisng the shared data
lock = asyncio.Lock()
# list to house api endpoints
api_endpoints = []

version_info = []

version_data = [0, 0, 0]

versions_count = {
    "total": 0,
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
    "v_star": r"v\d+$",
    "integer2": r"^(d\{3}|\d{2}|\d{1})+$",
    "integer": r"^\d+$",
    "date_yyyy_mm_dd": r"^(?:\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2})$"
}


def identify_all_versions():
    for version in version_info:
        identify(version)


def identify(version):
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
    count = 100000000

    # access the json object to locate "versions" header and the "swaggerURL" header
    for key, value in item.items():
        if count > 0:
            try:
                sub = value["versions"]  # a list of versions
                version_info.append(value["preferred"])
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
    return links_list


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
            url = data["host"]
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
            # combing the base URL and the endpoint path
            full_url = f"{url}{l}"
            api_endpoints.append(full_url)
    except:
        pass
    finally:
        pass


def extract_version_location():
    """
    Extract version location in each URLs
    """

    for l in api_endpoints:
        if locate_version(l):
            version_data[0] += 1
        else:
            version_data[1] += 1
        version_data[2] += 1


def locate_version(link):
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
            return True
    return False


def compile_version_data():
    version_information = []
    # identify_all_versions()
    version_information.append(version_data)
    version_information.append(len(version_info))
    # version_information.append(versions_count)
    return version_information


def reset_data():
    global api_endpoints
    api_endpoints = []
    global version_info
    version_info = []
    global version_data
    version_data = [0, 0, 0]
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
    print("sanity check")


def execute(url):
    reset_data()
    links = get_links(url)
    asyncio.run(get_all_data(links))
    extract_version_location()
    result = compile_version_data()
    return result


##### Functions for printing information #####

def print_links():
    """
    Print all the gathered api_endpoints
    """

    for l in api_endpoints:
        print(l)
    print(f"Length of the list is: {len(api_endpoints)}")


def print_version_info():
    total = version_info[0] + version_info[1]
    true = (version_info[0]/total) * 100
    false = (version_info[1]/total) * 100
    print(f"True:{true:.2f}% :   False:{false:.2f}%")


def display_success():
    return "Success,,,,F Yeah!!!"
