def calculate_address_score(addr, is_route, is_street_number):
    score = 10.0
    
    if len(addr) < 5 or len(addr) > 60:
        score *= 0.7
        
    if not is_route:
        score *= 0.8
        
    if not is_street_number:
        score *= 0.6
        
    return round(score)