"""Módulo utilitário para exportação de dados em formatos estruturados."""
import csv
import json
from io import StringIO
from typing import List, Dict, Any

def export_to_csv(data: List[Dict[str, Any]]) -> str:
    """Converte lista de dicionários para string formato CSV."""
    if not data:
        return ""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

def export_to_json(data: List[Dict[str, Any]]) -> str:
    """Converte lista de dicionários para string formato JSON estruturado."""
    return json.dumps(data, indent=4, default=str, ensure_ascii=False)