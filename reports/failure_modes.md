# Failure Modes (auto-generated)

Total failures: 24

## False positive (answered when should be NOT_FOUND)

Count: 1

- **q032** (doc_002_sla, ambiguous): expected='NOT_FOUND' | predicted='Sundays 01:00–03:00 UTC'

## Missed answer (returned NOT_FOUND)

Count: 23

- **q004** (doc_001_refund_policy, edge): expected='No, FINAL SALE promotional purchases are not refundable.' | predicted='NOT_FOUND'
- **q005** (doc_001_refund_policy, base): expected='5–10 business days.' | predicted='NOT_FOUND'
- **q008** (doc_002_sla, edge): expected='25% monthly credit.' | predicted='NOT_FOUND'
- **q009** (doc_002_sla, base): expected='Within 14 days.' | predicted='NOT_FOUND'
- **q013** (doc_003_leave_policy, base): expected='No, sick leave does not carry over.' | predicted='NOT_FOUND'
