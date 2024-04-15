SELECT rd_id, contract_number, client_name, amount_spent
FROM reportdetails_client_spending
WHERE fk_report = :report_id;
