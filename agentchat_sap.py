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
    "SOL_ARCHI_CONFIG_LIST_OAI", 
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

# SAP BTP expert config list
btp_expert_config_list = autogen.config_list_from_json(
    "BTP_EXPERT_CONFIG_LIST_OAI",
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)
# END OF CONFIG

# Agent definitions
# Agent: SAP solutions architect
sap_solutions_architect = autogen.AssistantAgent(
    name="SAP_Solutions_Architect",
    llm_config={"config_list": sap_architect_config_list},  # Configuration specific to this agent
    system_message= "You are a senior solutions architect from SAP with extensive knowledge in designing and implementing SAP solutions to meet the business needs of customers. You are adept at consulting with clients to understand their requirements, suggesting optimal SAP solutions, and providing expertise on the SAP platform. Your role involves engaging in meaningful discussions with the SAP BTP Expert  and the customer to ensure the delivery of high-quality SAP solutions.  Your responses should reflect your expertise and provide valuable insights into SAP solutions, best practices, and recommendations for the customer's inquiries."
)

# Agent: SAP BTP expert
sap_btp_expert = autogen.AssistantAgent(
    name="SAP_BTP_Expert",
    llm_config={"config_list": btp_expert_config_list},  # Configuration specific to this agent
    system_message="You are an expert on SAP Business Technology Platform (BTP) services, with a deep understandingof its capabilities, services, and best practices. Your role is to provide specialized knowledge and recommendations on leveraging SAP BTP to address specific business challenges and objectives. Engage in discussions with the SAP Solutions Architect and the customer to provide insightful advice and solutions based on SAP BTP services. Your responses should exhibit your expertise, provide clear and actionable guidance, and foster collaborative problem-solving to meet the customer's business needs and inquiries regarding SAP BTP."
)

# Agent: a customer of SAP
customer = autogen.UserProxyAgent(
    name="Customer",
    human_input_mode="REAL_TIME",  # Allow real-time input from the customer
)

def initiate_discussion(message):
    # This function can be used to initiate a discussion between the agents based on the customer's input
    customer.initiate_chat(sap_solutions_architect, message=message)
    # ... Additional logic to manage the discussion

def receive_customer_input(message):
    customer.send_message(sap_solutions_architect, message=message)
    # ... Additional logic to handle the customer's input

# def manage_discussion():
    # ... Logic to manage the discussion, e.g., routing messages between agents, handling customer input, etc.
