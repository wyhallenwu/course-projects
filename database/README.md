# Course final projects for database principles

## database design
### ER graph
![er](./er.jpg)

### detailed attributes  
1. Customer:  
- customer_id int(5)
- name nvarchar(20)
- property int(1)
- discount rate float
- phone nvarchar(11)
2. Company
- customer_id int(5)
- company_name nvarchar(20)
- company_phone nvarchar(11)
3. Car
- customer_id int(5)
- plate_number nvarchar(10)
- car_type(small, middle, large) int(1)
- color nvarchar(5)
- car_property(sedan, SUV, coupe, pickup, truck) nvarchar(10)
4. Service agent
- agent_id int(5)
- name nvarchar(10)
- phone nvarchar(11)
- gender boolen
5. Contract
- contract_id int(10)
- settlement method int(1)
- start_repairing_time date
- expected_finish_time date
- description text
- repair_type 
- repair_property
- contract_time datetime
6. Commodity
- commodity_id int(5)
- name nvarchar(20)
- price float
7. Repair list
- id
- time
8. Garageman
- id
- name
- connect information
- gender
- type of work 
9. Parts
- id
- name
- price

***
### Question and answer(recording my thoughts):   
There may need optimization for the database design. For example, maybe I can organise all stuffs in a set.(2021-01-09 still need discuss): After thinking carefully, I think in this project, it is necessary to unite all stuffs in a set. There are serveral reasons, (1) stuffs are a group intuitively, we must store them into a set so that we can easily query for information (2) service agent and garageman have differences in salary caculation, work types, etc.  
**Solution**: create a table Stuff which only contains id, name, connect information, gender, type(0 service agent, 1 garageman), a table GaragemanSkill contains id and skills. When query for garageman, we only need to join GaragemanSkill, Stuff on id.