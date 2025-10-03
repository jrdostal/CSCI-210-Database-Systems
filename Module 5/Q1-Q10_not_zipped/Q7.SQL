--Q7.sql Delete the LINE entry you created for invoice 1009 and product '13-Q2/P2'
DELETE FROM LINE WHERE INV_NUMBER = '1009' AND P_CODE = '13-Q2/P2';