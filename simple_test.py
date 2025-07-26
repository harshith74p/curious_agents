#!/usr/bin/env python3
"""
Simple test to debug the hanging issue
"""
import os
import sys
import time

print("Simple test starting...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Test 1: Basic imports
print("\nTest 1: Basic imports")
try:
    import json
    print("+ json import successful")
except Exception as e:
    print(f"- json import failed: {e}")

# Test 2: Check if google-adk is installed
print("\nTest 2: Check google-adk installation")
try:
    import google
    print("+ google package found")
    print(f"  Google package location: {google.__file__}")
except Exception as e:
    print(f"- google package not found: {e}")

# Test 3: Try to import ADK with timeout
print("\nTest 3: Testing ADK import (this might hang)")
try:
    print("  Attempting to import google.adk...")
    import google.adk
    print("+ google.adk import successful")
    
    print("  Attempting to import LlmAgent...")
    from google.adk.agents import LlmAgent
    print("+ LlmAgent import successful")
    
except Exception as e:
    print(f"- ADK import failed: {e}")

print("\nTest complete!") 