SELECT `bill_history`.`bill_id`,
(`new_amount`-`old_amount`) AS `money`,
`currency`,
`change_date`,
`reason`,
`initiator`
FROM `bill_history` JOIN
(SELECT `bill_id`, `currency_id` FROM `bill` WHERE `user_id` =
(SELECT `user_id` FROM `user` WHERE `login` = '$user_login')
) AS `bill_t`
ON `bill_t`.`bill_id`=`bill_history`.`bill_id`
JOIN `currency` USING (`currency_id`)
ORDER BY `change_date` DESC $detail;