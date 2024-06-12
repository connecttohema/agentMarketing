SELECT DISTINCT v.FirstName, v.LastName
FROM vendor v
WHERE v.DatePurchased >= date('now', '-6 months');