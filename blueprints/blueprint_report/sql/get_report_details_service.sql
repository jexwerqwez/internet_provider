SELECT rd_id, service_name, on_count, off_count
FROM reportdetails_service_period_on_off
WHERE fk_report = :report_id;
