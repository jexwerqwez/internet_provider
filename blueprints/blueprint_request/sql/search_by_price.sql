SELECT * FROM product WHERE prod_price BETWEEN :min_price AND :max_price LIMIT :limit OFFSET :offset;
