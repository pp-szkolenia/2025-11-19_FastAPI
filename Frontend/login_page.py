import base64
import json
import streamlit as st
import requests


def _decode_claims(jwt: str) -> dict:
    try:
        payload_b64 = jwt.split(".")[1]
        padding = "=" * (-len(payload_b64) % 4)
        payload = base64.urlsafe_b64decode(payload_b64 + padding).decode("utf-8")
        return json.loads(payload)
    except Exception:
        return {}


def login_page(api_base: str):
    st.header("Login")

    if st.session_state.get("jwt"):
        st.success("You are already logged in.")
        return

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if not submitted:
        return

    try:
        resp = requests.post(
            f"{api_base}/login",
            json={"username": username, "password": password},
            timeout=10,
        )
    except Exception as e:
        st.error(f"Login request failed: {e}")
        return

    if resp.status_code != 200:
        try:
            msg = resp.json().get("detail") or resp.text
        except Exception:
            msg = resp.text
        st.error(msg or f"Login failed with status {resp.status_code}.")
        return

    data = resp.json()
    token = data.get("access_token")
    token_type = data.get("token_type", "bearer")
    if not token:
        st.error("No access_token in response.")
        return

    st.session_state.jwt = token
    st.session_state.token_type = token_type

    claims = _decode_claims(token)
    st.session_state.current_user = {
        "username": username,
        "user_id": claims.get("user_id") or claims.get("sub"),
        "is_admin": bool(claims.get("is_admin", False)),
        "exp": claims.get("exp"),
    }

    st.session_state.data_loaded = False
    st.success("Logged in successfully.")
    st.rerun()
