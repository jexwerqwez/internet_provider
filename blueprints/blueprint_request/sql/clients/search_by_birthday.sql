select * from contract where year(birthday) = :year and month(birthday) = :month LIMIT :limit OFFSET :offset;
