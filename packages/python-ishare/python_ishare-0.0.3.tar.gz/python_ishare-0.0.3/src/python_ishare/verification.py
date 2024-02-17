import re
from typing import Any, Literal

import jwt
from jwt import ExpiredSignatureError, ImmatureSignatureError, InvalidAudienceError

from python_ishare import exceptions as ishare_exc
from python_ishare.authentication import decode_jwt, x5c_b64_to_certificate

ASSERTION_TYPE = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"


def is_valid_eori_number(eori_number: str, strict_eori: bool) -> bool:
    """
    Returns true if the eori number is valid for use within iSHARE.

    The 'strict_eori' can be set to False if your connecting satellite is not enforcing
    valid eori numbers.

    :param eori_number:
    :param strict_eori: Whether to check eori number format.
    :return:
    """
    if eori_number is None or eori_number == "":
        return False

    if not strict_eori:  # Prevent eori number validation.
        return True

    pattern = r"EU.EORI.[A-Z]{2}[0-9]{1,15}"
    matches = re.fullmatch(pattern, eori_number)
    return matches is not None


def validate_client_assertion(
    client_id: str,
    client_assertion: str,
    audience: str,
    grant_type: Literal["client_credentials"],
    scope: Literal["iSHARE"],
    client_assertion_type: Literal[
        "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
    ],
    strict_eori: bool = False,
) -> dict[str, Any]:
    """
    https://dev.ishare.eu/m2m/authentication.html

    :param client_id: iSHARE identifier of the Service Consumer.
    :param client_assertion: the json web token as per iSHARE specification.
    :param audience: the iSHARE identifier of the target service.
    :param grant_type:
    :param scope:
    :param client_assertion_type:
    :param strict_eori: Whether to validate eori numbers per specification.
    :raises iSHAREAuthenticationException: and all it's inheriting classes
    :return: The decrypted payload
    """
    if grant_type != "client_credentials":
        raise ishare_exc.ISHAREInvalidGrantType()

    if scope != "iSHARE":
        raise ishare_exc.ISHAREInvalidScope()

    if client_assertion_type != ASSERTION_TYPE:
        raise ishare_exc.ISHAREInvalidClientAssertionType()

    headers = jwt.get_unverified_header(client_assertion)

    if headers["alg"] != "RS256":
        raise ishare_exc.ISHAREInvalidTokenAlgorithm()

    if headers["typ"] != "JWT":
        raise ishare_exc.ISHAREInvalidTokenType()

    if headers["x5c"] is None or len(headers["x5c"]) < 1:
        raise ishare_exc.ISHAREInvalidCertificate()

    try:
        jwt_payload: dict[str, Any] = decode_jwt(
            json_web_token=client_assertion,
            public_x509_cert=list(x5c_b64_to_certificate(headers["x5c"])),
            audience=audience,
        )
    except ExpiredSignatureError:
        raise ishare_exc.ISHARETokenExpired()
    except ImmatureSignatureError:
        raise ishare_exc.ISHARETokenNotValidYet()
    except InvalidAudienceError:
        raise ishare_exc.ISHAREInvalidAudience()

    if not is_valid_eori_number(eori_number=client_id, strict_eori=strict_eori):
        raise ishare_exc.ISHAREInvalidClientId()

    if client_id != jwt_payload.get("sub") or client_id != jwt_payload.get("iss"):
        raise ishare_exc.ISHAREInvalidTokenIssuerOrSubscriber()

    if not jwt_payload.get("jti"):
        raise ishare_exc.ISHAREInvalidTokenJTI()

    expires: int = jwt_payload.get("exp", 0)
    issued: int = jwt_payload.get("iat", 0)

    if expires - issued != 30:
        raise ishare_exc.ISHARETokenExpirationInvalid()

    return jwt_payload
