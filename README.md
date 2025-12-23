# roman-numerals-api

A small, deterministic Flask microservice that converts **Roman numerals ⇄ integers**.

This service exposes two GET endpoints with strict validation and canonical Roman numeral rules.  
It is designed to be simple, cacheable, and easy to deploy (Cloud Run–friendly).

---

## Features

- Roman → integer conversion
- Integer → Roman conversion
- Canonical Roman enforcement (rejects permissive forms like `IIII`)
- Case-insensitive Roman input (`mmxxv` is accepted)
- Deterministic responses (safe for HTTP caching)
- JSON responses using the `rest_response` helper from `flask-template`

---

## Endpoints

### Convert Roman numeral to integer

```
GET /roman_to_int/<roman>
```

Example:

```
GET /roman_to_int/MMXXV
```

Response:

```json
{
  "status": "OK",
  "result": {
    "input": "MMXXV",
    "normalized": "MMXXV",
    "value": 2025
  }
}
```

Lowercase input is accepted and normalized:

```
GET /roman_to_int/mmxxv
```

---

### Convert integer to Roman numeral

```
GET /int_to_roman/<value>
```

Example:

```
GET /int_to_roman/2025
```

Response:

```json
{
  "status": "OK",
  "result": {
    "input": 2025,
    "roman": "MMXXV"
  }
}
```

---

## Validation Rules

### Roman numerals

- Allowed characters: `I V X L C D M` (case-insensitive)
- Must be **canonical** (subtractive notation only)
- Examples of rejected input:
  - `IIII`
  - `VV`
  - `IL`
  - `XM`
- Valid numeric range after parsing: **1–3999**

### Integers

- Digits only (`0–9`)
- No signs, whitespace, or decimals
- Supported range: **1–3999**

---

## Error Handling

Invalid input returns HTTP 400 with a consistent JSON envelope:

```json
{
  "status": "ERROR",
  "result": "Roman numeral is not canonical (permissive forms like IIII are rejected)."
}
```

---

## Caching

Successful responses include:

```
Cache-Control: public, max-age=86400
```

Because the service is deterministic, identical requests always produce identical responses and are safe to cache by clients or intermediaries.

---

## Local Development

```
python app.py
```

The service listens on port **8080** by default.

Health check:

```
GET /health
```

---

## Deployment

This project is compatible with the `flask-template` base and works out of the box on:

- Google Cloud Run
- Any container-based platform
- Local Docker or VM deployments
