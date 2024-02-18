import mysql.connector
import requests


class ServerPlan:
    def __init__(self, dbhost=None,dbuser=None,dbpassword=None,dbdatabase=None,sql_query=None, url=None):
        self.host = dbhost
        self.user = dbuser
        self.password = dbpassword
        self.database = dbdatabase
        
        self.connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )

        if sql_query is None:
            self.sql_query = (
                "SELECT project_name_info, alias, ocserver_info, rds_info FROM wosapp_server_result "
                "WHERE switch_status = '0' AND (rds_info = 'available' OR ocserver_info = 'RUNNING')"
            )
        else:
            self.sql_query = sql_query
        if url is None:
            self.url = "https://open.feishu.cn/open-apis/bot/v2/hook/39ee"
        else:
            self.url = url

    def serverplan(self):
        cursor = self.connection.cursor()
        cursor.execute(self.sql_query)
        results = cursor.fetchall()
        message = "服务未关闭的项目:\n"
        i = 0
        for row in results:
            i = i + 1
            project_name_info, alias, ocserver_info, rds_info = row
            message += f"{i}、{project_name_info}\t\t{alias}\n"
        cursor.close()
        self.connection.close()
        headers = {"Content-Type": "application/json"}
        data = {"msg_type": "text", "content": {"text": message}}
        response = requests.post(self.url, json=data, headers=headers)
        print(response.text)
        return response.text

