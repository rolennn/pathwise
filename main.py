import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="centered")

# connect to gsheet, then save info in session_state.users_data
conn = st.connection("gsheets", type=GSheetsConnection)
if "users_data" not in st.session_state: 
	st.session_state.users_data = conn.read()

if "role" not in st.session_state:
    st.session_state.role = None    
ROLES = [None, "USER1", "USER2", "GUEST"]


def login():
    st.header("Welcome to Pathwise!")
    role = st.selectbox(
		"Please choose from the following profiles.", 
		ROLES,
		help="If you want to see how the program works for pre-defined accounts, please choose either USER1 or USER2. If you want to try without an account, please choose GUEST."
	)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
about_page = st.Page("about_us.py",title="About Us", icon=":material/contact_page:")
wallet_page = st.Page("components/wallet.py",title="Digital Wallet", icon=":material/credit_card:")
dashboard_page = st.Page("components/dashboard.py",title="Dashboard", icon=":material/analytics:")
pathfinder_page = st.Page("components/pathfinder.py",title="Pathfinder", icon=":material/graph_4:")

if st.session_state.role in ["USER1", "USER2", "GUEST"]: 
	pg = st.navigation(
		{
			"Pathwise": [dashboard_page, wallet_page, pathfinder_page],
			"Prototype Guide":  [logout_page, about_page],
		}
	)
else:
	pg = st.navigation([st.Page(login)])
	
pg.run()
