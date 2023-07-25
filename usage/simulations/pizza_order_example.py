from src.juno import Juno

def pizza_order_simulation():
    """
    A simulation of two agents talking to each other about ordering a pizza
    
    Agents are created using Juno and use the following methods to interact:
    .process() is used to process the input of the other agent
    .verbalize() is used to produce a response to the other agent
    Note:
    .listen() is not used since input is coming from the other agent rather than the user
    """
    
    # Instructions for agent one
    agent_one_prompt = "Pretend you are ordering a pizza over the phone"
    # Instructions for agent two
    agent_two_prompt = "Pretend you work at a pizza place and are taking an order from a customer over the phone"
    
    # Creating the agents
    customer = Juno(name='John', gender='male', prompt=agent_one_prompt)
    employee = Juno(name='Sarah', gender='female', prompt=agent_two_prompt)
    
    # starting the conversation with agent one's initial input
    beginning_input = 'I would like a cheese pizza with extra cheese please'
    customer.verbalize(beginning_input)
    
    # agent two's initial response
    employee_response = employee.process(beginning_input)
    employee.verbalize(employee_response)
    
    # Endless loop of both agents exchanging pizza-order-related dialog :)
    while True:
        
        customer_response = customer.process(employee_response)
        customer.verbalize(customer_response)
        
        employee_response = employee.process(customer_response)
        employee.verbalize(employee_response)
        
if __name__ == '__main__':  
    pizza_order_simulation()