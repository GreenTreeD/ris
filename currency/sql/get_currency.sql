SELECT `currency`, `rate` FROM `exchange_rates` JOIN `currency` ON `exchange_rates`.`from_currency` = `currency`.`currency_id`
WHERE `to_currency` = (SELECT `currency_id` FROM `currency` WHERE `currency` = '$to_currency')
AND `rate_date` = '$today';