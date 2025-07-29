from app.tdn.api.character_api import TdnCharacterApi


def character(character_id) -> TdnCharacterApi:
    from app.tdn import get_session
    return TdnCharacterApi(get_session(), character_id)