"""
constants.py
This module contains constant values used throughout the SDK for making requests
to the associated API and other related operations.
"""
import os

# The header name used to send the authentication token with API requests.
INFUZU_AUTH_TOKEN_HEADER_NAME: str = os.environ.get('INFUZU_AUTH_TOKEN_HEADER_NAME', "I-Auth-Token")

# Default timeout for API requests in seconds.
DEFAULT_REQUEST_TIMEOUT: int = os.environ.get('DEFAULT_REQUEST_TIMEOUT', 30)

# Base URL for the Clockwise service hosted by Infuzu.
CLOCKWISE_BASE_URL: str = os.environ.get("CLOCKWISE_BASE_URL", "https://clockwise.infuzu.com/")

# Endpoint to retrieve assignments from the Clockwise service.
CLOCKWISE_RETRIEVE_ASSIGNMENT_ENDPOINT: str = os.environ.get('CLOCKWISE_RETRIEVE_ASSIGNMENT_ENDPOINT', "assignment/")

# Endpoint to mark an assignment as completed in the Clockwise service.
CLOCKWISE_ASSIGNMENT_COMPLETE_ENDPOINT: str = os.environ.get(
    'CLOCKWISE_ASSIGNMENT_COMPLETE_ENDPOINT', "task-completed/"
)
CLOCKWISE_CREATE_RULE_ENDPOINT: str = os.environ.get('CLOCKWISE_CREATE_RULE_ENDPOINT', "rule/create/")
CLOCKWISE_DELETE_RULE_ENDPOINT: str = os.environ.get('CLOCKWISE_DELETE_RULE_ENDPOINT', "rule/delete/<str:rule_id>/")
CLOCKWISE_RULE_LOGS_ENDPOINT: str = os.environ.get('CLOCKWISE_RULE_LOGS_ENDPOINT', "rule/logs/<str:rule_id>/")


INFUZU_KEYS_BASE_URL: str = os.environ.get("INFUZU_KEYS_BASE_URL", "https://keys.infuzu.com/")
INFUZU_KEYS_KEY_PAIR_ENDPOINT: str = os.environ.get("INFUZU_KEYS_KEY_PAIR_ENDPOINT", "api/key/<str:key_id>/")


COGITOBOT_BASE_URL: str = os.environ.get("COGITOBOT_BASE_URL", "https://cogitobot.infuzu.com/")
COGITOBOT_RETRIEVE_DOCUMENT_VERSION_ENDPOINT: str = os.environ.get(
    "COGITOBOT_RETRIEVE_DOCUMENT_VERSION_ENDPOINT",
    "internal/document-version/<str:document_version_id>/"
)


ACCESS_BASE_URL: str = os.environ.get("ACCESS_BASE_URL", "https://accounts.infuzu.com/")
ACCESS_RETRIEVE_OBJECT_ACCESS_PROFILE_ENDPOINT: str = os.environ.get(
    "ACCESS_RETRIEVE_OBJECT_ACCESS_PROFILE_ENDPOINT", 'access/object-access-profile/<str:user_id>/<str:object_type>/'
)
