# Таблицы для базы данных

### Работники

#### Создание:
```sql
CREATE TABLE `workers` (
  `worker_id` int NOT NULL AUTO_INCREMENT,
  `user_role` enum('admin','manager') NOT NULL,
  `surname` varchar(45) NOT NULL,
  `login` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`worker_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

#### Данные:
```sql
INSERT INTO workers (user_role, surname, login, password) VALUES
('admin', 'Иванов', 'ivanov_admin', 'admin123'),
('manager', 'Петров', 'petrov_manager', 'manager123'),
('admin', 'Сидоров', 'sidorov_worker', 'worker123'),
('manager', 'Кузнецова', 'kuznetsova_manager', 'manager456'),
('manager', 'Федоров', 'fedorov_worker', 'worker456');
```
### Пользователи
##### Создание:
``` sql
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `surname` varchar(20) NOT NULL,
  `bday` date NOT NULL,
  `address` varchar(45) NOT NULL,
  `phone_num` varchar(11) NOT NULL,
  `contract_date` date NOT NULL,
  `login` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `login_UNIQUE` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

#### Данные:
```sql
INSERT INTO `user` (surname, bday, address, phone_num, contract_date, login, password) VALUES
('Смирнов', '1985-03-25', 'ул. Ленина, д. 10', '89991234567', '2015-01-01', 'smirnov123', 'password123'),
('Кузнецова', '1990-07-14', 'пр. Мира, д. 20', '89997654321', '2018-05-10', 'kuznetsova456', 'password456'),
('Морозов', '1982-11-30', 'ул. Пушкина, д. 5', '89998887766', '2017-08-22', 'morozov789', 'password789'),
('Егорова', '1995-02-18', 'пр. Победы, д. 15', '89995554433', '2020-03-12', 'egorova112', 'password101'),
('Дмитриев', '1993-09-09', 'ул. Красная, д. 3', '89997778899', '2021-11-19', 'dmitriev334', 'password202'),
('Романова', '1990-05-25', 'ул. Советов, д. 7', '89991234580', '2020-06-10', 'romanova567', 'password303'),
('Чернов', '1987-10-14', 'пр. Октябрьский, д. 8', '89997654332', '2019-11-03', 'chernov879', 'password404'),
('Григорьева', '1992-03-22', 'ул. Лермонтова, д. 12', '89998887755', '2021-08-15', 'grigorieva112', 'password505'),
('Михайлова', '1995-07-30', 'ул. Крылова, д. 5', '89997778888', '2022-01-25', 'mikhaylova223', 'password606'),
('Захаров', '1989-12-05', 'пр. Шевченко, д. 3', '89995554411', '2023-04-19', 'zaharov334', 'password707');
```
### Валюты
Да, хранятся отдельной табличкой на случай если надо будет ввести новую валюту или изменить название или какие-то параметры старой, чтобы всё не слетело.ы
#### Создание:
```sql
CREATE TABLE `currency` (
  `currency_id` int NOT NULL AUTO_INCREMENT,
  `currency` varchar(3) NOT NULL,
  PRIMARY KEY (`currency_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
#### Данные:
```sql
INSERT INTO `currency` (currency) 
VALUES
('USD'), 
('EUR'), 
('RUB'), 
('JPY'), 
('CNY');
```

### Счета

1. Валюту счёта нельзя изменить
2. Нельзя перевести деньги на счёт с другой валютой.

#### Создание:
``` sql
CREATE TABLE `bill` (
  `bill_id` varchar(12) NOT NULL,
  `user_id` int NOT NULL,
  `currency` int NOT NULL,
  `amount` double NOT NULL,
  `last_change` datetime NOT NULL,
  PRIMARY KEY (`bill_id`),
  UNIQUE KEY `bill_id_UNIQUE` (`bill_id`),
  KEY `User_Bill_FK_idx` (`user_id`),
  KEY `Currency_Bill_FL_idx` (`currency`),
  CONSTRAINT `Currency_Bill_FL` FOREIGN KEY (`currency`) REFERENCES `currency` (`currency_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `User_Bill_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

#### Триггер для подсчёта bill_id:
``` sql
CREATE DEFINER=`root`@`localhost` TRIGGER `bill_BEFORE_INSERT` BEFORE INSERT ON `bill` FOR EACH ROW BEGIN
	DECLARE current_max VARCHAR(12);
    SELECT MAX(bill_id) INTO current_max FROM bill;
    IF current_max IS NULL
    THEN
		SET NEW.bill_id = '000000000001';
	ELSE
		SET NEW.bill_id = LPAD(CAST(CAST(current_max AS UNSIGNED) + 1 AS CHAR), 12, '0');
	END IF;
END
```
#### Данные:
```sql
INSERT INTO `bill` (user_id, currency, amount, last_change) VALUES
(1, 2, 1500.75, '2023-03-15 10:00:00'),
(2, 3, 2450.50, '2022-08-22 11:15:00'),
(3, 1, 3000.00, '2023-01-05 12:30:00'),
(4, 2, 1200.25, '2023-11-10 13:45:00'),
(5, 4, 750.90, '2023-04-18 14:00:00'),
(6, 2, 850.65, '2023-09-07 14:30:00'),
(7, 3, 500.40, '2023-06-12 15:00:00'),
(8, 1, 1800.00, '2023-02-25 15:30:00'),
(9, 4, 2200.30, '2023-10-02 16:00:00'),
(10, 3, 3200.10, '2023-07-17 16:30:00'),
(1, 3, 1300.80, '2022-12-01 17:00:00'),
(2, 2, 950.40, '2023-05-09 17:30:00'),
(3, 4, 1750.00, '2022-11-20 18:00:00'),
(4, 1, 600.50, '2022-03-14 18:30:00'),
(5, 1, 2200.00, '2023-08-30 19:00:00');
```


### Изменения в счетах

#### Создание:

```sql
CREATE TABLE `bill_history` (
  `bill_id` varchar(12) NOT NULL,
  `old_amount` double NOT NULL,
  `new_amount` double NOT NULL,
  `change_date` datetime NOT NULL,
  `reason` enum('deposit','withdraw','transfer') NOT NULL,
  KEY `Bill_History_FK_idx` (`bill_id`),
  CONSTRAINT `Bill_History_FK` FOREIGN KEY (`bill_id`) REFERENCES `bill` (`bill_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
#### Процедура ```transfer``` для создания записей при переводе:
(эта процедура влияет и на `bill_history` и на `bill_history_inner`)

```sql
CREATE DEFINER=`root`@`localhost` PROCEDURE `transfer`(
    IN sender_bill VARCHAR(12), 
    IN receiver_bill VARCHAR(12), 
    IN transfer_amount DOUBLE
)
BEGIN
    DECLARE sender_old_amount DOUBLE;
    DECLARE receiver_old_amount DOUBLE;
    DECLARE sender_new_amount DOUBLE;
    DECLARE receiver_new_amount DOUBLE;
    DECLARE exchange_rate FLOAT;
    DECLARE sender_currency INT;
    DECLARE receiver_currency INT;
    DECLARE sender_user INT;
    DECLARE receiver_user INT;

    -- Получение данных отправителя и получателя
    SELECT amount, currency_id, user_id 
    INTO sender_old_amount, sender_currency, sender_user 
    FROM bill 
    WHERE bill_id = sender_bill;

    SELECT amount, currency_id, user_id 
    INTO receiver_old_amount, receiver_currency, receiver_user 
    FROM bill 
    WHERE bill_id = receiver_bill;

    -- Проверка на достаточность средств
    IF sender_old_amount < transfer_amount THEN 
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Недостаточно средств';
    END IF;

    -- Проверка на одинаковую валюту у отправителя и получателя, если это разные пользователи
    IF sender_user != receiver_user AND sender_currency != receiver_currency THEN
        SIGNAL SQLSTATE '45002' SET MESSAGE_TEXT = 'Разные валюты у пользователей';
    END IF;

    -- Внутренний перевод (один пользователь)
    IF sender_user = receiver_user THEN
        IF sender_currency = receiver_currency THEN
            -- Одинаковая валюта
            SET sender_new_amount = sender_old_amount - transfer_amount;
            SET receiver_new_amount = receiver_old_amount + transfer_amount;
        ELSE
            -- Разная валюта: получение курса
            SELECT rate INTO exchange_rate 
            FROM exchange_rates 
            WHERE from_currency = sender_currency 
              AND to_currency = receiver_currency 
              AND rate_date = CURDATE();

            IF exchange_rate IS NULL THEN
                SIGNAL SQLSTATE '45001' SET MESSAGE_TEXT = 'Нет exchange_rate на текущую дату';
            END IF;

            SET sender_new_amount = sender_old_amount - transfer_amount;
            SET receiver_new_amount = receiver_old_amount + transfer_amount * exchange_rate;
        END IF;

        -- Запись в историю и обновление счетов
        INSERT INTO bill_inner_history (sender_bill, receiver_bill, sender_amount, current_rate, change_date)
        VALUES (sender_bill, receiver_bill, transfer_amount, COALESCE(exchange_rate, 1), NOW());

    ELSE
        -- Внешний перевод (разные пользователи)
        SET sender_new_amount = sender_old_amount - transfer_amount;
        SET receiver_new_amount = receiver_old_amount + transfer_amount;

        -- Запись в историю
        INSERT INTO bill_history (bill_id, old_amount, new_amount, change_date, reason)
        VALUES 
        (sender_bill, sender_old_amount, sender_new_amount, NOW(), 'transfer'),
        (receiver_bill, receiver_old_amount, receiver_new_amount, NOW(), 'transfer');
    END IF;

    -- Обновление балансов
    UPDATE bill SET amount = sender_new_amount WHERE bill_id = sender_bill;
    UPDATE bill SET amount = receiver_new_amount WHERE bill_id = receiver_bill;
END
```

### Внутренние изменения в счетах

#### Создание:

```sql
CREATE TABLE `bill_inner_history` (
  `sender_bill` varchar(12) NOT NULL,
  `receiver_bill` varchar(12) NOT NULL,
  `sender_amount` double NOT NULL,
  `current_rate` float NOT NULL,
  `change_date` datetime NOT NULL,
  PRIMARY KEY (`sender_bill`,`receiver_bill`,`change_date`),
  KEY `Receiver_Bill_FK_idx` (`receiver_bill`),
  CONSTRAINT `Receiver_Bill_FK` FOREIGN KEY (`receiver_bill`) REFERENCES `bill` (`bill_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `Sender_Bill_FK` FOREIGN KEY (`sender_bill`) REFERENCES `bill` (`bill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


### Внутренний курс банка

#### Создание:

```sql
CREATE TABLE `exchange_rates` (
  `from_currency` varchar(3) NOT NULL,
  `to_currency` varchar(3) NOT NULL,
  `rate` float NOT NULL,
  `rate_date` date NOT NULL,
  PRIMARY KEY (`from_currency`,`to_currency`,`rate_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

Обновляется через админскую панель во вкладке "Курс банка", своми руками ничего вводить не надо.


# Структура приложения
### Основное приложение
`app.py` - главный файл приложения, запускать его.<br>
`model_route.py` - моделлер для основного приложения, у каждого blueprint свой моделлер в папке.<br>
`access.py` - декораторы для разграничения доступа внутри сайта.<br>
1. `login_required` - требует логин
2. `role_required` - требует роли(списком)
Зачем передавать роли параметром, а не сделать json с правами доступа? 
3. Потому что надо, чтобы к разным функциям внутри blueprint имели доступ разные группы пользователей, а разбивать и так маленький blueprint на кучу файлов нет смысла.

### Страницы приложения
`templates` - папка со всеми html страницами на сайте.<br>
Все страницы являются "продолжением" страницы `layout.html`.<br>
Все макросы (маленькие функции, которые генерируют куски кода в зависимости от входного параметра) лежат в файле `macros.html`.<br>
Макросы уже импортируются вместе с `layout.html`, так как они подключаются уже там.<br>
По названиям +- понятно в каком blueprint какие страницы используются.

### Blueprint'ы
Название blueprint'a = название папки + `_bp`<br>
Пример: `auth_bp`.<br>
Все blueprint'ы подключаются вручную в главном файле приложения. <br>
У каждого blueprint'а есть свой моделлер - `model_route.py` - внутри его папки. 
В папке `sql` лежат шаблоны sql запросов, которые используются в blueprint'e.


### Другие папки

#### static
Статичные файлы, которые Flask берёт для генерации страниц. Таблица стилей `style.css` и картинки для оформления сайта

#### data
Там один файл, конфигурация базы данных для сайта

#### database
Инструменты для работы с базой данных, используются в моделлерах.


# FAQ

### Не запускается, так как не хватает библиотек
Изменить интерпритатор на тот, что идёт вместе с репозиторием

### `'cryptography' package not installed`
Не включен сервер mysql. Просто зайти в MySQL Workbench.