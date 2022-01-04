from dataclasses import dataclass

@dataclass
class Account:
    """Account metaclass for storing secrets.
    """
    cookies: str
    gvoice_key: str
    phone_number: str
    
    def __init__(self, cookies: str, gvoice_key: str, phone_number: str):
        self.cookies = cookies
        self.gvoice_key = gvoice_key
        self.phone_number = phone_number