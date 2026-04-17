import json
import uuid
from urllib import error, request

BASE_URL = "https://healthcare-backend-v712.onrender.com"


def call_api(method, path, payload=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    req = request.Request(url, data=body, headers=headers, method=method)

    try:
        with request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
            data = json.loads(text) if text else None
            return resp.status, data
    except error.HTTPError as exc:
        text = exc.read().decode("utf-8")
        data = None
        if text:
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                data = text
        return exc.code, data


def expect(status, expected, name, body=None):
    if status != expected:
        raise AssertionError(
            f"{name} failed: expected {expected}, got {status}. response={body}"
        )


def main():
    suffix = uuid.uuid4().hex[:8]

    user1 = {
        "name": "Live User One",
        "email": f"live.one.{suffix}@example.com",
        "password": "StrongPass123!",
    }
    user2 = {
        "name": "Live User Two",
        "email": f"live.two.{suffix}@example.com",
        "password": "StrongPass456!",
    }

    checks = []

    status, body = call_api("GET", "/api/patients/")
    expect(status, 401, "patients_without_token", body)
    checks.append("PASS patients_without_token")

    status, body = call_api("POST", "/api/auth/register/", user1)
    expect(status, 201, "register_user1", body)
    checks.append("PASS register_user1")

    status, _ = call_api("POST", "/api/auth/register/", user1)
    expect(status, 400, "register_duplicate", body)
    checks.append("PASS register_duplicate")

    status, body = call_api("POST", "/api/auth/login/", {"email": user1["email"], "password": user1["password"]})
    expect(status, 200, "login_user1", body)
    token1 = body["access"]
    checks.append("PASS login_user1")

    status, body = call_api("POST", "/api/doctors/", {
        "full_name": "Dr Live",
        "specialization": "Cardiology",
        "email": f"dr.live.{suffix}@example.com",
        "contact_number": "9999999999",
        "years_of_experience": 10,
    }, token1)
    expect(status, 201, "create_doctor_user1", body)
    doctor_id = body["id"]
    checks.append("PASS create_doctor_user1")

    status, body = call_api("POST", "/api/patients/", {
        "full_name": "Patient Live",
        "age": 30,
        "gender": "male",
        "contact_number": "8888888888",
        "address": "NY",
        "medical_history": "None",
    }, token1)
    expect(status, 201, "create_patient_user1", body)
    patient_id = body["id"]
    checks.append("PASS create_patient_user1")

    status, body = call_api("POST", "/api/mappings/", {"patient": patient_id, "doctor": doctor_id}, token1)
    expect(status, 201, "create_mapping_user1", body)
    mapping_id = body["id"]
    checks.append("PASS create_mapping_user1")

    status, _ = call_api("POST", "/api/mappings/", {"patient": patient_id, "doctor": doctor_id}, token1)
    expect(status, 400, "duplicate_mapping_rejected", _)
    checks.append("PASS duplicate_mapping_rejected")

    status, _ = call_api("POST", "/api/auth/register/", user2)
    expect(status, 201, "register_user2", _)
    checks.append("PASS register_user2")

    status, body = call_api("POST", "/api/auth/login/", {"email": user2["email"], "password": user2["password"]})
    expect(status, 200, "login_user2", body)
    token2 = body["access"]
    checks.append("PASS login_user2")

    status, _ = call_api("GET", f"/api/patients/{patient_id}/", token=token2)
    expect(status, 404, "patient_owner_protected", _)
    checks.append("PASS patient_owner_protected")

    status, body = call_api("GET", "/api/doctors/", token=token2)
    expect(status, 200, "doctor_list_user2", body)
    checks.append("PASS doctor_list_user2")

    status, body = call_api("GET", "/api/mappings/", token=token2)
    expect(status, 200, "mapping_list_user2", body)
    if any(item["id"] == mapping_id for item in body):
        raise AssertionError("mapping_visibility_user2 failed: user2 can see user1 mapping")
    checks.append("PASS mapping_visibility_user2")

    status, _ = call_api("GET", f"/api/mappings/{patient_id}/", token=token2)
    expect(status, 404, "mapping_patient_owner_protected", _)
    checks.append("PASS mapping_patient_owner_protected")

    status, _ = call_api("GET", "/api/doctors/", token="bad.token.value")
    expect(status, 401, "invalid_token_rejected", _)
    checks.append("PASS invalid_token_rejected")

    print("Live API checks completed")
    for item in checks:
        print(item)
    print(f"Total passed: {len(checks)}")


if __name__ == "__main__":
    main()
