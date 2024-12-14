SELECT `total_withdrawal`, `total_deposit` FROM
(SELECT
    SUM(`sender_amount`) AS `total_withdrawal`,
    `sender_bill` AS `bill_id`
FROM
    `bill_inner_history`
WHERE
    `sender_bill` = '$bill_id' AND
    `change_date` >= '$begin_date' AND
    `change_date` < '$end_date'
) AS `a`
JOIN
(SELECT
    SUM(`sender_amount` * `current_rate`) AS `total_deposit`,
    `receiver_bill` as `bill_id`
FROM
    `bill_inner_history`
WHERE
    `receiver_bill` = '$bill_id' AND
    `change_date` >= '$begin_date' AND
    `change_date` < '$end_date'
)
AS `b`
USING(`bill_id`);