SELECT bill_id, login, currency, amount, last_change
FROM bill
JOIN `user` USING (user_id)
JOIN currency USING (currency_id)
$detail
ORDER BY bill_id;