SELECT `bill_id` FROM `bill` WHERE
`user_id` = (SELECT `user_id` FROM `user` WHERE `login` = '$receiver_login')
AND `currency_id` = (SELECT `currency_id` FROM `bill` WHERE `bill_id` = '$sender_bill');