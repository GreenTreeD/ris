SELECT `total_withdrawal`, `total_deposit` FROM
(SELECT
    COALESCE(SUM(`sender_amount`), 0) AS `total_withdrawal`,
    '$bill_id' AS `bill_id`
FROM
    `bill_inner_history`
WHERE
    `sender_bill` = '$bill_id' AND
    DATE(`change_date`) >= '$begin_date' AND
    DATE(`change_date`) <= '$end_date'
) AS `a`
JOIN
(SELECT
    COALESCE(SUM(`sender_amount` * `current_rate`), 0) AS `total_deposit`,
    '$bill_id' as `bill_id`
FROM
    `bill_inner_history`
WHERE
    `receiver_bill` = '$bill_id' AND
    DATE(`change_date`) >= '$begin_date' AND
    DATE(`change_date`) <= '$end_date'
)
AS `b`
USING(`bill_id`);