--sqlite

select title, description, name
from film 
join language on film.language_id = language.language_id 
limit 300

select customer_id 
from rental 
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where film.title = 'MONTEZUMA COMMAND'

select first_name, last_name, sum(amount)
from customer 
join payment on customer.customer_id = payment.customer_id
group by customer.customer_id, first_name, last_name

select distinct actor.*
from actor 
join film_actor on actor.actor_id = film_actor.actor_id
join film on film_actor.film_id = film.film_id
where film.rental_rate = .99

select first_name, last_name, address, city, country, postal_code, phone 
from customer 
join address on customer.address_id = address.address_id 
join city on address.city_id = city.city_id 
join country on city.country_id = country.country_id 
where customer_id in (select customer_id from rental where return_date is null)

