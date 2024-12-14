SELECT `login`, `bill_id`, `sum` FROM `user` JOIN
(SELECT `bill_id`, `user_id`, (`old_amount`-`new_amount`) AS `sum` FROM `bill`
JOIN `bill_history` USING (`bill_id`)
WHERE `change_date` = '$change_date'
AND NOT `bill_id` = $bill_id) AS `bill_t`
USING (`user_id`);