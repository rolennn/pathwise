# wallet.py

import streamlit as st
import pandas as pd
import plotly.express as px
import support_funcs as sf


st.set_page_config(page_title="Wallet", layout="centered")

# gather session data
data = st.session_state.users_data
role = st.session_state.role
financial_profile = sf.process_json(data[data['name'] == role].iloc[0,4])
savings_investment = sf.process_json(data[data['name'] == role].iloc[0,5])
debt = sf.process_json(data[data['name'] == role].iloc[0,6])
expenses = sf.process_json(data[data['name'] == role].iloc[0,7])
budget = sf.process_json(data[data['name'] == role].iloc[0,8])

st.title("Digital Wallet")	
st.markdown("Keep track of your finances, budgets, savings, and debts.")


# financial_profile
st.markdown("---")
st.subheader("Financial Profile")
cards = st.columns(4)
for (card, info) in zip(cards, financial_profile):
	with card: 
		with st.container(border=True):
			key = f'edit_fp_{info["title"]}'
			st.markdown(f"##### {info['title']}")
			st.write(sf.format_currency(info["value"]))
			if st.button(label="Edit", key=key, help="Change value", use_container_width=True, icon=":material/edit:", disabled=True):
				pass

# budget performance
st.markdown("---")
st.subheader("Budget Performance")
blist, bchart = st.columns([1,1.5])

with blist:
	st.write("Monthly Budget")
	for info in budget: 
		percent = float(info["current"]) / float(info["goal"])
		with st.container(border=True):
			label, edits = st.columns([4,1])
			with label:
				st.markdown(f"##### {info['title']}")
				st.markdown(
					f"**{sf.format_currency(info['current'])}** of **{sf.format_currency(info['goal'])}**: {percent:.2%}"
				)
			with edits: 
				rem_key = f'rem_bp_{info["title"]}'
				edit_key = f'edit_bp_{info["title"]}'
				if st.button(label="", key=rem_key, icon=":material/close:", disabled=True):
					pass
				if st.button(label="", key=edit_key, icon=":material/edit:", disabled=True):
					pass
with bchart:
	st.write("Spending Breakdown")

			
# savings and investments
st.markdown("---")
st.subheader("Savings and Investments")
for info in savings_investment:
	with st.container(border=True):
		label, edits = st.columns([11,1])
		with label:
			st.markdown(f"##### {info['title']}")
			st.markdown(
				f"**{sf.format_currency(info['current'])}** of **{sf.format_currency(info['goal'])}**: {percent:.2%}"
			)
		with edits: 
			rem_key = f'rem_si_{info["title"]}'
			edit_key = f'edit_si_{info["title"]}'
			if st.button(label="", key=rem_key, icon=":material/close:", disabled=True):
				pass
			if st.button(label="", key=edit_key, icon=":material/edit:", disabled=True):
				pass
if st.button(label="Add new category", key="si_cat", icon=":material/add:", disabled=True, use_container_width=True):
	pass


# debt tracking
st.markdown("---")
st.subheader("Debt Monitoring")
for info in debt:
	percent = float(info['current_balance']) / float(info['orig_balance'])
	with st.container(border=True):
		label, edits = st.columns([11,1])
		with label:
			st.markdown(f"##### {info['title']}")
			st.markdown(
				f"**{sf.format_currency(info['orig_balance'])}** for **{sf.format_currency(info['monthly_payment'])}** per month ({info['interest']}% interest)"
			)
			st.markdown(f"Due: {sf.format_currency(info['current_balance'])} ({percent:.2%})")
		with edits: 
			rem_key = f'rem_dm_{info["title"]}'
			edit_key = f'edit_dm_{info["title"]}'
			if st.button(label="", key=rem_key, icon=":material/close:", disabled=True):
				pass
			if st.button(label="", key=edit_key, icon=":material/edit:", disabled=True):
				pass
if st.button(label="Add new category", key="dm_cat", icon=":material/add:", disabled=True, use_container_width=True):
	pass
