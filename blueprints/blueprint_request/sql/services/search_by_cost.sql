SELECT * FROM all_services WHERE cost BETWEEN :min_cost AND :max_cost LIMIT :limit OFFSET :offset;
