import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'streamlit'))

from functions.llm_chat_function import is_valid_mistral_key

def test_wrong_key():
    assert is_valid_mistral_key('abcdefghijklmnopqrstuvwxyz') == False

def test_empty_key():
    assert is_valid_mistral_key('') == False
