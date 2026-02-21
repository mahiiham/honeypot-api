import re

def extract_entities(text):
    
    phone_pattern = r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b'
    email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    url_pattern = r'\bhttps?://[^\s]+\b'
    upi_pattern = r'\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b'
    bank_pattern = r'\b\d{9,18}\b'                    
    case_pattern = r'\b[A-Z]{2,}-?\d{3,}\b'
    policy_pattern = r'\bPOL\d{4,}\b'
    order_pattern = r'\bORD\d{4,}\b'

    extracted = {
        "phoneNumbers": re.findall(phone_pattern, text),
        "emailAddresses": re.findall(email_pattern, text),
        "phishingLinks": re.findall(url_pattern, text),
        "upiIds": re.findall(upi_pattern, text),
        "bankAccounts": re.findall(bank_pattern, text),
        "caseIds": re.findall(case_pattern, text),
        "policyNumbers": re.findall(policy_pattern, text),
        "orderNumbers": re.findall(order_pattern, text),
    }

    
    cleaned_phones = []
    for p in extracted["phoneNumbers"]:
        digits = re.sub(r'\D', '', p)          
        if len(digits) == 10 and digits[0] in '6789':
            cleaned_phones.append(p)
    extracted["phoneNumbers"] = cleaned_phones

    return extracted