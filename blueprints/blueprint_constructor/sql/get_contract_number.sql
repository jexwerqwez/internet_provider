SELECT contract.contract_number FROM contract
JOIN external_user ON contract.contract_number = external_user.contract_number
WHERE external_user.id = :user_id
