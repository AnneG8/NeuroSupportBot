import logging

from environs import Env
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
from google.cloud.dialogflow_v2beta1.types import DetectIntentResponse


logger = logging.getLogger(__name__)


def create_api_key(project_id: str, suffix: str) -> Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"My first API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    logger.info(f"Successfully created an API key: {response.name}")
    return response


def detect_intent_text(project_id, session_id, text, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    logger.info(f'Session path: {session}\n')

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent_detection_confidence:
        logger.info('Successful response.')
    else:
        logger.info('Failed to recognize intent.')

    return response.query_result.fulfillment_text
