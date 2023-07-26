from src.juno import Juno

def pizza_order_simulation():
    """
    A simulation of two agents talking to each other about ordering a pizza
    
    Agents are created using Juno and use the following methods to interact:
    .process() used to process and produce a response to the other agent's input
    .verbalize() performs text-to-speech on the agent's response
    Note:
    .listen() is not used since input is coming from the other agent rather than the user
    """
    
    # instructions for agent one
    agent_one_prompt = "Pretend you are ordering a pizza over the phone"
    # instructions for agent two
    agent_two_prompt = "Pretend you work at a pizza place and are taking an order from a customer over the phone"
    
    # creating bot agents using Juno
    customer = Juno(name='John', # name of the agent
                    role='customer', # role of the agent
                    gender='male', # gender of the agent
                    personality='sassy', # personality the agent will embody
                    prompt=agent_one_prompt, # prompt that GPT will use to generate a response
                    unique=True, # if True, the agent will have its own settings file. If you want to create multiple agents, this should be set to True for all agents
                    voice_engine='azure', # voice engine to be used for text-to-speech (currently only supports 'azure' or 'elevenlabs')
                    voice_name='jacob', # name of the voice to be used for text-to-speech
                    startup_sound=False) # if True, the bot will play a startup sound when initialized
    
    employee = Juno(name='Sarah',
                    role='employee', 
                    gender='female',
                    personality='friendly', 
                    prompt=agent_two_prompt,
                    unique=True,
                    voice_engine='elevenlabs',
                    voice_name='bella',
                    startup_sound=False)
    
    # starting the conversation with agent one's initial input
    beginning_input = 'I would like a cheese pizza with extra cheese please'
    customer.verbalize(beginning_input)
    
    # agent two's initial response
    employee_response = employee.process(beginning_input)
    employee.verbalize(employee_response)
    
    # endless loop of both agents exchanging pizza-order-related dialog :)
    while True:
        
        customer_response = customer.process(employee_response)
        customer.verbalize(customer_response)
        
        employee_response = employee.process(customer_response)
        employee.verbalize(employee_response)
        
if __name__ == '__main__':  
    pizza_order_simulation()