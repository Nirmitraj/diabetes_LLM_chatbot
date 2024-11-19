# prompt_template="""
# Use the following pieces of information to answer the user's question.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.

# Context: {context}
# Question: {question}

# Only return the helpful answer below and nothing else.
# Helpful answer:
# """

prompt_template = """You are a helpful assistant. Given the following conversation and a follow-up question, provide a helpful and accurate answer.

Chat History:
{chat_history}

Context from the retrieved documents:
{context}

Question:
{question}

Only return the helpful answer below and nothing else.
Helpful answer:"""

# question_categorize_prompt_template = """
# Given the following queries, classify them into one of two categories: "general" or "medical".
    
# 1. "Hi, how are you?" -> general
# 2. "What are you doing?" -> general
# 3. "What are the side effects of aspirin?" -> medical
# 4. "Is fever a symptom of COVID-19?" -> medical
# 5. "{question}" ->
# """

question_categorize_prompt_template = """
You are a medical assistant specialized in diabetes. Based on the chat history and the current query, categorize the user query as either "diabetes" or "not-diabetes".
Note: ONLY give response as either "diabetes" or "not-diabetes"

Chat History:
User: "I was diagnosed with type 2 diabetes last year."
AI: "I see. Do you have any specific concerns about managing your diabetes?"

User: "What is a good breakfast for someone with diabetes?"
AI: "It's important to have a balanced meal with controlled carbs. Oatmeal with nuts or a veggie omelette can be good choices."

User Query: "Can you suggest some exercises for lowering blood sugar?"
Category: diabetes

Chat History:
User: "I'm planning to travel to Europe next month."
AI: "That sounds exciting! Do you need any travel tips or health advice?"

User Query: "How long is the flight from New York to Paris?"
Category: not-diabetes

Chat History:
User: "I've been feeling really tired lately."
AI: "Fatigue can have many causes. Is it related to your diabetes or something else?"

User Query: "Could my diabetes be causing my fatigue?"
Category: diabetes

# Direct diabetes-related questions without needing prior context

User Query: "What are the early symptoms of diabetes?"
Category: diabetes

User Query: "How can I prevent complications from diabetes?"
Category: diabetes

User Query: "Is it safe for someone with diabetes to drink alcohol?"
Category: diabetes

User Query: "What medications are commonly prescribed for type 2 diabetes?"
Category: diabetes

User Query: "What is the best way to monitor my blood sugar levels?"
Category: diabetes

# General or unrelated questions

User Query: "What is the capital of France?"
Category: not-diabetes

User Query: "Can you help me with my math homework?"
Category: not-diabetes

User Query: "What's the weather like today?"
Category: not-diabetes

User Query: "How do I set up a new phone?"
Category: not-diabetes

Chat History:
{chat_history}

User Query: "{question}"
Category:
"""

conversation_prompt_template = """
You are a medical assistant specialized in diabetes and having a conversation with a user. Below is the chat history:

{chat_history}
    
User: {question}
AI:
"""