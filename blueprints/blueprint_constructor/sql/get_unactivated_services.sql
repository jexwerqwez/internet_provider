SELECT all_services.all_services_id, all_services.name
FROM all_services
WHERE all_services.all_services_id NOT IN (
    SELECT service_on_off.all_services_id
    FROM service_on_off
    WHERE contract_number = :contract_number
    AND (off_date IS NULL OR off_date > CURRENT_DATE)
)