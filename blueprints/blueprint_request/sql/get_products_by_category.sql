SELECT prod_name, prod_price, prod_measure, prod_img
FROM product
WHERE prod_category = :category_name
AND (prod_price >= :price_from OR :price_from IS NULL)
AND (prod_price <= :price_to OR :price_to IS NULL)
LIMIT :limit OFFSET :offset;
