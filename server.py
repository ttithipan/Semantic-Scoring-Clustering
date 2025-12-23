# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from services.ticket_scores import TicketEmbedder, cluster_tickets_by_semantics, batch_score_tickets

app = FastAPI()
embedder = TicketEmbedder() # Loads model immediately on startup

class TicketRequest(BaseModel):
    tickets: list

@app.post("/cluster")
def cluster(request: TicketRequest):
    return cluster_tickets_by_semantics(request.tickets, eps= 0.55)

@app.post("/score")
def score(request: TicketRequest):
    return batch_score_tickets(tickets = request.tickets)
