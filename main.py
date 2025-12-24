import requests

# --- 3. MOCK DATA ---
tickets = [
    "I cannot login", 
    "Login button broken",
    "Error 403: Access Denied when clicking login",
    "cant sign in",
    "Server is down",
    "Api is not responding",
    "500 Internal Server Error at /api/v1/checkout",
    "IT BROKE HELP",
    "The printer is out of paper",
]
cluster_response = requests.post("http://localhost:8000/cluster", json={"tickets": tickets})
scores_response = requests.post("http://localhost:8000/score", json={"tickets": tickets})
clustered_tickets = cluster_response.json()
tickets_score = scores_response.json()
champions = {}

for cluster_id, indices in clustered_tickets.items():
    # 1. Convert key to int to ensure safely checks against -1
    #    (JSON keys are always strings, e.g. "-1")
    c_id = int(cluster_id)

    if c_id == -1:
        print(f"--- Cluster {cluster_id} (Noise/Unclustered) ---")
        # Initialize a list to hold ALL noise items
        champions[cluster_id] = []
        
        for index in indices:
            score = tickets_score[index]
            text = tickets[index]
            
            # Print every single item
            print(f" - {text} (Score: {score})")
            
            # Save them all
            champions[cluster_id].append({
                "index": index,
                "score": score,
                "text": text
            })
            
    else:    
        best_index = max(indices, key=lambda i: tickets_score[i])
        
        champions[cluster_id] = {
            "index": best_index,
            "score": tickets_score[best_index],
            "text": tickets[best_index]
        }
        
        print(f"--- Cluster {cluster_id} ---")
        print(f"Champion: {tickets[best_index]} (Score: {tickets_score[best_index]})")
        for index in indices:
            score = tickets_score[index]
            text = tickets[index]
            
            # Print every single item
            print(f" - {text} (Score: {score})")