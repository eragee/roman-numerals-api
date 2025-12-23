from flask import Flask, make_response

from helpers import rest_error, rest_response
from roman import (
    int_to_roman,
    is_valid_int_charset,
    is_valid_roman_charset,
    roman_to_int_strict,
)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

_CACHE_CONTROL = "public, max-age=86400"


def _cache_ok(resp):
    resp.headers["Cache-Control"] = _CACHE_CONTROL
    return resp


@app.route("/health", methods=["GET"])
def health():
    resp = make_response(rest_response("OK"))
    return _cache_ok(resp)


@app.route("/roman_to_int/<roman>", methods=["GET"])
def roman_to_int(roman: str):
    if not is_valid_roman_charset(roman):
        return rest_error("Invalid Roman input: allowed characters are IVXLCDM only (case-insensitive).")

    try:
        value = roman_to_int_strict(roman)
    except ValueError as e:
        return rest_error(str(e))

    payload = {
        "input": roman,
        "normalized": roman.upper(),
        "value": value,
    }
    resp = make_response(rest_response(payload))
    return _cache_ok(resp)


@app.route("/int_to_roman/<value>", methods=["GET"])
def int_to_roman_route(value: str):
    if not is_valid_int_charset(value):
        return rest_error("Invalid integer input: digits only (0-9).")

    n = int(value, 10)
    try:
        roman = int_to_roman(n)
    except ValueError as e:
        return rest_error(str(e))

    payload = {
        "input": n,
        "roman": roman,
    }
    resp = make_response(rest_response(payload))
    return _cache_ok(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
