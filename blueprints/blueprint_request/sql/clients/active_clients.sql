create or replace view spenders ( contract_number , sum_of_changes )
as select contract_number , SUM( new_balance - old_balance )
from balance_history
join ( select contract_number , balance_history_id from
balance_history where
( month( amendment ) = :month2 and year( amendment ) = :year2) and
(( new_balance - old_balance ) < 0) )march2020 using
( contract_number ) group by contract_number ;
select * from contract join spenders using ( contract_number )
where sum_of_changes = ( select max( sum_of_changes ) from
spenders ) LIMIT :limit OFFSET :offset