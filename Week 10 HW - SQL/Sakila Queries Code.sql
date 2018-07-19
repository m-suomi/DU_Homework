-- Homework Week 10: SQL using sakila

USE sakila;

-- 1a. Display the first and last names of all actors from the table actor.
SELECT a.first_name, a.last_name 
FROM actor a;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. 
-- 	   Name the column Actor Name.
SELECT UPPER(CONCAT(a.first_name, ' ', a.last_name)) as 'Actor Name'
FROM actor a;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only
--     the first name, "Joe." What is one query would you use to obtain this information?
SELECT a.actor_id, a.first_name, a.last_name
FROM actor a
WHERE a.first_name='JOE';

-- 2b. Find all actors whose last name contain the letters GEN
SELECT a.actor_id, a.first_name, a.last_name
FROM actor a
WHERE a.last_name LIKE '%GEN%';

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name
--     and first name, in that order:
SELECT a.actor_id, a.first_name, a.last_name
FROM actor a
WHERE a.last_name LIKE '%LI%'
ORDER BY 3,2;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan,
--     Bangladesh, and China:
SELECT c.country_id, c.country
FROM country c
WHERE c.country IN ('Afghanistan', 'Bangladesh', 'China');

-- ???reorder middle column??? 3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint:
--     you will need to specify the data type.
ALTER TABLE actor
ADD middle_name VARCHAR(45);

SELECT a.actor_id, a.first_name, a.middle_name, a.last_name, a.last_update -- reorder columns appearance in output
FROM actor a;

-- 3b. You realize that some of these actors have tremendously long last names. Change the data type of
--     the middle_name column to blobs.
ALTER TABLE actor
MODIFY middle_name BLOB(20);

-- 3c. Now delete the middle_name column.
ALTER TABLE actor
DROP middle_name;

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT a.last_name, COUNT(*) as number_actors
FROM actor a
GROUP BY 1
ORDER BY 2 DESC;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that
-- are shared by at least two actors
SELECT a.last_name, COUNT(*) as number_actors
FROM actor a
GROUP BY 1
HAVING number_actors >= 2
ORDER BY 2 DESC;

-- 4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS, 
--     the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.
UPDATE actor
SET first_name='HARPO'
WHERE actor_id=172;
-- SELECT * from actor WHERE last_name='Williams'; -- see what current name is

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct
-- name after all! In a single query, if the first name of the actor is currently HARPO, change it to
-- GROUCHO. Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will
-- be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO,
-- HOWEVER! (Hint: update the record using a unique identifier.)

-- SELECT * from actor WHERE last_name='Williams'; -- see what current name is

UPDATE actor
	SET first_name = 
		CASE 
			WHEN first_name='HARPO' THEN 'GROUCHO'
            ELSE 'MUCHO GROUCHO'
		END
	WHERE actor_id=172;

-- SELECT * from actor WHERE last_name='Williams'; -- see what current name is


-- ???? 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
--     Hint: https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html
SHOW CREATE TABLE address;

'CREATE TABLE `address` (
  `address_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(50) NOT NULL,
  `address2` varchar(50) DEFAULT NULL,
  `district` varchar(20) NOT NULL,
  `city_id` smallint(5) unsigned NOT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `location` geometry NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`address_id`),
  KEY `idx_fk_city_id` (`city_id`),
  SPATIAL KEY `idx_location` (`location`),
  CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8'

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. 
--     Use the tables staff and address:
SELECT s.first_name, s.last_name, a.address, a.district, a.postal_code -- include district and postal_code to have full address info
FROM staff s -- seems weird there are only two staff in the staff table, but corresponds to the payment table too
JOIN address a ON s.address_id=a.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables 
--     staff and payment
SELECT s.first_name, s.last_name, SUM(p.amount) as 'Total $ Rung Up'
FROM staff s 
JOIN payment p ON s.staff_id=p.staff_id
GROUP BY 1, 2;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor
--     and film. Use inner join.
SELECT f.title, COUNT(*) as '# of Actors'    -- using DISTINCT is unnecessary, gets same result: COUNT(DISTINCT fa.actor_id)
FROM film f
JOIN film_actor fa ON f.film_id=fa.film_id -- INNER JOIN is the default
GROUP BY 1
ORDER BY 2 DESC;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT f.title, COUNT(*) as '# of Copies'
FROM film f
JOIN inventory i ON f.film_id=i.film_id
WHERE f.title='Hunchback Impossible'
GROUP BY 1; -- 6 copies of Hunchback Impossible in Inventory

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer.
--     List the customers alphabetically by last name:
SELECT c.first_name, c.last_name, SUM(p.amount)
FROM customer c
JOIN payment p ON c.customer_id=p.customer_id
GROUP BY 1, 2
ORDER BY 2;

-- ??why need subqueries?? 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended
--     consequence, films starting with the letters K and Q have also soared in popularity. Use 
--     subqueries to display the titles of movies starting with the letters K and Q whose language is
--     English.
SELECT f.title
FROM film f 
WHERE (f.title LIKE 'K%' OR f.title LIKE 'Q%')
AND f.language_id=1;  -- language_id=1 is English

-- ?? why need subqueries?? 7b. Use subqueries to display all actors who appear in the film Alone Trip.
SELECT a.first_name, a.last_name
FROM actor a
JOIN film_actor fa ON a.actor_id=fa.actor_id
JOIN film f ON fa.film_id=f.film_id
WHERE f.title='Alone Trip';

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names
--     and email addresses of all Canadian customers. Use joins to retrieve this information.
-- customer: has address_id, address: has city_id, city: has country_id, country_id: has country
SELECT c.first_name, c.last_name, c.email, co.country
FROM customer c
JOIN address a ON c.address_id=a.address_id
JOIN city ci ON a.city_id=ci.city_id
JOIN country co ON ci.country_id=co.country_id
WHERE co.country='Canada';

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a
--     promotion. Identify all movies categorized as family films.
-- category: has category_id=8 and name=Family; film_category: has film_id and category_id
SELECT f.title
FROM film f
JOIN film_category fcat ON f.film_id=fcat.film_id
JOIN category cat ON fcat.category_id=cat.category_id
WHERE cat.name='Family';

-- 7e. Display the most frequently rented movies in descending order.
-- film: has film_id, inventory: has film_id and inventory_id, rental: has inventory_id 
SELECT f.title, COUNT(*) as '# Times Rented'
FROM film f
JOIN inventory i ON f.film_id=i.film_id
JOIN rental r ON i.inventory_id=r.inventory_id
GROUP BY 1
ORDER BY 2 DESC;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
-- payment has customer_id and amount, customer has customer_id and store_id
SELECT c.store_id, SUM(p.amount) as 'Total Business ($)'
FROM payment p
JOIN customer c ON p.customer_id=c.customer_id
GROUP BY 1;

-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT s.store_id, ci.city, co.country
FROM store s
JOIN address a ON s.address_id=a.address_id
JOIN city ci ON a.city_id=ci.city_id
JOIN country co ON ci.country_id=co.country_id;

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may
--     need to use the following tables: category, film_category, inventory, payment, and rental.)
SELECT cat.name, SUM(p.amount) as 'Gross Revenue ($)'
FROM category cat
JOIN film_category fcat ON cat.category_id=fcat.category_id
JOIN inventory i ON fcat.film_id=i.film_id
JOIN rental r ON i.inventory_id=r.inventory_id
JOIN payment p ON r.rental_id=p.rental_id
GROUP BY 1
ORDER BY 2 DESC LIMIT 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five 
--     genres by gross revenue. Use the solution from the problem above to create a view. If you 
--     haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW `top_five_genres` AS
	SELECT cat.name, SUM(p.amount) as 'Gross Revenue ($)'
	FROM category cat
	JOIN film_category fcat ON cat.category_id=fcat.category_id
	JOIN inventory i ON fcat.film_id=i.film_id
	JOIN rental r ON i.inventory_id=r.inventory_id
	JOIN payment p ON r.rental_id=p.rental_id
	GROUP BY 1
	ORDER BY 2 DESC LIMIT 5;

-- 8b. How would you display the view that ytop_five_genresou created in 8a?
SELECT * FROM top_five_genres;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
DROP VIEW top_five_genres;