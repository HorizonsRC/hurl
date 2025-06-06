from urllib.parse import quote, urlencode


def get_ensemble_stats_url(
    base_url,
    site=None,
    measurement=None,
    statistic=None,
    collection=None,
):
    params = {
        "Request": "EnsembleStats",
        "Service": "Hilltop",
        "Site": site,
        "Measurement": measurement,
        "Statistic": statistic,
        "Collection": collection,
    }

    selected_params = {
        key: val for key, val in params.items() if val is not None
    }

    url = f"{base_url}?{urlencode(selected_params, quote_via=quote)}"
    return url
