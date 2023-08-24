use super_store;

# Changing tha datatypes to varchar

ALTER TABLE orders
MODIFY COLUMN `Order ID` VARCHAR(20),
MODIFY COLUMN `ship mode` VARCHAR(20),
MODIFY COLUMN `customer ID` VARCHAR(20),
MODIFY COLUMN `customer name` VARCHAR(50),
MODIFY COLUMN `segment` VARCHAR(20),
MODIFY COLUMN `country` VARCHAR(20),
MODIFY COLUMN `city` VARCHAR(20),
MODIFY COLUMN `state` VARCHAR(20),
MODIFY COLUMN `region` VARCHAR(20),
MODIFY COLUMN `product ID` VARCHAR(20),
MODIFY COLUMN `category` VARCHAR(20),
MODIFY COLUMN `sub-category` VARCHAR(20),
MODIFY COLUMN `product name` VARCHAR(255);

# adding primary key to orders table
ALTER TABLE orders
ADD constraint PK_ORDERS primary key(`order id`,`customer name`,`product id`,`row id`);

# changing the data types for both persons and returns tables

ALTER TABLE persons
MODIFY person VARCHAR(50);

ALTER TABLE persons
MODIFY region VARCHAR(50);

ALTER TABLE returns
MODIFY returned VARCHAR(20);

ALTER TABLE returns
MODIFY `order id` VARCHAR(20);

# creating indexes for both columns to use as foreign keys

ALTER TABLE orders
ADD INDEX idx_customer_name (`customer name`);

ALTER TABLE persons
ADD FOREIGN KEY (person) REFERENCES orders(`customer name`);

ALTER TABLE orders
ADD INDEX idx_order_id (`order id`);

ALTER TABLE returns 
ADD FOREIGN KEY (`order id`) REFERENCES orders(`order id`);

# creating a table by joining 3 tables

CREATE TABLE super_store_data
SELECT o.*,p.person,r.returned
FROM orders o
LEFT JOIN persons p
ON o.`customer name` = p.person
LEFT JOIN returns r
ON o.`order id` = r.`order id`;

# Query 1
# city wise sales and profit
SELECT city, SUM(sales) `total sales`, SUM(profit) `total profit`
FROM super_store_data
GROUP BY city 
ORDER BY `total profit` DESC;

# Query 2
# segment wise max values
SELECT segment, MAX(sales) `max sales`, MAX(discount) `max discount`, MAX(profit) `max profit`
FROM super_store_data
GROUP BY segment 
ORDER BY `max profit` DESC;

# Query 3
# top 3 sales of each city
WITH CTE AS
		(SELECT *, dense_rank() OVER(PARTITION BY city ORDER BY sales DESC) AS r
		FROM orders)
SELECT city,sales
FROM CTE
WHERE r<4
order by city;


# Creating a stored procedure

DELIMITER $ 

CREATE PROCEDURE tasks()
BEGIN
	# city wise sales and profit
	SELECT city, SUM(sales) `total sales`, SUM(profit) `total profit`
	FROM super_store_data
	GROUP BY city 
	ORDER BY `total profit` DESC;

	# segment wise max values
	SELECT segment, MAX(sales) `max sales`, MAX(discount) `max discount`, MAX(profit) `max profit`
	FROM super_store_data
	GROUP BY segment 
	ORDER BY `max profit` DESC;
	
    # top 3 sales of each city
	WITH CTE AS
			(SELECT *, dense_rank() OVER(PARTITION BY city ORDER BY sales DESC) AS r
			FROM orders)
	SELECT city,sales
	FROM CTE
	WHERE r<4
	order by city;
END $

DELIMITER ;

CALL tasks();
