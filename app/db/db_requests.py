from typing import Any, Optional, List, Iterable
import aiosqlite
import logging


class DB:
    tables = {}

    @classmethod
    async def create_table(
        cls,
        table_cls: Any,
        columns: str,
        table_cls_row: Optional[Any] = None
    ) -> None:

        """Creates a table and enters it into its internal "tables" dict

        Args:
            table_cls (Any): Table class
            columns (str): SQL-designed columns (just copy them from the SQL command)
            table_cls_row (Optional[Any]): The class in which the result of the table search will be returned to you. Defaults to None.

        Examples:

        Example with row class:
        >>> await DB.create_table(
                table_cls=Users,
                columns='''
                    id INT PRIMARY KEY NOT NULL,
                    username TEXT NOT NULL
                ''',
                table_cls_row=User
            )

        Example without row class:
        >>> await DB.create_table(
                table_cls=Statistics,
                columns='''
                    bot_users INT DEFAULT(0),
                    wallet_users INT DEFAULT(0)
                '''
            )
        """

        if table_cls_row:
            cls.tables.update({table_cls.__name__: table_cls_row})

        else:
            cls.tables.update({table_cls.__name__: None})

        await cls.execute(sql_request=f"""
            CREATE TABLE IF NOT EXISTS {table_cls.__name__} (
                {columns}
            )
        """)

        logging.info(f'Created table: {table_cls.__name__}')

    @classmethod
    async def execute(
        cls,
        sql_request: str,
        sql_args: Optional[List[Any]] = []
    ) -> Optional[Iterable]:

        """The method for executing the SQL command

        Args:
            sql_request (str): A string with an SQL command
            sql_args (Optional[List[Any]]): A list with arguments for the SQL command. Defaults to [].

        Returns:
            Optional[Iterable]: Returns the result of executing the command, or None
        """

        async with aiosqlite.connect('database.db') as db:
            if 'select' in sql_request.lower():
                async with db.execute(sql_request, sql_args) as cursor:
                    return await cursor.fetchall()

            else:
                await db.execute(sql_request, sql_args)

                await db.commit()

    @classmethod
    async def get(
        cls,
        table_cls: Any,
        sql_args: List[str],
        sql_values: List[Any]
    ) -> Optional[Any]:

        """Returns the found row

        Args:
            table_cls (Any): Table class
            sql_args (List[str]): Attributes for finding a row
            sql_values (List[Any]): Attribute values for finding row

        Returns:
            Optional[Any]: The found row, if not found then None
        """

        if table_cls.__name__ in cls.tables:
            results: Optional[Iterable[Any]] = await cls.execute(
                sql_request=f'SELECT * FROM {table_cls.__name__} WHERE ({",".join(sql_args)}) = ({"?," * (len(sql_args) - 1) + "?"});',  # noqa: E501
                sql_args=sql_values
            )

            logging.info(f'Get data: {sql_args} from table: {table_cls.__name__}')  # noqa: E501

            if results:
                if cls.tables[table_cls.__name__]:
                    return cls.tables[table_cls.__name__](*list(results)[0])

                else:
                    return table_cls(*list(results)[0])

            else:
                return None

        else:
            logging.error(f'Table "{table_cls.__name__}" not found.')

    @classmethod
    async def get_many(
        cls,
        table_cls: Any,
        sql_args: Optional[List[str]] = None,
        sql_values: Optional[List[Any]] = None
    ) -> Optional[Any]:

        """Returns the found rows

        Args:
            table_cls (Any): Table class
            sql_args (List[str]): Attributes for finding a row
            sql_values (List[Any]): Attribute values for finding row

        Returns:
            Optional[Any]: The list of found rows, if not found, the list will be empty
        """

        if table_cls.__name__ in cls.tables:
            sql_request = f'SELECT * FROM {table_cls.__name__}'

            if sql_args and sql_values:
                sql_request += f' WHERE ({",".join(sql_args)}) = ({"?," * (len(sql_args) - 1) + "?"});'  # noqa: E501

            results: Optional[Iterable[Any]] = await cls.execute(
                sql_request=sql_request,
                sql_args=sql_values
            )

            logging.info(f'Get data: {sql_args if sql_args else "all"} from table: {table_cls.__name__}')  # noqa: E501

            if results:
                if cls.tables[table_cls.__name__]:
                    rows: List[Any] = []

                    for result in results:
                        row_class = cls.tables[table_cls.__name__]
                        rows.append(row_class(*result))

                    return rows

                else:
                    return table_cls(*list(results)[0])

            else:
                return None

        else:
            logging.error(f'Table "{table_cls.__name__}" not found.')

    @classmethod
    async def add(
        cls,
        table_cls: Any,
        sql_args: List[str],
        sql_values: List[Any]
    ) -> None:

        """Method for adding a row to a table

        Args:
            table_cls (Any): Table class
            sql_args (List[str]): Attributes for finding a row
            sql_values (List[Any]): Attribute values for finding row
        """

        if table_cls.__name__ in cls.tables:
            await cls.execute(
                sql_request=f'INSERT or IGNORE INTO {table_cls.__name__} ({",".join(sql_args)}) VALUES ({"?," * (len(sql_args) - 1) + "?"});',  # noqa: E501
                sql_args=sql_values
            )

            logging.info(f'Insert data: {sql_args} into table: {table_cls.__name__}')  # noqa: E501

        else:
            logging.error(f'Table "{table_cls.__name__}" not found.')

    @classmethod
    async def remove(
        cls,
        table_cls: Any,
        sql_args: List[str],
        sql_values: List[Any]
    ) -> None:

        """Method for deleting a row from a table

        Args:
            table_cls (Any): Table class
            sql_args (List[str]): Attributes for finding a row
            sql_values (List[Any]): Attribute values for finding row
        """

        if table_cls.__name__ in cls.tables:
            await cls.execute(
                sql_request=f'DELETE FROM {table_cls.__name__} WHERE ({",".join(sql_args)}) = ({"?," * (len(sql_args) - 1) + "?"});',  # noqa: E501
                sql_args=sql_values
            )

            logging.info(f'Remove data: {sql_args} from table: {table_cls.__name__}')  # noqa: E501

        else:
            logging.error(f'Table "{table_cls.__name__}" not found.')

    @classmethod
    async def update(
        cls,
        table_cls: Any,
        need_to_update_values: List[str],
        sql_values: List[Any],
        where_sql_arg: str,
        sql_arg: Any
    ) -> None:

        """Replaces the attribute of the specified row with the desired value

        Args:
            table_cls (Any): Table class
            need_to_update_values (List[str]): Attributes that need to be updated
            sql_values (List[Any]): Values that will replace the original ones
            where_sql_arg (str): The name of the attribute to find the row by
            sql_arg (Any): The attribute for which you need to find a row
        """

        if table_cls.__name__ in cls.tables:
            set_part = ''

            for index, value in enumerate(need_to_update_values):
                if index == len(need_to_update_values)-1:
                    set_part += f'{value}=?'

                else:
                    set_part += f'{value}=?,'

            await cls.execute(
                sql_request=f'UPDATE {table_cls.__name__} SET {set_part} WHERE {where_sql_arg}=?',  # noqa: E501
                sql_args=sql_values + [sql_arg]
            )

            logging.info(f'Updated data: {need_to_update_values} in table: {table_cls.__name__}')  # noqa: E501

        else:
            logging.error(f'Table "{table_cls.__name__}" not found.')
