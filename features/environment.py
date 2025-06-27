import os
from dotenv import load_dotenv

def before_all(context):
    load_dotenv()  # Load .env file
    context.base_url = os.getenv("BASE_URL")
    context.ws_url = os.getenv("WS_URL")
    print(f"Environment setup: BASE_URL={context.base_url}, WS_URL={context.ws_url}")

def after_all(context):
    print("Test run completed.")

def before_scenario(context, scenario):
    print(f"Starting scenario: {scenario.name}")

def after_scenario(context, scenario):
    if scenario.status == "failed":
        print(f"Scenario failed: {scenario.name}")
    else:
        print(f"Scenario passed: {scenario.name}")
