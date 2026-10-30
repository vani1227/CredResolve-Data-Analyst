
-- CREDRESOLVE COLLECTIONS RECOVERY ANALYTICS
-- SQL Analysis Queries
-- Database: SQLite

-- 1. Total accounts and outstanding amount
SELECT
    COUNT(*) AS total_accounts,
    ROUND(SUM(outstanding_amount), 2) AS total_outstanding
FROM accounts;


-- 2. Account distribution by risk segment
SELECT
    risk_segment,
    COUNT(*) AS total_accounts,
    ROUND(SUM(outstanding_amount), 2) AS outstanding_amount
FROM accounts
GROUP BY risk_segment
ORDER BY outstanding_amount DESC;


-- 3. Payment status distribution
SELECT
    payment_status,
    COUNT(*) AS total_payments,
    ROUND(SUM(amount), 2) AS total_amount
FROM payments
GROUP BY payment_status
ORDER BY total_payments DESC;


-- 4. Successful payment summary
SELECT
    COUNT(*) AS successful_transactions,
    ROUND(SUM(amount), 2) AS successful_payment_amount
FROM payments
WHERE UPPER(payment_status) = 'SUCCESS';


-- 5. Monthly successful payment trends
SELECT
    STRFTIME('%Y-%m', event_at) AS payment_month,
    COUNT(*) AS successful_transactions,
    ROUND(SUM(amount), 2) AS recovered_amount
FROM payments
WHERE UPPER(payment_status) = 'SUCCESS'
GROUP BY STRFTIME('%Y-%m', event_at)
ORDER BY payment_month;


-- 6. Payment method analysis
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM payments
WHERE UPPER(payment_status) = 'SUCCESS'
GROUP BY payment_method
ORDER BY total_amount DESC;


-- 7. Call outcome analysis
SELECT
    call_status,
    COUNT(*) AS total_calls,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM calls), 2
    ) AS call_percentage
FROM calls
GROUP BY call_status
ORDER BY total_calls DESC;


-- 8. Agent performance
SELECT
    agent_id,
    COUNT(*) AS total_calls,
    SUM(
        CASE WHEN UPPER(call_status) = 'ANSWERED'
        THEN 1 ELSE 0 END
    ) AS answered_calls,
    ROUND(
        SUM(
            CASE WHEN UPPER(call_status) = 'ANSWERED'
            THEN 1.0 ELSE 0 END
        ) * 100.0 / COUNT(*), 2
    ) AS answer_rate
FROM calls
GROUP BY agent_id
ORDER BY answer_rate DESC;


-- 9. Campaign performance
SELECT
    campaign_id,
    COUNT(*) AS total_calls,
    SUM(
        CASE WHEN UPPER(call_status) = 'ANSWERED'
        THEN 1 ELSE 0 END
    ) AS answered_calls,
    ROUND(
        SUM(
            CASE WHEN UPPER(call_status) = 'ANSWERED'
            THEN 1.0 ELSE 0 END
        ) * 100.0 / COUNT(*), 2
    ) AS answer_rate
FROM calls
GROUP BY campaign_id
ORDER BY answer_rate DESC;


-- 10. Missing values in account records
SELECT
    COUNT(*) AS total_accounts,
    SUM(CASE WHEN borrower_id IS NULL THEN 1 ELSE 0 END)
        AS missing_borrower_ids
FROM accounts;


-- 11. Duplicate payment IDs
SELECT
    payment_id,
    COUNT(*) AS record_count
FROM payments
GROUP BY payment_id
HAVING COUNT(*) > 1
ORDER BY record_count DESC;


-- 12. Account status distribution
SELECT
    status,
    COUNT(*) AS total_accounts
FROM accounts
GROUP BY status
ORDER BY total_accounts DESC;
