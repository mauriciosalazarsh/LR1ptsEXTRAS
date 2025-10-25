#!/usr/bin/env python3
"""
Módulo principal para ejecutar el backend como módulo Python
Uso: python -m backend
"""

from backend.app import app, init_parser, DEFAULT_GRAMMAR

if __name__ == '__main__':
    # Inicializar con gramática por defecto
    init_parser(DEFAULT_GRAMMAR)

    print("\n" + "="*70)
    print(" " * 15 + "BACKEND API - AUTOMATA LR(1)")
    print(" " * 10 + "Compiladores - UTEC - Puntos Extras")
    print("="*70)
    print("\n✅ Servidor API iniciado en: http://127.0.0.1:5001")
    print("🔧 Modo: API pura para frontend React")
    print("📍 Frontend React esperado en: http://localhost:5173")
    print("\nPresiona Ctrl+C para detener el servidor\n")

    app.run(debug=False, host='0.0.0.0', port=5001)
