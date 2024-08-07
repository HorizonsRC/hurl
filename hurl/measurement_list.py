from urllib.parse import urlencode, quote
from hurl.utils import get_hilltop_response
from xml.etree import ElementTree

def get_measurement_list_url(
    base_url,
    site=None,
    collection=None,
    units=None,
    target=None,
):
    params = {
        "Request": "MeasurementList",
        "Service": "Hilltop",
        "Site": site,
        "Collection": collection,
        "Units": units,
        "Target": target,
    }

    selected_params = {
        key: val for key, val in params.items() if val is not None
    }

    url = f"{base_url}?{urlencode(selected_params, quote_via=quote)}"
    return url


def get_measurement_list(
    base_url, site=None, collection=None, units=None, target=None, timeout=60
):
    if target is not None:
        raise ValueError("HtmlSelect (JSON) not supported.")
    
    url = get_measurement_list_url(base_url, site, collection, units)
    
    success, ret_obj = get_hilltop_response(url, timeout=timeout)

    root = ElementTree.fromstring(ret_obj.decode())
    measurement_list = []
    for child in root.findall("Measurement"):
        measurement_list += [child.get("Name")]
    
    return success, measurement_list, url
