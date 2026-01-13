import asyncio
import warnings
from puresnmp import Client, ObjectIdentifier as OID, V2C, V1

warnings.simplefilter("ignore")

# client = Client("127.0.0.1", V2C("public"), port=1024)
# coro = client.multiget(
#      [OID('1.3.6.1.2.1.1.3.0'), OID('1.3.6.1.2.1.1.2.0')]
# )


# oids - это список вида: [OID(..), OID(..), OID(..), ...]
async def requestV2(ip, port_number, password_type, oids_str):

    oids = converter_listStringOIDs_to_listOIDs(oids_str)
    client = Client(ip, V2C(password_type), port=port_number)
    coro = client.multiget(oids)

    try:
        result = await asyncio.wait_for(coro, timeout=5.0)
        return result
    except asyncio.TimeoutError:
        print("Превышен лимит ожидания ответа")
        return None
    except Exception as e:
        print(f"Error request: {e}")
        return None


async def requestV1(ip, port_number, password_type, oids_str):

    oids = converter_listStringOIDs_to_listOIDs(oids_str)
    client = Client(ip, V1(password_type), port=port_number)
    coro = client.multiget(oids)

    try:
        result = await asyncio.wait_for(coro, timeout=5.0)
        return result
    except asyncio.TimeoutError:
        print("Превышен лимит ожидания ответа")
        return None
    except Exception as e:
        print(f"Error request: {e}")
        return None


def converter_listStringOIDs_to_listOIDs(oids_str: list[str]) -> list[OID]:
    oids = []

    for oid_str in oids_str:
        oid = OID(oid_str)
        oids.append(oid)

    return oids




if name == "__main__":
    # Определяем параметры
    ip = "127.0.0.1"
    port_number = 1024
    password_type = "public"  # community string
    oids = ['1.3.6.1.4.1.99999.1.1.0', '1.3.6.1.4.1.99999.1.2.0']

    result = asyncio.run(requestV1(ip, port_number, password_type, oids))
    print(result)

    if result:
        print(f"Тип результата: {type(result)}")  # <class 'tuple'>
        print(f"Длина результата: {len(result)}")  # 2

        # Работаем с результатом
        for var_bind in result:
            print(var_bind)

            #print(f"OID: {var_bind.oid}, Значение: {var_bind.value}")
            # Или так:
            #print(f"OID: {var_bind[0]}, Значение: {var_bind[1]}")