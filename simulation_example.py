from src.juno import Juno

def pizza_order_simulation():
    """
    A simulation of two agents talking to each other about ordering pizza
    """
    
    # Prompt for Agent One
    agent_one_prompt = "Pretend you are ordering a pizza over the phone"
    # Prompt for Agent Two
    agent_two_prompt = "Pretend you work at a pizza place and are taking an order from over the phone"
    
    # Creating the agents
    agent_one = Juno(name='John', gender='male', prompt=agent_one_prompt)
    agent_two = Juno(name='Sarah', gender='female', prompt=agent_two_prompt)
    
    # To start the conversation, agent one will say something first
    beginning_input = 'I would like a cheese pizza with extra cheese please'
    agent_one.verbalize(beginning_input)
    
    # Agent two will process agent one's response and respond
    agent_two_response = agent_two.process(beginning_input)
    agent_two.verbalize(agent_two_response)
    
    # Endless loop of both agents talking to each other about ordering pizza :)
    while True:
        
        agent_one_response = agent_one.process(agent_two_response)
        agent_one.verbalize(agent_one_response)
        
        agent_two_response = agent_two.process(agent_one_response)
        agent_two.verbalize(agent_two_response)
        
if __name__ == '__main__':  
    pizza_order_simulation()