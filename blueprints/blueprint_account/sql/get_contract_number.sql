SELECT contract.contract_number FROM contract
JOIN internal_user ON contract.contract_number = internal_user.contract_number
WHERE internal_user.id = :user_id
