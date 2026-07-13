// ==========================================================
// DefaultSense AI — Neo4j verification (Phase 1)
// Node counts by label, relationship counts by type, and a
// risk-propagation query proving the graph is wired correctly.
// ==========================================================

// Node counts by label
MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count ORDER BY label;

// Relationship counts by type
MATCH ()-[r]->() RETURN type(r) AS relationship, count(*) AS count ORDER BY relationship;

// Risk propagation: customers whose employer's industry is High risk
MATCH (c:Customer)-[:WORKS_FOR]->(e:Employer)-[:BELONGS_TO]->(i:Industry)
WHERE i.risk_level = 'High'
RETURN c.name AS customer, e.name AS employer, e.risk_score AS employer_risk, i.name AS industry
ORDER BY employer_risk DESC;

// Connected-borrower risk: borrowers sharing a guarantor
MATCH (c1:Customer)-[:GUARANTEED_BY]->(g:Guarantor)<-[:GUARANTEED_BY]-(c2:Customer)
WHERE c1.customer_id < c2.customer_id
RETURN g.name AS guarantor, c1.name AS borrower_a, c2.name AS borrower_b;
