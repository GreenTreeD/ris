SELECT `bill_id`, `currency`, `amount`, `last_change`
FROM `bill` JOIN `currency` USING (`currency_id`)
WHERE `user_id` = (SELECT `user_id` FROM `user` WHERE `login` = '$user_login')
ORDER BY `bill_id`;