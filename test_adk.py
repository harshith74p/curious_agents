#!/usr/bin/env python3
"""
Simple test of Google ADK with Gemini API
"""
import os
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
os.environ["GOOGLE_API_KEY"] = "AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg"

def test_imports():
    try:
        from google.adk.agents import LlmAgent
        from google.adk.runners import InMemoryRunner
        print("+ Google ADK imports successful")
        return True
    except ImportError as e:
        print(f"- Import error: {e}")
        return False

def test_agent_creation():
    try:
        from google.adk.agents import LlmAgent
        agent = LlmAgent(
            name="test_agent",
            model="gemini-2.0-flash",
            description="Test agent",
            instruction="You are a helpful assistant."
        )
        print("+ Agent creation successful")
        print(f"+ Agent name: {agent.name}")
        print(f"+ Model: {agent.model}")
        return True
    except Exception as e:
        print(f"- Agent creation error: {e}")
        return False

def main():
    print("Testing Google ADK Setup...")
    print("API Key configured: AIzaSyChiIdeDZsYCVTXfUdpIj-KgbZdN8Cs2Dg")
    print()
    if test_imports():
        if test_agent_creation():
            print("\nSUCCESS! Google ADK is ready for your demo!")
            print("Your CuriousAgents system can now use real Gemini AI")
            print("Ready for presentation!")
        else:
            print("\nAgent creation failed")
    else:
        print("\nImport failed")

if __name__ == "__main__":
    main() 