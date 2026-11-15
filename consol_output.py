
def message_output(welcome = True, found_site = False, no_site = False):

    if welcome:
        message = "Choose your landing site."
    
    elif found_site:
        message = """We found an accessible 
        sample collection site!"""
    
    elif no_site:
        message = """No accessible sample collection 
        site within 100km!"""

    return message