#!/usr/bin/env python3
"""
Script di test per l'API FastAPI + MCP
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_api():
    """Testa tutte le funzionalità dell'API"""
    
    print("=== TEST API FASTAPI + MCP ===")
    print()
    
    # Test 1: Verifica che il server sia attivo
    print("1. Test connessione al server...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server attivo")
            print(f"   Risposta: {response.json()['message']}")
        else:
            print("❌ Server non risponde correttamente")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione: {e}")
        return
    
    print()
    
    # Test 2: Ottieni tutti i todo (dovrebbero esserci quelli di esempio)
    print("2. Test ottenimento di tutti i todo...")
    response = requests.get(f"{BASE_URL}/mcp/tools/get_all_todos")
    if response.status_code == 200:
        todos = response.json()
        print(f"✅ Trovati {len(todos)} todo")
        for todo in todos:
            print(f"   - {todo['title']}")
    else:
        print(f"❌ Errore: {response.status_code}")
    
    print()
    
    # Test 3: Crea un nuovo todo
    print("3. Test creazione nuovo todo...")
    new_todo = {
        "title": "Test API",
        "description": "Testare che l'API funzioni correttamente"
    }
    response = requests.post(f"{BASE_URL}/mcp/tools/create_todo", json=new_todo)
    if response.status_code == 200:
        created_todo = response.json()
        todo_id = created_todo['id']
        print(f"✅ Todo creato con ID: {todo_id}")
        print(f"   Titolo: {created_todo['title']}")
    else:
        print(f"❌ Errore nella creazione: {response.status_code}")
        return
    
    print()
    
    # Test 4: Aggiorna il todo appena creato
    print("4. Test aggiornamento todo...")
    update_data = {
        "completed": True,
        "description": "Test completato con successo!"
    }
    response = requests.post(f"{BASE_URL}/mcp/tools/update_todo?todo_id={todo_id}", json=update_data)
    if response.status_code == 200:
        updated_todo = response.json()
        print(f"✅ Todo aggiornato")
        print(f"   Completato: {updated_todo['completed']}")
        print(f"   Descrizione: {updated_todo['description']}")
    else:
        print(f"❌ Errore nell'aggiornamento: {response.status_code}")
    
    print()
    
    # Test 5: Ottieni todo completati
    print("5. Test ottenimento todo completati...")
    response = requests.get(f"{BASE_URL}/mcp/tools/get_completed_todos")
    if response.status_code == 200:
        completed_todos = response.json()
        print(f"✅ Trovati {len(completed_todos)} todo completati")
        for todo in completed_todos:
            print(f"   - {todo['title']}")
    else:
        print(f"❌ Errore: {response.status_code}")
    
    print()
    
    # Test 6: Ottieni statistiche
    print("6. Test statistiche...")
    response = requests.get(f"{BASE_URL}/mcp/resources/todo_stats")
    if response.status_code == 200:
        stats = response.json()
        print("✅ Statistiche ottenute:")
        print(f"   Totale: {stats['total_todos']}")
        print(f"   Completati: {stats['completed_todos']}")
        print(f"   In sospeso: {stats['pending_todos']}")
        print(f"   Tasso completamento: {stats['completion_rate']}")
    else:
        print(f"❌ Errore: {response.status_code}")
    
    print()
    
    # Test 7: Test endpoint MCP
    print("7. Test endpoint MCP...")
    response = requests.get(f"{BASE_URL}/mcp/tools")
    if response.status_code == 200:
        tools = response.json()
        print(f"✅ Trovati {len(tools['tools'])} strumenti MCP")
        for tool in tools['tools'][:3]:  # Mostra solo i primi 3
            print(f"   - {tool['name']}: {tool['description']}")
    else:
        print(f"❌ Errore: {response.status_code}")
    
    print()
    
    # Test 8: Elimina il todo di test
    print("8. Test eliminazione todo...")
    response = requests.post(f"{BASE_URL}/mcp/tools/delete_todo?todo_id={todo_id}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Errore nell'eliminazione: {response.status_code}")
    
    print()
    print("=== TEST COMPLETATO ===")

def show_curl_examples():
    """Mostra esempi di utilizzo con curl"""
    print("\n=== ESEMPI DI UTILIZZO CON CURL ===")
    print()
    
    examples = [
        ("Ottenere tutti i todo", "curl -X GET http://localhost:8000/todos"),
        ("Creare un nuovo todo", 'curl -X POST http://localhost:8000/todos -H "Content-Type: application/json" -d \'{"title": "Nuovo todo", "description": "Descrizione"}\''),
        ("Aggiornare un todo", 'curl -X PUT http://localhost:8000/todos/1 -H "Content-Type: application/json" -d \'{"completed": true}\''),
        ("Ottenere statistiche", "curl -X GET http://localhost:8000/stats"),
        ("Eliminare un todo", "curl -X DELETE http://localhost:8000/todos/1")
    ]
    
    for description, command in examples:
        print(f"{description}:")
        print(f"  {command}")
        print()

if __name__ == "__main__":
    print("TESTER API FASTAPI + MCP")
    print("=" * 30)
    
    # Prima mostra gli esempi
    show_curl_examples()
    
    # Poi esegui i test
    test_api()