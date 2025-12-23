import torch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from typing import List, Dict, Union, Optional

# CONSTANTS - distinct from logic
ERROR_CODES = {"400", "401", "403", "404", "408", "500", "502", "503", "504"}
ERROR_PATHS = {"/api", "/home", "/login", "/var", "/log"}

class TicketEmbedder:
    def __init__(self):
        self._model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    @property
    def model(self):
        if self._model is None:
            print("Loading Model...")
            self._model = SentenceTransformer('all-mpnet-base-v2',device=self.device)
        return self._model
    
    def encode(self, tickets, batch_size = 32, show_progress_bar = True):
        return self.model.encode(tickets, batch_size=batch_size, show_progress_bar=show_progress_bar, convert_to_numpy=True)

embedder = TicketEmbedder()

def calculate_ticket_score(text: Optional[str]) -> int:
    """
    :param text: Input string.
    :type text: Optional[str]
    :return: score
    :rtype: int
    """
    if not text:
        return 0
    text = str(text)
    text_length = len(text)
    score = min(text_length // 10, 5)

    if any(code in text for code in ERROR_CODES):
        score += 15
    if any(path in text for path in ERROR_PATHS):
        score += 10

    if text_length < 20:
        score -= 10
    elif 100 <= text_length <= 1000:
        score += 5
    elif text_length > 2000:
        score -= 5

    return score

def batch_score_tickets(tickets: Union[str, List[str]]) -> Union[int, List[int]]:
    if isinstance(tickets, str):
        return calculate_ticket_score(tickets)
    
    if isinstance(tickets, list):
        return [calculate_ticket_score(t) for t in tickets]
    
    raise ValueError(f"Expected list or string, got {type(tickets)}")

def cluster_tickets_by_semantics(
    tickets: List[str], 
    eps: float = 0.55, 
    min_samples: int = 2,
    batch_size: int = 32
) -> Dict[int, List[int]]:
    """
    Clusters tickets and returns a mapping of ClusterID -> List of Ticket INDICES.
    Arguments allow tuning without changing code.
    """
    if not tickets:
        return {}
    
    # IMPROVEMENT 2: Control Batch Size
    # If you throw 10k tickets at the GPU at once, it might OOM.
    # .encode(batch_size=32) processes them in chunks.
    embeddings = embedder.model.encode(
        tickets, 
        batch_size=batch_size, 
        convert_to_numpy=True, 
        show_progress_bar=True
    )
    
    # IMPROVEMENT 3: Flexible Parameters
    clustering_model = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    cluster_assignment = clustering_model.fit_predict(embeddings)

    # IMPROVEMENT 4: Return Indices, not Strings (Memory Efficient)
    clustered_indices = {}
    
    # Enumerate gives us the index (i) and the cluster_id
    for i, cluster_id in enumerate(cluster_assignment):
        cluster_id = int(cluster_id) # Convert numpy.int to python int
        
        if cluster_id not in clustered_indices:
            clustered_indices[cluster_id] = []
        clustered_indices[cluster_id].append(i)
        
    return clustered_indices