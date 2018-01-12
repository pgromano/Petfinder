"""
@author: pgromano

This majority of this code is based off of the repo
github.com/gtaylor/petfinder-api/. For any issues with the API, please look at
the Petfinder developer site (http://www.petfinder.com/developers).
"""

from . import parser
from lxml import etree
import requests


__all__ = ['PetfinderClient']


API_URL = "http://api.petfinder.com/"
PET_FIND_URL = API_URL + "pet.find"
PET_GET_URL = API_URL + "pet.get"
PET_GETRANDOM_URL = API_URL + "pet.getRandom"
BREED_LIST_URL = API_URL + "breed.list"


class PetfinderClient(object):
    """ Petfinder Client for Web API

    In order to pull details from the API key (1) you must set up a developer
    tokens which are necessary to instantiate this client with credentials.
    Full documentation can be found from the petfinder API (2).

    Arguments
    ---------
    api_key : str
        API developer key
    api_secret : str
        API developer secret
    api_auth_token : str, optional
        API auth token. Currently not implemented in the Petfinder API, but
        introduced here for future incorporation.
    animal : str, {'barnyard', 'bird', 'cat', 'dog', 'horse', 'reptile', 'smallfurry'}
        Type of animal.
    age : str, {'Baby', 'Young', 'Adult', 'Senior'}
        Age of animal.
    breed : str
        Breed of animal. The function `breeds` returns a complete list of
        available breeds.
    location : str
        The zip/postal code or city and state where the search should begin.
    max_results : int
        The maximum number of results to return per call.
    sex : str, {'F', 'M'}
        Sex of animal.
    size : str, {'S', 'M', 'L', 'XL'}
        Size of animal.

    References
    ----------
        [1]: http://www.petfinder.com/developers/api-key
        [2]: http://www.petfinder.com/developers/api-docs
    """

    def __init__(self, api_key, api_secret, api_auth_token=None,
                 animal=None, age=None, breed=None, location=None,
                 max_results=10, sex=None, size=None, offset=None):

        # Set API key and secret
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_auth_token = None

        # Set animal property
        self.animal = animal
        self.age = age
        self.breed = breed
        self.location = location
        self.max_results = max_results
        self.sex = sex
        self.size = size

        if offset is None:
            offset = 0
        self._offset = offset

        if not isinstance(location, (str, None.__class__)):
            self.location = str(location)

    @property
    def all_breeds(self):
        """ Returns a list of breeds for a particular animal

        Returns
        -------
        breeds : list
            List of breeds
        """
 
        if hasattr(self, '_breeds'):
            return self._breeds
        self._all_breeds = self._get_all_breeds()
        return self._all_breeds

    def find(self, return_type='full'):
        """ Find pets near """

        # Define query parameters
        query = {"key": self.api_key,
                 "format": "xml",
                 "animal": self.animal,
                 "age": self.age,
                 "breed": self.breed,
                 "count": self.max_results,
                 "location": self.location,
                 "offset": self._offset,
                 "output": return_type,
                 "size": self.size,
                 "sex": self.sex}

        # Query from API
        response = requests.get(PET_FIND_URL, params=query)
        self._offset += self.max_results

        # Parse XML
        results = etree.fromstring(response.content)
        return parser.pet_records(results, return_type)

    def get(self, pet_id=None, return_type='full'):
        """ Get record of individual pet

        Arguments
        ---------
        pet_id : str, optional
            The ID key for a specific pet. It None, then the `pet.getRandom`
            method is used, and a random pet is returned with initialized
            filter.
        return_type : int, {'id', 'basic', 'full'}
            The type of data to return. If 'id' only the pet_id is returned,
            'basic' and 'full' give a complete record, but the client method
            returns identical attributes.

        Returns
        -------
        record : dict
            A record of the queried pet.
        """
        
        # If no pet_id given, then randomly select pet
        if pet_id is None:
            # Define query parameters
            query = {"key": self.api_key,
                     "format": "xml",
                     "animal": self.animal,
                     "breed": self.breed,
                     "size": self.size,
                     "sex": self.sex,
                     "location": self.location,
                     "output": return_type}

            # Query from API
            response = requests.get(PET_GETRANDOM_URL, params=query)

        # If pet_id given, get records from database
        else:
            # Define query parameters
            query = {"key": self.api_key,
                     "id": pet_id,
                     "format": "json"}

            # Query from API
            response = requests.get(PET_GET_URL, params=query)

        # Parse XML
        results = etree.fromstring(response.content)
        return parser.pet_record(results, return_type)

    def update(self, **kwargs):
        for key in kwargs.keys():
            if kwargs[key] is not None:
                if key == "offset":
                    setattr(self, "_"+key, kwargs[key])
                else:
                    setattr(self, key, kwargs[key])

    def _get_all_breeds(self):
        """ Helper function to get all breeds """

        if self.animal is None:
            raise ValueError("Animal type must be set!")

        # Define query parameters
        query = {"key": self.api_key,
                 "format": "xml",
                 "animal": self.animal}

        # Query from API
        response = requests.get(BREED_LIST_URL, params=query)

        # Parse XML
        results = etree.fromstring(response.content)
        return parser.pet_breeds(results)
