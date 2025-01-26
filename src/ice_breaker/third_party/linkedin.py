import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(profile_url: str | None = None, mock: bool = True):
    """scrape information from linkedin profiles,
    Manually scrape the information from the linkedin profile"""

    if mock:
        r = requests.get("http://localhost:8000/content.json")
        r.raise_for_status()
        data = r.json()


    else:
        if not profile_url:
            raise ValueError("Must provide a linkedin profile url")
        api_key = os.environ.get("PROXYCURL_API_KEY")
        assert api_key is not None

        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url': profile_url,
            'extra': 'include',
        }
        r = requests.get(api_endpoint,
                                params=params,
                                headers=headers)
        data = r.json()

    data = {k: v
            for k, v in data.items()
            if v not in ([], "", None)
            and k not in ["similarly_named_profiles", "people_also_viewed", "certifications", "logo_url"]
            }
    #if data.get("groups"):
    #    for group_dict in data.get("groups"):
    #        group_dict.pop("profile_pic_url")

    return data
