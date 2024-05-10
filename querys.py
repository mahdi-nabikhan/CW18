class QueryManager:

    def __init__(self, table_name, db_config, db_context_manager):
        self.table_name = table_name
        self.db_config = db_config
        self.result = None
        self.db_context_manager = db_context_manager

    def select(self, field_names: list, where_clause: str = None):
        select_query = f"""
        SELECT {",".join(field_names)}
        FROM {self.table_name}
        """
        if where_clause:
            """TODO: fix this"""
            select_query += f" WHERE {where_clause}"
        with self.db_context_manager(self.db_config) as cdbm:
            cdbm.cursor.execute(select_query)
            self.result = cdbm.cursor.fetchall()
        return self.result

    def update(self, set_dict: dict, where_clause: str = None):

        update_query = f"""
        UPDATE {self.table_name}
        SET {",".join(list(map(lambda x: f"{x[0]}='{x[1]}'" if isinstance(x[1], str) and not x[1].isdigit() else f"{x[0]}={x[1]}",
                               list(set_dict.items()))))}
                               
        """

        if where_clause:
            """TODO: fix this"""
            update_query += f" WHERE {where_clause}"
        with self.db_context_manager(self.db_config) as cdbm:
            cdbm.cursor.execute(update_query)

    def delete(self):
        pass

    def insert(self, inserts: dict, returning_field: str = None):

        insert_query = f""" 
        INSERT INTO {self.table_name} ({",".join(inserts.keys())}) 
        VALUES ({",".join(list(map(lambda x: f"'{x}'" if isinstance(x, str) and not x.isdigit() else str(x), inserts.values())))})
        
        """
        if returning_field:
            insert_query += f"RETURNING {returning_field}"

        with self.db_context_manager(self.db_config) as cdbm:
            cdbm.cursor.execute(insert_query)
            self.result = cdbm.cursor.fetchall()
            return self.result

    def join(
            self,
            field_names: list,
            table1: str,
            table2: str,
            table_on_field,
            table2_on_field,
            where_clause=None
    ):
        join_2_table = f"""
        SELECT {",".join(field_names)}
        FROM {table1} JOIN {table2} 
        ON {table1}.{table_on_field} = {table2}.{table2_on_field} """
        if where_clause:
            """TODO: fix this"""
            join_2_table += f" WHERE {where_clause}"
        with self.db_context_manager(self.db_config) as cdbm:
            cdbm.cursor.execute(join_2_table)
            self.result = cdbm.cursor.fetchall()
        return self.result
