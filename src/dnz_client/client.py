from apiclient import (
    APIClient, endpoint, HeaderAuthentication, JsonResponseHandler,
    NoAuthentication
)


SINGLE_VALUE_FIELDS = ["direction", "exclude_filters_from_facets",
                       "facets_page", "page", "per_page", "sort", "text"]
MULTI_VALUE_FIELDS = ["facets", "fields", "geo_bbox"]
DICT_FIELDS = ["_and", "_or", "_without"]
# DICT_MULTI_VALUE_FIELDS are those fields that may occur multiple
# times in an "and" or "without" filter.
DICT_MULTI_VALUE_FIELDS = [
    "category", "collection", "content_partner", "creator", "dc_type",
    "format", "placename", "primary_collection", "subject", "title", "usage"
]


@endpoint(base_url="http://api.digitalnz.org/v3")
class Endpoint:
    search = "records.json"
    metadata = "records/{record_id}.json"


class DNZClient(APIClient):

    def metadata(self, record_id, fields=None):
        url = Endpoint.metadata.format(record_id=record_id)
        params = self._generate_metadata_params(fields)
        return self.get(url, params=params)

    def search(self, **kwargs):
        params = self._generate_search_params(**kwargs)
        return self.get(Endpoint.search, params=params)

    def _format_dict_param(self, filter_type, values):
        # Does not handle combining OR filters across multiple fields,
        # eg: "(year is 2014 OR 2015) AND (primary_collection is
        # TAPUHI OR Public Address)", which requires nesting, eg:
        # "&and[or][year][]=2015&and[or][year][]=2014&and[and][or][primary_collection][]=TAPUHI&and[and][or][primary_collection][]=Public+Address"
        params = {}
        for k, v in values.items():
            if filter_type == "and[or]":
                multi = "[]"
            elif k in DICT_MULTI_VALUE_FIELDS:
                multi = "[]"
            else:
                multi = ""
            name = "{}[{}]{}".format(filter_type, k, multi)
            params[name] = v
        return params

    def _format_multivalue_param(self, values):
        return ",".join(values) or None

    def _generate_metadata_params(self, fields):
        params = {}
        if fields is not None:
            params["fields"] = self._format_multivalue_param(fields)
        return params

    def _generate_search_params(self, **kwargs):
        params = {}
        for k, v in kwargs.items():
            if k in SINGLE_VALUE_FIELDS:
                params[k] = v
            elif k in MULTI_VALUE_FIELDS:
                params[k] = self._format_multivalue_param(v)
            elif k in DICT_FIELDS:
                field_name = self._get_field_name(k)
                params.update(self._format_dict_param(field_name, v))
        return params

    def _get_field_name(self, k):
        if k == "_and":
            name = "and"
        elif k == "_or":
            name = "and[or]"
        elif k == "_without":
            name = "without"
        return name


def get_client(api_token=None, **kwargs):
    if api_token is None:
        auth_method = NoAuthentication()
    else:
        auth_method = HeaderAuthentication(
            parameter="Authentication-Token",
            scheme=None,
            token=api_token,
        )
    return DNZClient(
        authentication_method=auth_method,
        response_handler=JsonResponseHandler,
        **kwargs
    )
