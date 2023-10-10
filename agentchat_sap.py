import autogen
import openai
import json

# load OpenAI API key from config file
with open("OAI_CONFIG_LIST.json", "r") as f:
    config = json.load(f)
openai.api_key = config["api_key"]

# Configuration list for the different agents
# Loads a list of configurations from an environment variable or a json file
# 1. SAP solutions architect
# 2. SAP BTP expert
# 3. customer of SAP

# SAP solutions architect config list
sap_architect_config_list = autogen.config_list_from_json(
    "SOL_ARCHITECT_CONFIG_LIST", 
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

# SAP BTP expert config list
btp_expert_config_list = autogen.config_list_from_json(
    "BTP_EXPERT_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

# Agent: SAP solutions architect
sap_solutions_architect = autogen.AssistantAgent(
    name="SAP_Solutions_Architect",
    llm_config={"config_list": sap_architect_config_list},  # Configuration specific to this agent
)

# Agent: SAP BTP expert
sap_btp_expert = autogen.AssistantAgent(
    name="SAP_BTP_Expert",
    llm_config={"config_list": btp_expert_config_list},  # Configuration specific to this agent
)

# Agent: a customer of SAP
customer = autogen.UserProxyAgent(
    name="Customer",
    human_input_mode="REAL_TIME",  # Allow real-time input from the customer
)
