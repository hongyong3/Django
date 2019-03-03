## Django_Reset_DB

- DB 에 존재하는 모든 데이터 레코드를 삭제

  ```bash
  $ python manage.py sqlflush
  ```

- 특정 App 의 모든 데이터 레코드를 삭제

  ```bash
  $ python manage.py sqlflush <APP_NAME>
  ```

- 특정 App 의 모든 테이블을 삭제

  ```bash
  $ python manage.py migrate <APP_NAME> zero
  ```