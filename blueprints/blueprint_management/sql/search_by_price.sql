SELECT * FROM all_services WHERE cost BETWEEN :min_price AND :max_price LIMIT :limit OFFSET :offset;
