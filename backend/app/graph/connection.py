"""Neo4j driver management.

Lazily creates a single shared driver. Read queries run through `run_read`,
which returns plain dicts so the service layer never touches driver objects.
"""

from __future__ import annotations

from typing import Any

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.config import settings

_driver = None


def get_driver():
    """Return the shared Neo4j driver, creating it on first use."""
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_username, settings.neo4j_password),
        )
    return _driver


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def is_available() -> bool:
    """True if the Neo4j server is reachable and authenticated."""
    try:
        get_driver().verify_connectivity()
        return True
    except (ServiceUnavailable, Neo4jError, OSError):
        return False


def run_read(cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Execute a read query and return records as dicts."""
    with get_driver().session() as session:
        result = session.run(cypher, params or {})
        return [record.data() for record in result]


def run_read_graph(
    cypher: str, params: dict[str, Any] | None = None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Execute a query returning paths/nodes/rels and serialize the graph.

    Returns (nodes, edges) shaped for a graph viewer (e.g. React Flow):
      nodes: [{id, label, name, properties}]
      edges: [{id, type, source, target}]
    """
    with get_driver().session() as session:
        result = session.run(cypher, params or {})
        records = list(result)  # stream records so the graph accumulates
        graph = result.graph()

        nodes = []
        for node in graph.nodes:
            props = dict(node)
            label = next(iter(node.labels), "Node")
            name = props.get("name") or props.get("customer_id") or label
            nodes.append(
                {
                    "id": node.element_id,
                    "label": label,
                    "name": name,
                    "properties": props,
                }
            )

        edges = [
            {
                "id": rel.element_id,
                "type": rel.type,
                "source": rel.start_node.element_id,
                "target": rel.end_node.element_id,
            }
            for rel in graph.relationships
        ]
        _ = records  # records already consumed to build the graph
        return nodes, edges
