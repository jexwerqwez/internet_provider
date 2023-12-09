SELECT * FROM contract WHERE current_balance BETWEEN :min_balance AND :max_balance LIMIT :limit OFFSET :offset;
