from dataclasses import dataclass
from requests import Response
from .. import constants
from ..http_requests import signed_requests
from ..utils.caching import CacheSystem


USER_ACCESS_PROFILE_CACHE: CacheSystem = CacheSystem(default_expiry_time=60)


@dataclass
class UserAccessProfile:
    user_id: str
    billing_in_good_standing: bool
    active_subscriptions: list[str]

    @classmethod
    def retrieve(cls, user_id: str, object_type: str) -> 'ObjectAccessProfile':
        def get_user_access_profile() -> 'UserAccessProfile':
            api_response: Response = signed_requests.request(
                method="GET",
                url=f"{constants.ACCESS_BASE_URL}"
                    f"{constants.ACCESS_RETRIEVE_USER_ACCESS_PROFILE_ENDPOINT}".replace('<str:user_id>', user_id)
            )
            if api_response.status_code == 200:
                return cls(**api_response.json())
            raise Exception(f"Error retrieving object access profile: {api_response.text}")
        return USER_ACCESS_PROFILE_CACHE.get(
            cache_key_name=f'{user_id}__{object_type}', specialized_fetch_function=get_user_access_profile
        )
