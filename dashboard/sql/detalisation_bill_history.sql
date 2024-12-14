SELECT
    SUM(CASE WHEN `reason` = 'deposit' THEN `new_amount` - `old_amount` ELSE 0 END) AS `total_deposit`,
    SUM(CASE WHEN `reason` = 'withdraw' THEN `old_amount` - `new_amount` ELSE 0 END) AS `total_withdraw`,
    SUM(CASE WHEN `reason` = 'transfer' AND `old_amount` > `new_amount` THEN `old_amount` - `new_amount` ELSE 0 END)
    AS `total_transfer_out`,
    SUM(CASE WHEN `reason` = 'transfer' AND `new_amount` > `old_amount` THEN `new_amount` - `old_amount` ELSE 0 END) AS `total_transfer_in`
FROM
    `bill_history`
WHERE
    `change_date` >= '$begin_date' AND
    `change_date` < '$end_date' AND
    `bill_id` = '$bill_id'
GROUP BY `bill_id`;
