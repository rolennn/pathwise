# support_funcs.py
import pandas as pd
import numpy as np
from datetime import date
import json

def format_currency(value):
	return f"₱ {int(value):,}"
	
def process_json(json_obj):
	return json.loads(json_obj)

	
if __name__ == "__main__":
	pass
