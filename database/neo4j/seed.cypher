// ==========================================================
// DefaultSense AI — Neo4j Seed Data (Phase 1)
// Mirrors the PostgreSQL customer/loan UUIDs so the graph and
// relational stores are linked. MERGE → idempotent re-runs.
// Ref: docs/04 §5, docs/11 §6
// ==========================================================

// ---------- Regions ----------
MERGE (:Region {name: 'West'});
MERGE (:Region {name: 'South'});
MERGE (:Region {name: 'North'});

// ---------- Branches ----------
MERGE (b1:Branch {branch_id: 'b0000000-0000-0000-0000-000000000001'}) SET b1.name = 'Mumbai Main',   b1.region = 'West';
MERGE (b2:Branch {branch_id: 'b0000000-0000-0000-0000-000000000002'}) SET b2.name = 'Chennai City',  b2.region = 'South';
MERGE (b3:Branch {branch_id: 'b0000000-0000-0000-0000-000000000003'}) SET b3.name = 'Delhi Central', b3.region = 'North';

// ---------- Industries (risk_level drives graph risk features) ----------
MERGE (i1:Industry {name: 'Information Technology'}) SET i1.risk_level = 'Low';
MERGE (i2:Industry {name: 'Retail'})                SET i2.risk_level = 'Moderate';
MERGE (i3:Industry {name: 'Manufacturing'})         SET i3.risk_level = 'High';
MERGE (i4:Industry {name: 'Agriculture'})           SET i4.risk_level = 'High';
MERGE (i5:Industry {name: 'Education'})              SET i5.risk_level = 'Low';

// ---------- Employers (risk_score 0-100) ----------
MERGE (e1:Employer {name: 'TechNova Pvt Ltd'})    SET e1.risk_score = 15;
MERGE (e2:Employer {name: 'Mehta Retail'})        SET e2.risk_score = 45;
MERGE (e3:Employer {name: 'Verma Manufacturing'}) SET e3.risk_score = 80;
MERGE (e4:Employer {name: 'GreenFields Agro'})    SET e4.risk_score = 70;
MERGE (e5:Employer {name: 'BrightFuture Academy'}) SET e5.risk_score = 20;

// ---------- Employer -> Industry ----------
MATCH (e:Employer {name:'TechNova Pvt Ltd'}),    (i:Industry {name:'Information Technology'}) MERGE (e)-[:BELONGS_TO]->(i);
MATCH (e:Employer {name:'Mehta Retail'}),        (i:Industry {name:'Retail'})                MERGE (e)-[:BELONGS_TO]->(i);
MATCH (e:Employer {name:'Verma Manufacturing'}), (i:Industry {name:'Manufacturing'})         MERGE (e)-[:BELONGS_TO]->(i);
MATCH (e:Employer {name:'GreenFields Agro'}),    (i:Industry {name:'Agriculture'})           MERGE (e)-[:BELONGS_TO]->(i);
MATCH (e:Employer {name:'BrightFuture Academy'}),(i:Industry {name:'Education'})             MERGE (e)-[:BELONGS_TO]->(i);

// ---------- Guarantors ----------
MERGE (g1:Guarantor {guarantor_id: 'g0000000-0000-0000-0000-000000000001'}) SET g1.name = 'Suresh Sharma';
MERGE (g2:Guarantor {guarantor_id: 'g0000000-0000-0000-0000-000000000002'}) SET g2.name = 'Deepak Verma';

// ---------- Customers (same UUIDs as PostgreSQL) ----------
MERGE (c1:Customer {customer_id: 'c0000000-0000-0000-0000-000000000001'}) SET c1.name = 'Priya Sharma', c1.credit_score = 810;
MERGE (c2:Customer {customer_id: 'c0000000-0000-0000-0000-000000000002'}) SET c2.name = 'Arjun Mehta',  c2.credit_score = 690;
MERGE (c3:Customer {customer_id: 'c0000000-0000-0000-0000-000000000003'}) SET c3.name = 'Kavya Nair',   c3.credit_score = 640;
MERGE (c4:Customer {customer_id: 'c0000000-0000-0000-0000-000000000004'}) SET c4.name = 'Rohit Verma',  c4.credit_score = 600;
MERGE (c5:Customer {customer_id: 'c0000000-0000-0000-0000-000000000005'}) SET c5.name = 'Sunita Devi',  c5.credit_score = 560;
MERGE (c6:Customer {customer_id: 'c0000000-0000-0000-0000-000000000006'}) SET c6.name = 'Imran Khan',   c6.credit_score = 520;

// ---------- Loans (same UUIDs as PostgreSQL) ----------
MERGE (l1:Loan {loan_id: '10000000-0000-0000-0000-000000000001'}) SET l1.loan_type = 'Home',        l1.status = 'Active';
MERGE (l2:Loan {loan_id: '10000000-0000-0000-0000-000000000002'}) SET l2.loan_type = 'Personal',    l2.status = 'Active';
MERGE (l3:Loan {loan_id: '10000000-0000-0000-0000-000000000003'}) SET l3.loan_type = 'Education',   l3.status = 'Active';
MERGE (l4:Loan {loan_id: '10000000-0000-0000-0000-000000000004'}) SET l4.loan_type = 'MSME',        l4.status = 'Overdue';
MERGE (l5:Loan {loan_id: '10000000-0000-0000-0000-000000000005'}) SET l5.loan_type = 'Agriculture', l5.status = 'Overdue';
MERGE (l6:Loan {loan_id: '10000000-0000-0000-0000-000000000006'}) SET l6.loan_type = 'Personal',    l6.status = 'Defaulted';

// ---------- Customer -[:HAS_LOAN]-> Loan ----------
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000001'}), (l:Loan {loan_id:'10000000-0000-0000-0000-000000000001'}) MERGE (c)-[:HAS_LOAN]->(l);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000002'}), (l:Loan {loan_id:'10000000-0000-0000-0000-000000000002'}) MERGE (c)-[:HAS_LOAN]->(l);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000003'}), (l:Loan {loan_id:'10000000-0000-0000-0000-000000000003'}) MERGE (c)-[:HAS_LOAN]->(l);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000004'}), (l:Loan {loan_id:'10000000-0000-0000-0000-000000000004'}) MERGE (c)-[:HAS_LOAN]->(l);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000005'}), (l:Loan {loan_id:'10000000-0000-0000-0000-000000000005'}) MERGE (c)-[:HAS_LOAN]->(l);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000006'}), (l:Loan {loan_id:'10000000-0000-0000-0000-000000000006'}) MERGE (c)-[:HAS_LOAN]->(l);

// ---------- Customer -[:WORKS_FOR]-> Employer ----------
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000001'}), (e:Employer {name:'TechNova Pvt Ltd'})    MERGE (c)-[:WORKS_FOR]->(e);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000002'}), (e:Employer {name:'Mehta Retail'})        MERGE (c)-[:WORKS_FOR]->(e);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000004'}), (e:Employer {name:'Verma Manufacturing'}) MERGE (c)-[:WORKS_FOR]->(e);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000005'}), (e:Employer {name:'GreenFields Agro'})    MERGE (c)-[:WORKS_FOR]->(e);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000006'}), (e:Employer {name:'BrightFuture Academy'}) MERGE (c)-[:WORKS_FOR]->(e);

// ---------- Customer -[:GUARANTEED_BY]-> Guarantor (shared guarantor = connected risk) ----------
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000004'}), (g:Guarantor {guarantor_id:'g0000000-0000-0000-0000-000000000002'}) MERGE (c)-[:GUARANTEED_BY]->(g);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000006'}), (g:Guarantor {guarantor_id:'g0000000-0000-0000-0000-000000000002'}) MERGE (c)-[:GUARANTEED_BY]->(g);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000001'}), (g:Guarantor {guarantor_id:'g0000000-0000-0000-0000-000000000001'}) MERGE (c)-[:GUARANTEED_BY]->(g);

// ---------- Customer -[:LOCATED_IN]-> Region ----------
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000001'}), (r:Region {name:'West'})  MERGE (c)-[:LOCATED_IN]->(r);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000002'}), (r:Region {name:'South'}) MERGE (c)-[:LOCATED_IN]->(r);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000003'}), (r:Region {name:'South'}) MERGE (c)-[:LOCATED_IN]->(r);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000004'}), (r:Region {name:'North'}) MERGE (c)-[:LOCATED_IN]->(r);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000005'}), (r:Region {name:'North'}) MERGE (c)-[:LOCATED_IN]->(r);
MATCH (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000006'}), (r:Region {name:'West'})  MERGE (c)-[:LOCATED_IN]->(r);

// ---------- Branch -[:SERVES]-> Customer ----------
MATCH (b:Branch {branch_id:'b0000000-0000-0000-0000-000000000001'}), (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000001'}) MERGE (b)-[:SERVES]->(c);
MATCH (b:Branch {branch_id:'b0000000-0000-0000-0000-000000000002'}), (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000002'}) MERGE (b)-[:SERVES]->(c);
MATCH (b:Branch {branch_id:'b0000000-0000-0000-0000-000000000002'}), (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000003'}) MERGE (b)-[:SERVES]->(c);
MATCH (b:Branch {branch_id:'b0000000-0000-0000-0000-000000000003'}), (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000004'}) MERGE (b)-[:SERVES]->(c);
MATCH (b:Branch {branch_id:'b0000000-0000-0000-0000-000000000003'}), (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000005'}) MERGE (b)-[:SERVES]->(c);
MATCH (b:Branch {branch_id:'b0000000-0000-0000-0000-000000000001'}), (c:Customer {customer_id:'c0000000-0000-0000-0000-000000000006'}) MERGE (b)-[:SERVES]->(c);

// ---------- Economic Event -> Industry (AFFECTED_BY) ----------
MERGE (ev:EconomicEvent {event_id: 'ev000000-0000-0000-0000-000000000001'})
  SET ev.name = 'Raw Material Price Surge 2024', ev.impact = 'Negative';
MATCH (i:Industry {name:'Manufacturing'}), (ev:EconomicEvent {event_id:'ev000000-0000-0000-0000-000000000001'}) MERGE (i)-[:AFFECTED_BY]->(ev);
MATCH (i:Industry {name:'Agriculture'}),   (ev:EconomicEvent {event_id:'ev000000-0000-0000-0000-000000000001'}) MERGE (i)-[:AFFECTED_BY]->(ev);

// ---------- Connected borrowers (RELATED_TO via shared guarantor) ----------
MATCH (c4:Customer {customer_id:'c0000000-0000-0000-0000-000000000004'}), (c6:Customer {customer_id:'c0000000-0000-0000-0000-000000000006'})
MERGE (c4)-[:RELATED_TO {reason:'shared_guarantor'}]->(c6);
