from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
import uvicorn

# Importa i moduli MCP
from mcp import todo_manager, TodoCreate, TodoUpdate, Todo, TodoStats

# Importa i tool
from tools import get_weather, get_weather_dynamic

# Importa il modulo di sampling
from sampling import code_review, request_sampling, CodeReviewRequest, SamplingRequest

app = FastAPI(
    title="FastAPI + MCP Server",
    description="Server FastAPI che integra funzionalità MCP per meteo e todo list",
    version="1.0.0"
)

# === ENDPOINT METEO ===

@app.post("/mcp/tools/get_weather", response_model=Dict)
async def weather_endpoint(location: str):
    """Endpoint per ottenere il meteo simulato"""
    return await get_weather(location)

@app.post("/mcp/tools/get_weather_dynamic", response_model=Dict)
async def weather_dynamic_endpoint(location: str):
    """Endpoint per ottenere il meteo reale da OpenWeatherMap"""
    return await get_weather_dynamic(location)

# === ENDPOINT SAMPLING ===

@app.post("/mcp/prompts/code_review", response_model=List[Dict])
async def code_review_endpoint(request: CodeReviewRequest):
    """Endpoint per la revisione del codice"""
    return await code_review(request)

@app.post("/mcp/sampling/request_sampling", response_model=Dict)
async def sampling_endpoint(request: SamplingRequest):
    """Endpoint per le richieste di sampling"""
    return await request_sampling(request)

# === ENDPOINT FILE RESOURCE ===

@app.get("/mcp/resources/read_file", response_model=Dict)
async def read_file(file_path: str):
    """
    Simula un resource che legge il contenuto di un file.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Errore nella lettura del file: {str(e)}")

# === NUOVI ENDPOINT MCP TODO ===

# Endpoint RESTful per compatibilità con i test esistenti
@app.get("/mcp/todos", response_model=List[Todo])
async def get_todos():
    """Ottieni tutti i todo (endpoint RESTful)"""
    return todo_manager.mcp_get_all_todos()

@app.post("/mcp/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    """Crea un nuovo todo (endpoint RESTful)"""
    return todo_manager.mcp_create_todo(todo.title, todo.description)

@app.get("/mcp/todos/status/completed", response_model=List[Todo])
async def get_completed_todos():
    """Ottieni i todo completati (endpoint RESTful)"""
    return todo_manager.mcp_get_completed_todos()

@app.get("/mcp/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str):
    """Ottieni un todo specifico (endpoint RESTful)"""
    todo = todo_manager.mcp_get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo non trovato")
    return todo

@app.put("/mcp/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    """Aggiorna un todo (endpoint RESTful)"""
    updates = todo_update.dict(exclude_unset=True)
    updated_todo = todo_manager.mcp_update_todo(todo_id, updates)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo non trovato")
    return updated_todo

@app.delete("/mcp/todos/{todo_id}", response_model=Dict)
async def delete_todo(todo_id: str):
    """Elimina un todo (endpoint RESTful)"""
    deleted_todo = todo_manager.mcp_delete_todo(todo_id)
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="Todo non trovato")
    return {"message": f"Todo '{deleted_todo['title']}' eliminato con successo"}

@app.get("/mcp/stats", response_model=Dict)
async def get_stats():
    """Ottieni statistiche (endpoint RESTful)"""
    stats = todo_manager.mcp_get_stats()
    return stats

@app.post("/mcp/tools/create_todo", response_model=Todo)
async def create_todo_tool(todo: TodoCreate):
    """
    MCP Tool: Crea un nuovo todo item
    """
    new_todo = todo_manager.mcp_create_todo(todo.title, todo.description)
    return new_todo

@app.get("/mcp/tools/get_all_todos", response_model=List[Todo])
async def get_all_todos_tool():
    """
    MCP Tool: Ottiene tutti i todo items
    """
    return todo_manager.mcp_get_all_todos()

@app.post("/mcp/tools/get_todo_by_id", response_model=Todo)
async def get_todo_by_id_tool(todo_id: str):
    """
    MCP Tool: Ottiene un todo specifico per ID
    """
    todo = todo_manager.mcp_get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo con ID {todo_id} non trovato")
    return todo

@app.post("/mcp/tools/update_todo", response_model=Todo)
async def update_todo_tool(todo_id: str, todo_update: TodoUpdate):
    """
    MCP Tool: Aggiorna un todo esistente
    """
    updates = todo_update.dict(exclude_unset=True)
    updated_todo = todo_manager.mcp_update_todo(todo_id, updates)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail=f"Todo con ID {todo_id} non trovato")
    return updated_todo

@app.post("/mcp/tools/delete_todo", response_model=Dict)
async def delete_todo_tool(todo_id: str):
    """
    MCP Tool: Elimina un todo
    """
    deleted_todo = todo_manager.mcp_delete_todo(todo_id)
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail=f"Todo con ID {todo_id} non trovato")
    return {"message": f"Todo '{deleted_todo['title']}' eliminato con successo"}

@app.get("/mcp/tools/get_completed_todos", response_model=List[Todo])
async def get_completed_todos_tool():
    """
    MCP Tool: Ottiene tutti i todo completati
    """
    return todo_manager.mcp_get_completed_todos()

@app.get("/mcp/tools/get_pending_todos", response_model=List[Todo])
async def get_pending_todos_tool():
    """
    MCP Tool: Ottiene tutti i todo in sospeso
    """
    return todo_manager.mcp_get_pending_todos()

@app.post("/mcp/tools/clear_completed_todos", response_model=Dict)
async def clear_completed_todos_tool():
    """
    MCP Tool: Elimina tutti i todo completati
    """
    return todo_manager.mcp_clear_completed_todos()

# === ENDPOINT MCP RESOURCES ===

@app.get("/mcp/resources/todo_stats", response_model=TodoStats)
async def get_todo_stats_resource():
    """
    MCP Resource: Statistiche sui todo
    """
    return todo_manager.mcp_get_stats()

@app.get("/mcp/resources/todo_list", response_model=List[Todo])
async def get_todo_list_resource():
    """
    MCP Resource: Lista completa dei todo
    """
    return todo_manager.mcp_get_all_todos()

# === DISCOVERY ENDPOINTS AGGIORNATI ===

@app.get("/capabilities/discovery", response_model=Dict)
async def discovery():
    """
    Simula il processo di discovery delle capacità MCP aggiornato.
    """
    return {
        "tools": [
            "get_weather", 
            "get_weather_dynamic",
            "create_todo",
            "get_all_todos",
            "get_todo_by_id",
            "update_todo",
            "delete_todo",
            "get_completed_todos",
            "get_pending_todos",
            "clear_completed_todos"
        ],
        "resources": [
            "read_file",
            "todo_stats",
            "todo_list"
        ],
        "prompts": ["code_review"],
        "sampling": ["request_sampling"]
    }

@app.get("/mcp/tools", response_model=Dict)
async def get_mcp_tools():
    """
    Restituisce tutti gli strumenti MCP disponibili
    """
    # Combina strumenti meteo e todo
    weather_tools = {
        "tools": [
            {
                "name": "get_weather",
                "description": "Ottiene il meteo simulato per una posizione",
                "parameters": {
                    "location": {"type": "string", "description": "Nome della città"}
                }
            },
            {
                "name": "get_weather_dynamic",
                "description": "Ottiene dati meteo reali da OpenWeatherMap",
                "parameters": {
                    "location": {"type": "string", "description": "Nome della città"}
                }
            }
        ]
    }
    
    todo_tools = todo_manager.get_mcp_tools()
    
    # Combina i due set di strumenti
    all_tools = weather_tools["tools"] + todo_tools["tools"]
    
    return {"tools": all_tools}

@app.get("/mcp/resources", response_model=Dict)
async def get_mcp_resources():
    """
    Restituisce tutte le risorse MCP disponibili
    """
    file_resources = {
        "resources": [
            {
                "uri": "file://read",
                "description": "Legge il contenuto di un file",
                "mimeType": "text/plain"
            }
        ]
    }
    
    todo_resources = todo_manager.get_mcp_resources()
    
    # Combina le risorse
    all_resources = file_resources["resources"] + todo_resources["resources"]
    
    return {"resources": all_resources}

# === ENDPOINT PRINCIPALE ===

@app.get("/", response_model=Dict)
async def root():
    """
    Endpoint principale con informazioni complete sul server
    """
    return {
        "message": "FastAPI + MCP Server",
        "version": "1.0.0",
        "description": "Server con funzionalità MCP per meteo e todo list",
        "capabilities": {
            "weather_tools": [
                "POST /tools/get_weather",
                "POST /tools/get_weather_dynamic"
            ],
            "todo_tools": [
                "POST /tools/create_todo",
                "GET /tools/get_all_todos",
                "POST /tools/get_todo_by_id",
                "POST /tools/update_todo",
                "POST /tools/delete_todo",
                "GET /tools/get_completed_todos",
                "GET /tools/get_pending_todos",
                "POST /tools/clear_completed_todos"
            ],
            "resources": [
                "GET /resources/read_file",
                "GET /resources/todo_stats",
                "GET /resources/todo_list"
            ],
            "prompts": [
                "POST /prompts/code_review"
            ],
            "discovery": [
                "GET /capabilities/discovery",
                "GET /mcp/tools",
                "GET /mcp/resources"
            ]
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    print("Avvio del server FastAPI + MCP...")
    print("Documentazione disponibile su: http://localhost:8000/docs")
    print("API disponibile su: http://localhost:8000")
    print("Premi Ctrl+C per interrompere")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )