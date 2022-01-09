# Course final projects for database principles

## database design
### ER graph
![er](./er.jpg)

### detailed attributes  
1. Customer:  
- id
- name
- property
- discount rate
- connect person
- connect information
2. Car
- plate number
- car type(small, middle, large)
- color
- car property(sedan, SUV, coupe, pickup, truck)
3. Service agent
- id
- name
- connect information
- gender
4. Order
- id
- settlement method
- start repairing time
- expected finish time
- detailed description
- repair type
- repair property
- order time
5. Single item
- id
- name
- consuming time
- unit price
6. Repair list
- id
- time
7. Garageman
- id
- name
- connect information
- gender
- type of work
8. Parts
- id
- name
- price

***
### Question and answer(recording my thoughts):   
There may need optimization for the database design. For example, maybe I can organise all stuffs in a set.(2021-01-09 still need discuss): After thinking carefully, I think in this project, it is necessary to unite all stuffs in a set. There are serveral reasons, (1) stuffs are a group intuitively, we must store them into a set so that we can easily query for information (2) service agent and garageman have differences in salary caculation, work types, etc.  
**Solution**: create a table Stuff which only contains id, name, connect information, gender, type(0 service agent, 1 garageman), a table GaragemanSkill contains id and skills. When query for garageman, we only need to join GaragemanSkill, Stuff on id.