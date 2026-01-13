import asyncio
import yaml
import rich
from rich.table import Table
from rich.live import Live
from puresnmp import ObjectIdentifier as OID

from node import Node, Parameter_Node
#from requests import requestV1


#"../data/hostsMap.yaml"
def load_hostsMap(path: str) -> dict:
  try:
    with open(path, 'r', encoding='UTF-8') as file:
      data = yaml.safe_load(file)
      
    if not isinstance(data, dict):
      raise TypeError('При загрузке данных из конфига .yaml не был получен тип данных "dict"')
        
    return data
    
  except FileNotFoundError:
    print(f"Файл {path} не найден")
    return {}
  except yaml.YAMLError as e:
    print(f"Ошибка разбора YAML: {e}")
    return {}
  except TypeError as e:
    print(str(e))
    return {}
  



def convert_data_to_Nodes(data: dict) -> list[Node]:
  
  nodes = []

  for obj in data: 

    name = data.get(obj).get('name')
    ip = data.get(obj).get('ip')
    port = data.get(obj).get('port')
    community = data.get(obj).get('community_string')
  
    values = data.get(obj).get('values')

    parameters = []
    
    for value in values:
      name: data.get(obj).get('values').get(value).get('name')
      oid = data.get(obj).get('values').get(value).get('oid')
      max_value = data.get(obj).get('values').get(value).get('max_value')
      min_value = data.get(obj).get('values').get(value).get('min_value')
      target_value = data.get(obj).get('values').get(value).get('catch_value')

      parameter = Parameter_Node(name,oid, max_value, min_value, target_value)
      parameters.append(parameter)
    
    node = Node(name, ip, port, community, parameters)
    
    nodes.append(node)
    
  return nodes


  

nodes = [] # переделать в кортеж

path = '../data/hostsMap.yaml'

data = load_hostsMap(path)
nodes = convert_data_to_Nodes(data)

#отправка запросов к узлам
#for node in nodes:
#  ip = node.ip
#  port = node.port
#  community = node.community#

 # oids = []
 # for parameter in node.paraters:


  

#answer = asyncio.run(requestV1(ip, port, community, oids))

  
if __name__ == '__main__':

  table = Table()
  table.add_column("Имя")
  table.add_column("IP_Адрес/Порт")
  table.add_column("Параметр/Значение")

  with Live(table, refresh_per_second=2) as live:  # update 4 times a second to feel fluid
    couter = 0
    for node in nodes:
      table.add_row(node.name,
      node.ip + "/" + node.port,
      node.values[counter] + "/" + answer[counter] )
    time.sleep(0.4)


  



