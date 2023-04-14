DigitalNZ API Python client
===========================

This library provides a Python client to interact with the DigitalNZ
API version 3. It supports searching records and getting metadata for
a specific record, returning all results as Python dictionaries loaded
from the returned JSON.


Usage
-----

::

   from dnz_client import get_client
   client = get_client("my API token")  # Omit token for anonymous use
   _and = {"collection": "Music 101", "subject": "Cats", "Weddings"}
   _or = {"category": ["Books", "Articles"]}
   results = client.search(
       text="Wanganui OR Whanganui", _and=_and, _or=_or,
       geo_bbox=["-41", "174", "-42", "175"], "direction": "asc")
   metadata = client.metadata(record_id=6330666, fields=["id", "title"])


The keyword arguments passed to the *search* method are those
specified in the `API documentation`_.

The arguments *_and*, *_or*, and *_without* contain dictionaries keyed
to the fields that are so joined; each value may be a string or list
of strings.

The keyword arguments *facets*, *fields*, and *geo_bbox* each take a
list of strings.

The other fields (*direction*, *exclude_filters_from_facets*,
*facets_page*, *page*, *per_page*, *sort*, and *text*) are either
string or integer values, as appropriate.

The return values of both *search()* and *metadata()* are dictionaries
loaded from the JSON returned by DigitalNZ.


Limitations
-----------

OR filters combined across multiple fields are not supported. For
example, it is supported to search for records where the *category* is
either "Audio" or "Videos", but searching for those records where the
*category* is either "Audio" or "Videos" **and** the *year* is either
"2014" or "2015" is not.

The client does no checking that supplied values are sensible or
permitted by the DigitalNZ API. For example, any string may be passed
as the *direction* field, though the API permits only "asc" and
"desc".


Exceptions
----------

See the underlying `api-client documentation`_ for the exceptions the
client raises.


.. _API documentation: https://app.swaggerhub.com/apis-docs/DigitalNZ/Records/3
.. _api-client documentation: https://github.com/MikeWooster/api-client#Exceptions
