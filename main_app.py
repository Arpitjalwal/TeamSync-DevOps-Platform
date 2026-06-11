import sys
import os

# Ye current directory ka path dhoondhega
curr_dir = os.path.dirname(os.path.abspath(__file__))

# Backend aur Engines folders ko path mein jodd dega
sys.path.append(os.path.join(curr_dir, 'backend'))
sys.path.append(os.path.join(curr_dir, 'engines'))

# Ab imports wahi rahenge jo tumne likhe hain
from backend.db_connect import get_db_connection
from engines.sql_engine import run_sql_query, initialize_db, drop_table, reset_entire_db
from engines.python_sandbox import run_python_code

import streamlit as st
import pandas as pd
import os
import requests
from streamlit_lottie import st_lottie
from backend.db_connect import get_db_connection
from engines.sql_engine import run_sql_query, initialize_db, drop_table, reset_entire_db
from engines.python_sandbox import run_python_code

# --- CONFIG & CSS ---
st.set_page_config(page_title="TeamSync Pro Portal", layout="wide", initial_sidebar_state="expanded")

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- LOTTIE ANIMATION ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_url = "https://assets5.lottiefiles.com/packages/lf20_v4b5txuu.json"
lottie_data = load_lottieurl(lottie_url)

initialize_db()

# --- SESSION STATES ---
if "username" not in st.session_state: st.session_state.username = None
if "room_id" not in st.session_state: st.session_state.room_id = None

# --- AUTH ---
if not st.session_state.username:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        if lottie_data: st_lottie(lottie_data, height=200, key="login_anim")
        st.markdown("<h1 class='neon-text' style='text-align: center;'>TeamSync</h1>", unsafe_allow_html=True)
        name_input = st.text_input("Apna Naam:")
        if st.button("🚀 Enter Platform", use_container_width=True):
            if name_input:
                st.session_state.username = name_input
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("💻 TeamSync")
st.sidebar.write(f"Logged in: **{st.session_state.username}**")

if st.session_state.username.lower() == "admin":
    st.sidebar.markdown("---")
    st.sidebar.subheader("👑 Admin Controls")
    if st.sidebar.button("Clear Chat Logs"):
        for f in os.listdir("."):
            if f.startswith("chat_") and f.endswith(".txt"): os.remove(f)
        st.rerun()
    if st.sidebar.button("Factory Reset DB"):
        reset_entire_db()
        st.rerun()

# --- CHAT BOX (FIXED STYLING) ---
if st.session_state.room_id:
    chat_file = f"chat_{st.session_state.room_id}.txt"
    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Live Chat")
    
    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            chat_content = f.read()
        st.sidebar.markdown(f'<div class="chat-box">{chat_content}</div>', unsafe_allow_html=True)

    with st.sidebar.form("chat_form", clear_on_submit=True):
        msg = st.text_input("Type message...")
        if st.form_submit_button("Send"):
            if msg:
                with open(chat_file, "a") as f:
                    f.write(f"<b>{st.session_state.username}</b>: {msg}<br>")
                st.rerun()

if st.sidebar.button("⬅️ Logout"):
    st.session_state.username = None
    st.session_state.room_id = None
    st.rerun()

# --- WORKSPACE ---
if not st.session_state.room_id:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.title("👋 Welcome!")
    c1, c2 = st.columns(2)
    new_room = c1.text_input("Project Naam:")
    if c1.button("Create Room"):
        st.session_state.room_id = new_room.lower().replace(" ", "-")
        st.rerun()
    join_room = c2.text_input("Join Room ID:")
    if c2.button("Join"):
        st.session_state.room_id = join_room.lower()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

st.title(f"⚡ Workspace: {st.session_state.room_id.upper()}")
tab1, tab2, tab3 = st.tabs(["🗄️ SQL", "🐍 Python", "📊 BI"])

with tab1:
    query = st.text_area("SQL Command:", height=150)
    if st.button("Run SQL ⚡"):
        res = run_sql_query(query)
        if res["error"]: st.error(res["error"])
        elif res["data"] is not None: st.dataframe(res["data"])
        else: st.success("Success!")

with tab2:
    code = st.text_area("Python Code:", height=250)
    if st.button("Execute ⚡"):
        res = run_python_code(code)
        if res["error"]: st.error(res["error"])
        else: st.code(res["stdout"])

with tab3:
    res_tables = run_sql_query("SELECT name FROM sqlite_master WHERE type='table';")
    if res_tables["data"] is not None and not res_tables["data"].empty:
        first_table = res_tables["data"].iloc[0, 0]
        res_data = run_sql_query(f"SELECT * FROM {first_table}")
        if res_data["data"] is not None:
            st.bar_chart(res_data["data"].select_dtypes(include=['number']))
