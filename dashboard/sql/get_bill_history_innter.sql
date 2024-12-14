SELECT `sender_bill`, `receiver_bill`, `sender_amount`, `currency`, `change_date` FROM
`bill_inner_history` JOIN
(SELECT `bill_id`, `currency` FROM `bill` JOIN `currency` USING (`currency_id`) WHERE `user_id` = $user_id) AS `bill_temp`
ON `bill_temp`.`bill_id` = `bill_inner_history`.`sender_bill`
ORDER BY `change_date` $detail;