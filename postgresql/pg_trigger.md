#  trigger


-- DTS增量同步报错
```
DTS-077100: Record Replicator error in table public.users. cause by [org.postgresql.util.PSQLException: 
ERROR: Version has changed 
Where: PL/pgSQL function update_version() line 7 at RAISE]
 About more information in [https://yq.aliyun.com/articles/508049].

这个DTS同步报错的原因是： 

DTS同步的源端 pg RDS 和 目标端 pg RDS 都有触发器，所以源端的数据同步的目标端后，触发器发生了改变，就产生错误了。

处理思路：
同步之前先在源端确认和查询触发器，确认之后，将目标端触发器禁用，然后进行DTS数据同步，同步完毕，在启用触发器即可。

```

查看触发器命令：

SELECT * FROM pg_trigger;

\dft

项目中需要对触发器进行批量禁止、启用操作，方法如下。
```
创建方法/函数/过程
/* Enable/disable all the triggers in database */
CREATE OR REPLACE FUNCTION fn_triggerall(DoEnable boolean) RETURNS integer AS 
$BODY$
DECLARE
mytables RECORD;
BEGIN
  FOR mytables IN SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%' 
  LOOP
    IF DoEnable THEN
      EXECUTE 'ALTER TABLE ' || mytables.relname || ' ENABLE TRIGGER ALL';
    ELSE
      EXECUTE 'ALTER TABLE ' || mytables.relname || ' DISABLE TRIGGER ALL';
    END IF;  
  END LOOP;

  RETURN 1;

END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE;


启用触发器
select fn_triggerall(true);

禁用触发器
select fn_triggerall(false);

如果，你想列举出特定表的触发器，语法如下：

runoobdb=# SELECT tgname FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname='users';

SELECT tgname FROM pg_trigger;

https://www.runoob.com/postgresql/postgresql-trigger.html

查看触发器   -- 这样查询，会包含一些 RI 开头的系统触发器
SELECT relname,tgname,tgenabled FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname IN 
(SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%');
```

查看触发器  -  系统触发器除外：
```
SELECT relname,tgname,tgenabled FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname IN 
(SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%')
AND NOT tgname LIKE 'RI_ConstraintTrigger_%';

```


禁用触发器：

```
SELECT 'ALTER TABLE '||relname||' DISABLE TRIGGER '||tgname||';' 
FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname IN 
(SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%')
AND NOT tgname LIKE 'RI_ConstraintTrigger_%';

```

启用触发器：

```
SELECT 'ALTER TABLE '||relname||' ENABLE TRIGGER '||tgname||';'
FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname IN 
(SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%')
AND NOT tgname LIKE 'RI_ConstraintTrigger_%';

```


实际操作举例

```
查看触发器  -  系统触发器除外：
SELECT relname,tgname,tgenabled FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname IN 
(SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%')
AND NOT tgname LIKE 'RI_ConstraintTrigger_%';


          relname           |                 tgname
----------------------------+-----------------------------------------
 payer_contact              | payer_contact_created_at
 payer_contact              | update_payer_contact_version
 award_issue_history        | campaign_award_issue_history_created_at
 award_issue_history        | update_award_issue_history_version
 pobo_role                  | pobo_role_create_trigger
 pobo_role                  | pobo_role_update_trigger
 account_owner              | account_owner_create_trigger
 account_owner              | account_owner_update_trigger
 users                      | update_users_version
 users                      | users_created_at
 role                       | role_created_at
 role                       | update_role_version
 campaign_award             | campaign_award_created_at
 campaign_award             | update_campaign_award_version
 user_primary_account       | user_primary_account_create_trigger
 user_primary_account       | user_primary_account_update_trigger
 access_control_list        | access_control_list_created_at
 access_control_list        | update_access_control_list_version
 account_draft              | account_draft_created_at
 account_draft              | update_account_draft_version
 account                    | account_created_at
 account                    | update_account_version
 currency_setting           | update_currency_setting_created_at
 currency_setting           | update_currency_setting_version
 campaign                   | campaign_created_at
 campaign                   | update_campaign_version
 beneficiary_contact        | beneficiary_contact_created_at
 beneficiary_contact        | update_beneficiary_contact_version
 user_preferences           | update_user_preferences_created_at
 user_preferences           | update_user_preferences_version
 account_authorization_list | authorization_created_at
 account_authorization_list | update_authorization_version
(32 rows)


禁用触发器：

SELECT 'ALTER TABLE '||relname||' DISABLE TRIGGER '||tgname||';'
FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname IN 
(SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%')
AND NOT tgname LIKE 'RI_ConstraintTrigger_%';


                                         ?column?
------------------------------------------------------------------------------------------
 ALTER TABLE payer_contact DISABLE TRIGGER payer_contact_created_at;
 ALTER TABLE payer_contact DISABLE TRIGGER update_payer_contact_version;
 ALTER TABLE award_issue_history DISABLE TRIGGER campaign_award_issue_history_created_at;
 ALTER TABLE award_issue_history DISABLE TRIGGER update_award_issue_history_version;
 ALTER TABLE pobo_role DISABLE TRIGGER pobo_role_create_trigger;
 ALTER TABLE pobo_role DISABLE TRIGGER pobo_role_update_trigger;
 ALTER TABLE account_owner DISABLE TRIGGER account_owner_create_trigger;
 ALTER TABLE account_owner DISABLE TRIGGER account_owner_update_trigger;
 ALTER TABLE users DISABLE TRIGGER update_users_version;
 ALTER TABLE users DISABLE TRIGGER users_created_at;
 ALTER TABLE role DISABLE TRIGGER role_created_at;
 ALTER TABLE role DISABLE TRIGGER update_role_version;
 ALTER TABLE campaign_award DISABLE TRIGGER campaign_award_created_at;
 ALTER TABLE campaign_award DISABLE TRIGGER update_campaign_award_version;
 ALTER TABLE user_primary_account DISABLE TRIGGER user_primary_account_create_trigger;
 ALTER TABLE user_primary_account DISABLE TRIGGER user_primary_account_update_trigger;
 ALTER TABLE access_control_list DISABLE TRIGGER access_control_list_created_at;
 ALTER TABLE access_control_list DISABLE TRIGGER update_access_control_list_version;
 ALTER TABLE account_draft DISABLE TRIGGER account_draft_created_at;
 ALTER TABLE account_draft DISABLE TRIGGER update_account_draft_version;
 ALTER TABLE account DISABLE TRIGGER account_created_at;
 ALTER TABLE account DISABLE TRIGGER update_account_version;
 ALTER TABLE currency_setting DISABLE TRIGGER update_currency_setting_created_at;
 ALTER TABLE currency_setting DISABLE TRIGGER update_currency_setting_version;
 ALTER TABLE campaign DISABLE TRIGGER campaign_created_at;
 ALTER TABLE campaign DISABLE TRIGGER update_campaign_version;
 ALTER TABLE beneficiary_contact DISABLE TRIGGER beneficiary_contact_created_at;
 ALTER TABLE beneficiary_contact DISABLE TRIGGER update_beneficiary_contact_version;
 ALTER TABLE user_preferences DISABLE TRIGGER update_user_preferences_created_at;
 ALTER TABLE user_preferences DISABLE TRIGGER update_user_preferences_version;
 ALTER TABLE account_authorization_list DISABLE TRIGGER authorization_created_at;
 ALTER TABLE account_authorization_list DISABLE TRIGGER update_authorization_version;
(32 rows)


启用触发器：
SELECT 'ALTER TABLE '||relname||' ENABLE TRIGGER '||tgname||';'
FROM pg_trigger, pg_class WHERE tgrelid=pg_class.oid AND relname IN 
(SELECT relname FROM pg_class WHERE relhastriggers is true AND NOT relname LIKE 'pg_%')
AND NOT tgname LIKE 'RI_ConstraintTrigger_%';


                                        ?column?
-----------------------------------------------------------------------------------------
 ALTER TABLE payer_contact ENABLE TRIGGER payer_contact_created_at;
 ALTER TABLE payer_contact ENABLE TRIGGER update_payer_contact_version;
 ALTER TABLE award_issue_history ENABLE TRIGGER campaign_award_issue_history_created_at;
 ALTER TABLE award_issue_history ENABLE TRIGGER update_award_issue_history_version;
 ALTER TABLE pobo_role ENABLE TRIGGER pobo_role_create_trigger;
 ALTER TABLE pobo_role ENABLE TRIGGER pobo_role_update_trigger;
 ALTER TABLE account_owner ENABLE TRIGGER account_owner_create_trigger;
 ALTER TABLE account_owner ENABLE TRIGGER account_owner_update_trigger;
 ALTER TABLE users ENABLE TRIGGER update_users_version;
 ALTER TABLE users ENABLE TRIGGER users_created_at;
 ALTER TABLE role ENABLE TRIGGER role_created_at;
 ALTER TABLE role ENABLE TRIGGER update_role_version;
 ALTER TABLE campaign_award ENABLE TRIGGER campaign_award_created_at;
 ALTER TABLE campaign_award ENABLE TRIGGER update_campaign_award_version;
 ALTER TABLE user_primary_account ENABLE TRIGGER user_primary_account_create_trigger;
 ALTER TABLE user_primary_account ENABLE TRIGGER user_primary_account_update_trigger;
 ALTER TABLE access_control_list ENABLE TRIGGER access_control_list_created_at;
 ALTER TABLE access_control_list ENABLE TRIGGER update_access_control_list_version;
 ALTER TABLE account_draft ENABLE TRIGGER account_draft_created_at;
 ALTER TABLE account_draft ENABLE TRIGGER update_account_draft_version;
 ALTER TABLE account ENABLE TRIGGER account_created_at;
 ALTER TABLE account ENABLE TRIGGER update_account_version;
 ALTER TABLE currency_setting ENABLE TRIGGER update_currency_setting_created_at;
 ALTER TABLE currency_setting ENABLE TRIGGER update_currency_setting_version;
 ALTER TABLE campaign ENABLE TRIGGER campaign_created_at;
 ALTER TABLE campaign ENABLE TRIGGER update_campaign_version;
 ALTER TABLE beneficiary_contact ENABLE TRIGGER beneficiary_contact_created_at;
 ALTER TABLE beneficiary_contact ENABLE TRIGGER update_beneficiary_contact_version;
 ALTER TABLE user_preferences ENABLE TRIGGER update_user_preferences_created_at;
 ALTER TABLE user_preferences ENABLE TRIGGER update_user_preferences_version;
 ALTER TABLE account_authorization_list ENABLE TRIGGER authorization_created_at;
 ALTER TABLE account_authorization_list ENABLE TRIGGER update_authorization_version;
(32 rows)

```




