import streamlit as st
import pandas as pd
import requests


def _api_base() -> str:
    return st.session_state.get("API_BASE", "http://localhost:8000")


def _auth_headers() -> dict:
    token = st.session_state.get("jwt")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _refetch_users():
    try:
        r = requests.get(f"{_api_base()}/users", headers=_auth_headers(), timeout=10)
        if r.status_code == 200:
            st.session_state.users = r.json()["result"]
        else:
            st.error(f"GET /users failed: {r.status_code}")
    except Exception as e:
        st.error(f"GET /users error: {e}")


def users_page(users):
    st.header("Manage Users")

    df_users = pd.DataFrame(users)
    st.write("### Existing Users")
    st.dataframe(df_users, use_container_width=True)

    col_top = st.columns(3)
    with col_top[0]:
        if st.button("Refresh users"):
            _refetch_users()
            st.rerun()

    with st.form("new_user_form"):
        st.subheader("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        is_admin = st.checkbox("Is Admin")
        submit_user = st.form_submit_button("Add User")
        if submit_user:
            try:
                payload = {"username": username, "password": password, "is_admin": is_admin}
                r = requests.post(f"{_api_base()}/users", json=payload, headers=_auth_headers(), timeout=10)
                if r.status_code in (200, 201):
                    _refetch_users()
                    st.success("User added successfully.")
                    st.rerun()
                else:
                    st.error(f"POST /users failed: {r.status_code} {r.text}")
            except Exception as e:
                st.error(f"POST /users error: {e}")

    st.subheader("Delete User")
    options_del = {f"{u.get('user_id')} – {u.get('username','')}": u for u in users}
    selected_label_del = st.selectbox("Select User to delete", list(options_del.keys()) if options_del else [], key="delete_user_select")
    if st.button("Delete User"):
        if options_del:
            try:
                user_id = options_del[selected_label_del]["user_id"]
                r = requests.delete(f"{_api_base()}/users/{user_id}", headers=_auth_headers(), timeout=10)
                if r.status_code in (200, 204):
                    _refetch_users()
                    st.success(f"User {user_id} deleted successfully.")
                    st.rerun()
                else:
                    st.error(f"DELETE /users/{user_id} failed: {r.status_code} {r.text}")
            except Exception as e:
                st.error(f"DELETE /users error: {e}")
