create_table_statement = 'CREATE TABLE master(username, master_password_hash, salt, encrypted_data, nonce)'

select_all_from_user_statement = 'SELECT * FROM master WHERE username=?'

update_data_statement = 'UPDATE master SET encrypted_data = ?, nonce = ? WHERE username=?'

insert_new_user_statement = 'INSERT INTO master VALUES(?, ?, ?, "", "")'
