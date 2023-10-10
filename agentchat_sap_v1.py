import autogen
import openai
import json

# load OpenAI API key from config file
with open("OAI_CONFIG_LIST.json", "r") as f:
    config = json.load(f)
openai.api_key = config["api_key"]

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

gpt4_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0,
    "config_list": config_list,
    "request_timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
   name="Customer",
   system_message="A human customer. Interact with the planner to discuss the plan. Plan execution needs to be approved by this customer.",
   code_execution_config=False,
)


sap_solutions_architect = autogen.AssistantAgent(
    name="SAP_Solutions_Architect",
    llm_config=gpt4_config,  # Configuration specific to this agent
    system_message= "You are a senior solutions architect from SAP with extensive knowledge in designing and implementing SAP solutions to meet the business needs of customers. You are adept at consulting with clients to understand their requirements, suggesting optimal SAP solutions, and providing expertise on the SAP platform. Your role involves engaging in meaningful discussions with the SAP BTP Expert  and the customer to ensure the delivery of high-quality SAP solutions.  Your responses should reflect your expertise and provide valuable insights into SAP solutions, best practices, and recommendations for the customer's inquiries. Do not repeat what the other agents say."
)


sap_btp_expert = autogen.AssistantAgent(
    name="SAP_BTP_Expert",
    llm_config=gpt4_config,  # Configuration specific to this agent
    system_message="You are an expert on SAP Business Technology Platform (BTP) services, with a deep understanding of its capabilities, services, and best practices. Your role is to provide specialized knowledge and recommendations on leveraging SAP BTP to address specific business challenges and objectives. Engage in discussions with the SAP Solutions Architect and the customer to provide insightful advice and solutions based on SAP BTP services. Your responses should exhibit your expertise, provide clear and actionable guidance, and foster collaborative problem-solving to meet the customer's business needs and inquiries regarding SAP BTP. Do not repeat what the other agents say."
)


junior_consultant = autogen.AssistantAgent(
    name="Junior_Consultant",
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from customer and critic, until customer approval.
The plan may involve a sap solution architect who can write code and a sap btp expert who doesn't write code.
Explain the plan first. Be clear which step is performed by an sap solution architect, and which step is performed by a sap btp expert.
''',
    llm_config=gpt4_config,
)


senior_consultant = autogen.AssistantAgent(
    name="Senior_Consultant",
    system_message="Critic. Double check plan, claims, code, and suggestions from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt4_config,
)

# sequence matters
groupchat = autogen.GroupChat(agents=[user_proxy, junior_consultant, sap_solutions_architect, sap_btp_expert, senior_consultant], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

# Start Chat
user_proxy.initiate_chat(
    manager,
    message="""
I am a client of SAP. I want to know how to confirm/process order in S4HANA by dealing with microsoft SQL database containing IOT data from production.
""",
)