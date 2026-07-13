"""Cypher queries for the Knowledge Graph."""

# Customer neighborhood to depth 2 (customer → employer → industry → event, etc.)
CUSTOMER_SUBGRAPH = """
MATCH path = (c:Customer {customer_id: $customer_id})-[*1..2]-(m)
RETURN path
"""

# Whether a customer exists in the graph.
CUSTOMER_EXISTS = """
MATCH (c:Customer {customer_id: $customer_id})
RETURN c.customer_id AS customer_id, c.name AS name
"""

# Relationship risk factors for a customer.
CUSTOMER_RISK = """
MATCH (c:Customer {customer_id: $customer_id})
OPTIONAL MATCH (c)-[:WORKS_FOR]->(e:Employer)
OPTIONAL MATCH (e)-[:BELONGS_TO]->(i:Industry)
OPTIONAL MATCH (i)-[:AFFECTED_BY]->(ev:EconomicEvent)
OPTIONAL MATCH (c)-[:LOCATED_IN]->(r:Region)
OPTIONAL MATCH (c)-[:GUARANTEED_BY]->(g:Guarantor)<-[:GUARANTEED_BY]-(other:Customer)
OPTIONAL MATCH (other)-[:HAS_LOAN]->(ol:Loan)
  WHERE ol.status IN ['Defaulted', 'Overdue']
RETURN
  c.name                       AS customer,
  e.name                       AS employer,
  e.risk_score                 AS employer_risk,
  i.name                       AS industry,
  i.risk_level                 AS industry_risk,
  r.name                       AS region,
  collect(DISTINCT ev.name)    AS economic_events,
  collect(DISTINCT other.name) AS connected_borrowers,
  collect(DISTINCT CASE WHEN ol IS NOT NULL THEN other.name END) AS connected_defaulters
"""

# Search nodes by a name/id fragment, optionally filtered by label.
SEARCH_NODES = """
MATCH (n)
WHERE (n.name IS NOT NULL AND toLower(n.name) CONTAINS toLower($q))
   OR (n.customer_id IS NOT NULL AND toLower(n.customer_id) CONTAINS toLower($q))
RETURN labels(n)[0] AS label,
       coalesce(n.name, n.customer_id) AS name,
       properties(n) AS properties
LIMIT $limit
"""
