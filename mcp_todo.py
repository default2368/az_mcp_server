"""
Modulo MCP per gestire una todo list
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

# Modelli Pydantic per la validazione
class TodoCreate(BaseModel):
    title: str
    description: str = ""

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None

class TodoStats(BaseModel):
    total_todos: int
    completed_todos: int
    pending_todos: int
    completion_rate: str

class MCPTodoManager:
    """Gestore MCP per la todo list"""
    
    def __init__(self):
        self.todos: Dict[str, Dict] = {}
        self.next_id = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Inizializza con dati di esempio"""
        self.mcp_create_todo("Studiare FastMCP", "Imparare come funziona il Model Context Protocol")
        self.mcp_create_todo("Creare un progetto di test", "Sviluppare un server MCP funzionante")
        self.mcp_create_todo("Scrivere documentazione", "Documentare il progetto per riferimento futuro")
    
    def mcp_create_todo(self, title: str, description: str = "") -> Dict:
        """Crea un nuovo todo item (MCP Tool)"""
        todo_id = str(self.next_id)
        self.next_id += 1
        
        todo = {
            "id": todo_id,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        self.todos[todo_id] = todo
        return todo
    
    def mcp_get_all_todos(self) -> List[Dict]:
        """Ottiene tutti i todo items (MCP Tool)"""
        return list(self.todos.values())
    
    def mcp_get_todo_by_id(self, todo_id: str) -> Optional[Dict]:
        """Ottiene un todo specifico per ID (MCP Tool)"""
        return self.todos.get(todo_id)
    
    def mcp_update_todo(self, todo_id: str, updates: Dict) -> Optional[Dict]:
        """Aggiorna un todo esistente (MCP Tool)"""
        if todo_id not in self.todos:
            return None
        
        todo = self.todos[todo_id]
        
        if "title" in updates and updates["title"] is not None:
            todo["title"] = updates["title"]
        if "description" in updates and updates["description"] is not None:
            todo["description"] = updates["description"]
        if "completed" in updates and updates["completed"] is not None:
            todo["completed"] = updates["completed"]
            if updates["completed"]:
                todo["completed_at"] = datetime.now().isoformat()
        
        todo["updated_at"] = datetime.now().isoformat()
        return todo
    
    def mcp_delete_todo(self, todo_id: str) -> Optional[Dict]:
        """Elimina un todo (MCP Tool)"""
        if todo_id not in self.todos:
            return None
        return self.todos.pop(todo_id)
    
    def mcp_get_completed_todos(self) -> List[Dict]:
        """Ottiene tutti i todo completati (MCP Tool)"""
        return [todo for todo in self.todos.values() if todo["completed"]]
    
    def mcp_get_pending_todos(self) -> List[Dict]:
        """Ottiene tutti i todo in sospeso (MCP Tool)"""
        return [todo for todo in self.todos.values() if not todo["completed"]]
    
    def mcp_clear_completed_todos(self) -> Dict:
        """Elimina tutti i todo completati (MCP Tool)"""
        completed_ids = [todo_id for todo_id, todo in self.todos.items() if todo["completed"]]
        
        if not completed_ids:
            return {"message": "Nessun todo completato da eliminare", "deleted_count": 0}
        
        for todo_id in completed_ids:
            self.todos.pop(todo_id)
        
        return {"message": f"Eliminati {len(completed_ids)} todo completati", "deleted_count": len(completed_ids)}
    
    def mcp_get_stats(self) -> Dict:
        """Calcola statistiche sui todo (MCP Resource)"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos.values() if todo["completed"])
        pending = total - completed
        
        return {
            "total_todos": total,
            "completed_todos": completed,
            "pending_todos": pending,
            "completion_rate": f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
        }
    
    def get_mcp_tools(self) -> Dict:
        """Restituisce la lista degli strumenti MCP disponibili"""
        return {
            "tools": [
                {
                    "name": "create_todo",
                    "description": "Crea un nuovo todo item",
                    "parameters": {
                        "title": {"type": "string", "description": "Titolo del todo"},
                        "description": {"type": "string", "description": "Descrizione del todo", "optional": True}
                    }
                },
                {
                    "name": "get_all_todos",
                    "description": "Ottiene tutti i todo items",
                    "parameters": {}
                },
                {
                    "name": "get_todo_by_id",
                    "description": "Ottiene un todo specifico",
                    "parameters": {
                        "todo_id": {"type": "string", "description": "ID del todo"}
                    }
                },
                {
                    "name": "update_todo",
                    "description": "Aggiorna un todo esistente",
                    "parameters": {
                        "todo_id": {"type": "string", "description": "ID del todo"},
                        "title": {"type": "string", "description": "Nuovo titolo", "optional": True},
                        "description": {"type": "string", "description": "Nuova descrizione", "optional": True},
                        "completed": {"type": "boolean", "description": "Stato completamento", "optional": True}
                    }
                },
                {
                    "name": "delete_todo",
                    "description": "Elimina un todo",
                    "parameters": {
                        "todo_id": {"type": "string", "description": "ID del todo"}
                    }
                },
                {
                    "name": "get_completed_todos",
                    "description": "Ottiene i todo completati",
                    "parameters": {}
                },
                {
                    "name": "get_pending_todos",
                    "description": "Ottiene i todo in sospeso",
                    "parameters": {}
                },
                {
                    "name": "clear_completed_todos",
                    "description": "Elimina tutti i todo completati",
                    "parameters": {}
                }
            ]
        }
    
    def get_mcp_resources(self) -> Dict:
        """Restituisce la lista delle risorse MCP disponibili"""
        return {
            "resources": [
                {
                    "uri": "todo://stats",
                    "description": "Statistiche sui todo",
                    "mimeType": "application/json"
                },
                {
                    "uri": "todo://list",
                    "description": "Lista completa dei todo",
                    "mimeType": "application/json"
                }
            ]
        }

# Istanza globale del gestore
todo_manager = MCPTodoManager()