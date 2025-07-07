#!/usr/bin/env python3
"""
Server MCP di test per gestire una todo list
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from fastmcp import FastMCP

# Struttura dati in memoria per i todo items
todos: Dict[str, Dict] = {}
next_id = 1

# Inizializza il server MCP
mcp = FastMCP("Todo List Server")

@mcp.tool()
def add_todo(title: str, description: str = "") -> str:
    """
    Aggiunge un nuovo todo item alla lista
    
    Args:
        title: Titolo del todo
        description: Descrizione opzionale del todo
    
    Returns:
        ID del todo creato
    """
    global next_id
    
    todo_id = str(next_id)
    next_id += 1
    
    todos[todo_id] = {
        "id": todo_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    return f"Todo creato con ID: {todo_id}"

@mcp.tool()
def get_todos() -> str:
    """
    Ottiene tutti i todo items
    
    Returns:
        Lista di tutti i todo in formato JSON
    """
    if not todos:
        return "Nessun todo trovato"
    
    return json.dumps(list(todos.values()), indent=2, ensure_ascii=False)

@mcp.tool()
def get_todo(todo_id: str) -> str:
    """
    Ottiene un todo specifico per ID
    
    Args:
        todo_id: ID del todo da recuperare
    
    Returns:
        Dettagli del todo in formato JSON
    """
    if todo_id not in todos:
        return f"Todo con ID {todo_id} non trovato"
    
    return json.dumps(todos[todo_id], indent=2, ensure_ascii=False)

@mcp.tool()
def update_todo(todo_id: str, title: Optional[str] = None, 
                description: Optional[str] = None, 
                completed: Optional[bool] = None) -> str:
    """
    Aggiorna un todo esistente
    
    Args:
        todo_id: ID del todo da aggiornare
        title: Nuovo titolo (opzionale)
        description: Nuova descrizione (opzionale)
        completed: Nuovo stato di completamento (opzionale)
    
    Returns:
        Messaggio di conferma
    """
    if todo_id not in todos:
        return f"Todo con ID {todo_id} non trovato"
    
    todo = todos[todo_id]
    
    if title is not None:
        todo["title"] = title
    if description is not None:
        todo["description"] = description
    if completed is not None:
        todo["completed"] = completed
        if completed:
            todo["completed_at"] = datetime.now().isoformat()
    
    todo["updated_at"] = datetime.now().isoformat()
    
    return f"Todo {todo_id} aggiornato con successo"

@mcp.tool()
def delete_todo(todo_id: str) -> str:
    """
    Elimina un todo
    
    Args:
        todo_id: ID del todo da eliminare
    
    Returns:
        Messaggio di conferma
    """
    if todo_id not in todos:
        return f"Todo con ID {todo_id} non trovato"
    
    deleted_todo = todos.pop(todo_id)
    return f"Todo '{deleted_todo['title']}' eliminato con successo"

@mcp.tool()
def get_completed_todos() -> str:
    """
    Ottiene tutti i todo completati
    
    Returns:
        Lista dei todo completati in formato JSON
    """
    completed = [todo for todo in todos.values() if todo["completed"]]
    
    if not completed:
        return "Nessun todo completato trovato"
    
    return json.dumps(completed, indent=2, ensure_ascii=False)

@mcp.tool()
def get_pending_todos() -> str:
    """
    Ottiene tutti i todo in sospeso
    
    Returns:
        Lista dei todo in sospeso in formato JSON
    """
    pending = [todo for todo in todos.values() if not todo["completed"]]
    
    if not pending:
        return "Nessun todo in sospeso trovato"
    
    return json.dumps(pending, indent=2, ensure_ascii=False)

@mcp.tool()
def clear_completed_todos() -> str:
    """
    Elimina tutti i todo completati
    
    Returns:
        Messaggio di conferma con il numero di todo eliminati
    """
    completed_ids = [todo_id for todo_id, todo in todos.items() if todo["completed"]]
    
    if not completed_ids:
        return "Nessun todo completato da eliminare"
    
    for todo_id in completed_ids:
        todos.pop(todo_id)
    
    return f"Eliminati {len(completed_ids)} todo completati"

@mcp.resource("todo://stats")
def get_todo_stats() -> str:
    """
    Risorsa che fornisce statistiche sui todo
    """
    total = len(todos)
    completed = sum(1 for todo in todos.values() if todo["completed"])
    pending = total - completed
    
    stats = {
        "total_todos": total,
        "completed_todos": completed,
        "pending_todos": pending,
        "completion_rate": f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
    }
    
    return json.dumps(stats, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Aggiungi alcuni todo di esempio
    add_todo("Studiare FastMCP", "Imparare come funziona il Model Context Protocol")
    add_todo("Creare un progetto di test", "Sviluppare un server MCP funzionante")
    add_todo("Scrivere documentazione", "Documentare il progetto per riferimento futuro")
    
    # Avvia il server
    mcp.run(transport="stdio")