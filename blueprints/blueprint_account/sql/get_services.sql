SELECT * FROM your_table_name
WHERE balance_history.contract_number = :contract_number AND (off_date IS NULL OR off_date > CURRENT_DATE)
