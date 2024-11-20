import requests
import re
import json
import aiohttp
import asyncio

# the function that links between app and functions


def process(data):
    identify_version(data["url"], data["info"])
    return get_api_info(data["url"], data["api_header"], data["api_key"])


# function to identiy versioning format
def identify_version(url, info):
    pattern = r'/v(\d+(\.\d)*)/'
    match = re.search(pattern, url)

    if match:  # version in the URL but not in the domain name
        version = match.group()[1:-1]

        info["version"] = version

        info["domain"] = "url"

        info["identifier"] = identify_format(version)
    else:  # version in the URL and in the domain name
        pattern_2 = r'v(\d+(\.\d)*)'
        match = re.search(pattern_2, url)
        version = match.group()
        if match:
            info["version"] = version

            info["domain"] = "url"

            info["identifier"] = identify_format(version)
        else:
            pass
        # some other versiong format and methods


# function to identify versioning format
def identify_format(version):
    sem_ver = r"^v\d+\.\d+\.\d+$"
    v_star = r"^v\d+"
    date = r"^\d{2}-\d{2}-\d{4}$"

    if re.search(sem_ver, version):
        return "SemVer"

    if re.search(v_star, version):
        return "v*"

    if re.search(date, version):
        return "date"

    return "something else"


# retrive api info and proccess it inot json
def get_api_info(url, header, key):
    url = f"{url}"
    headers = {header: key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        api_header = format_json(response.headers)
        # api_body = response.text
        # api_body = format_json(api_body)
        return api_header
    else:
        print(f"Failed to retrive data {response.status_code}")
        return

# function to formate a json object


def format_json(data):
    map = []
    for k, v in data.items():
        map.append({"header": k, "value": v})
    return map


####### __________________This is the functional code__________##############
# version identifiers regex queries
# identifiers = {
#     "sem_ver_3": r"^(v|)\d+\.\d+\.\d+$",
#     "sem_ver_2": r"^(v|)\d+\.\d+$",
#     "v_star": r"v\d+$",
#     "integer2": r"^(d\{3}|\d{2}|\d{1})+$",
#     "integer": r"^\d+$",
#     "date_yyyy_mm_dd": r"^(?:\d{4}-\d{2}-\d{2}|\d{4}\.\d{2}\.\d{2})$"
# }

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


def versions_numbers():
    return versions_count

# retrive api info and proccess it into json


def get_info(url):
    url = f"{url}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # version_list = locate_header(data)
        # identify_version(version_list)
        # versions_count["total"] = versions_count["sem_ver_3"] + versions_count["sem_ver_2"] + versions_count["v_star"] + versions_count["integer"] + versions_count["date_yyyy_mm_dd"] + versions_count["others"]
        # print(versions_count["total"])
        # print_results()
        links = get_links(data)
        print(len(links))
        # for l in links:
        #     print(l)

        api_header = ""
        return api_header
    else:
        print(f"Failed to retrive data {response.status_code}")
        return


def locate_version(item):
    version_list = []
    for key, value in item.items():
        sub = value["versions"]
        for k, v in sub.items():
            version_list.append(v["info"]["version"])
    # print(f"Number of APIs: {len(api)},  number of specifications: {count}")
    return version_list


# def identify_version(version_list):
#     for version in version_list:
#         identify(version)


# def identify(version):
#     if re.match(identifiers["date_yyyy_mm_dd"], version):
#         versions["date_yyyy_mm_dd"].append(version)
#         versions_count["date_yyyy_mm_dd"] += 1
#     elif re.match(identifiers["v_star"], version):
#         versions["v_star"].append(version)
#         versions_count["v_star"] += 1
#     elif re.match(identifiers["integer"], version):
#         versions["integer"].append(version)
#         versions_count["integer"] += 1
#     elif re.match(identifiers["sem_ver_3"], version):
#         versions["sem_ver_3"].append(version)
#         versions_count["sem_ver_3"] += 1
#     elif re.match(identifiers["sem_ver_2"], version):
#         versions["sem_ver_2"].append(version)
#         versions_count["sem_ver_2"] += 1
#     else:
#         versions["others"].append(version)
#         versions_count["others"] += 1

# For printing out results


def print_results():
    # print_list(versions["others"])
    print(f"Semver3: {versions['sem_ver_3']}")
    # print(f"Semver2: {len(versions['sem_ver_2'])}")
    # print(f"V_star: {len(versions['v_star'])}")
    # print(f"Integer: {len(versions['integer'])}")
    # print(f"Date: {len(versions['date_yyyy_mm_dd'])}")
    print(f"Others: {len(versions['others'])}")
    print(f'Total version numbers: {len(versions["sem_ver_3"]) + len(versions["sem_ver_2"]) + len(versions["v_star"])
          + len(versions["integer"]) + len(versions["date_yyyy_mm_dd"]) + len(versions["others"])}')


def print_list(list):
    for l in list:
        print(l)

##################################################################################################
##################################### This is the serious code ###################################
##################################################################################################


# lock to ensure data integrity when accessisng the shared data
lock = asyncio.Lock()
# list to house api endpoints
api_endpoints = []

version_info = [0, 0, 0]

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
    count = 1000000

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
            retrive_data(data, link)

defects = []


def retrive_data(data, link):
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
            version_info[0] += 1
        else:
            version_info[1] += 1
        version_info[2] += 1


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


def execute(url):
    links = get_links(url)
    asyncio.run(get_all_data(links))
    extract_version_location()
    return version_info


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

# def test_data(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         keys = data.keys()
#         for k in keys:
#             if k == "adyen.com:BalancePlatformService":
#                 sub = data["adyen.com:BalancePlatformService"]
#                 sub1 = sub["versions"]
#                 data = sub1.keys()
#                 print(data)
#                 break

# for k, v in data.items():
#     if k == "adyen.com:BalancePlatformService":
#         key = v["versions"]
#         data = key.keys()
#         print(data)
#     else:
#         print("didn't match")
#     break
# for i in key:
#     print(i)


# test_data("https://api.apis.guru/v2/list.json")

# links = ["https://api.apis.guru/v2/cache/logo/",
#          "https://api.apis.guru/v2/cache/logo/",
#          "https://api.apis.guru/cache/logo/2024-09-22",
#          "https://api.apis.guru/2.3.4/cache/logo/",
#          "https://api.v2.apis.guru/cache/logo/",
#          "https://api.apis.guru/v2.3/cache/logo/",
#          "https://api.apis.guru/cache/v1/logo/",
#          "https://api.apis.guru/cache/logo/"]
# links = ["https://api.apis.guru/v2/cache/logo/"]


# def run():
#     extract_version(links)
#     for v in version_info:
#         print(v)
# run()

# extract_version(links)


# identify_version()
# Test run the code
# get_info("https://api.apis.guru/v2/list.json")  # test run the code
# get_endpoints("https://api.apis.guru/v2/specs/1password.com/events/1.0.0/openapi.json")
