# getProducts.py

import sys
import logging
import rds_config
import pymysql

# rds settings
rds_host = "rds-instance-endpoint"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    # MySQL Connection 연결
    conn = pymysql.connect(rds_host, user=name, password=password,
                           db=db_name,connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

def handler(event, context):

    item_count = 0
    """
    2. MySql 사용 절차
    Python에서 MySQL에 있는 데이타를 사용하는 일반적인 절차는 다음과 같다.
    
    1. PyMySql 모듈을 import 한다
    2. pymysql.connect() 메소드를 사용하여 MySQL에 Connect 한다. 호스트명, 로그인, 암호, 접속할 DB 등을 파라미터로 지정한다.
    3. DB 접속이 성공하면, Connection 객체로부터 cursor() 메서드를 호출하여 Cursor 객체를 가져온다. DB 커서는 Fetch 동작을 관리하는데 사용되는데, 만약 DB 자체가 커서를 지원하지 않으면, Python DB API에서 이 커서 동작을 Emulation 하게 된다.
    4. Cursor 객체의 execute() 메서드를 사용하여 SQL 문장을 DB 서버에 보낸다.
    5. SQL 쿼리의 경우 Cursor 객체의 fetchall(), fetchone(), fetchmany() 등의 메서드를 사용하여 데이타를 서버로부터 가져온 후, Fetch 된 데이타를 사용한다.
    6. 삽입, 갱신, 삭제 등의 DML(Data Manipulation Language) 문장을 실행하는 경우, INSERT/UPDATE/DELETE 후 Connection 객체의 commit() 메서드를 사용하여 데이타를 확정 갱신한다.
    7. Connection 객체의 close() 메서드를 사용하여 DB 연결을 닫는다.
    아래 예제들의 기본 샘플 데이타로 아래와 같은 customer 테이블이 있다고 가정하자.
    
    """

    # Connection 으로부터 Cursor 생성
    with conn.cursor() as cur:
        # SQL문 실행
        cur.execute("create table IF NOT EXISTS employee ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, "
                    "PRIMARY KEY (EmpID))")
        cur.execute('insert into employee (EmpID, Name) values(1, "Joe")')
        cur.execute('insert into employee (EmpID, Name) values(2, "Bob")')
        cur.execute('insert into employee (EmpID, Name) values(3, "Mary")')
        conn.commit()

        cur.execute("select * from employee")
        for row in cur:
            item_count += 1
            logger.info(row)
            print(row)

    return "Added #d items from RDS MySQL table" % (item_count)