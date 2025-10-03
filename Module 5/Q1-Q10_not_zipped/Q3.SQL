--Q3.sql Add a line item to the new invoice for product 13-Q2/P2 with quantity 3 and price 14.99
INSERT INTO LINE (INV_NUMBER, LINE_NUMBER, P_CODE, LINE_UNITS, LINE_PRICE) VALUES
('1009', '1', '13-Q2/P2', '3', '14.99');