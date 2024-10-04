from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Set your OpenAI API key here
# 
# Prompt Template for breaking down tasks into Low-Level Language (LLL)
task_prompt_template = """
You are an assistant that translates high-level tasks into specific, executable steps using a Low-Level Language (LLL). 
Break down the following task into a sequence of atomic actions that can be passed to the Task Execution Engine.

User Task:
{user_input}

Instructions:
- Break down the task into simple, precise steps using Low-Level Language (LLL) syntax.
- Each step should represent an atomic action, e.g., "open_application('Outlook')", "click_element('Inbox')", etc.
- Use ephemeral memory to pass intermediate information, like the email retrieved.

Here’s an example of how to break down a task:
Task: "Retrieve an email from Vendor X and create a bill in QuickBooks."
Low-Level Steps:
1. open_application('Outlook')
2. ensure_screen('Inbox')
3. retrieve_email('Vendor X') -> ephemeral_memory['email_info']
4. open_application('QuickBooks')
5. ensure_screen('Bill Creation')
6. create_bill(ephemeral_memory['email_info'])

Now break down the user task.
"""

# Create LangChain prompt template
task_prompt = PromptTemplate(template=task_prompt_template, input_variables=['user_input'])

# Memory buffer for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", input_key="user_input")

# Function to process user input and generate low-level steps using LangChain
def get_lll_steps(user_input):
    # Simulated function to execute a conversation chain
    conversation_chain = ConversationChain(
        llm=client,  # Insert your LLM model here (e.g., OpenAI GPT)
        memory=memory,
        prompt=task_prompt
    )

    try:
        # Generate the low-level language (LLL) steps from user input
        lll_steps = conversation_chain.run(user_input)
        return lll_steps
    except Exception as e:
        return f"Error: {e}"
