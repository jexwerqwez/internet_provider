select * from contract left join ( select balance_history_id ,
contract_number
from balance_history where month ( amendment ) = :month3 and
year ( amendment ) = :year3) march2020
using ( contract_number ) where balance_history_id is NULL LIMIT :limit OFFSET :offset