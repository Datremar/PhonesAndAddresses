from redis_db.redis_client import r_client


class PhoneAddressHandler:
    def __new__(cls, *args, **kwargs):
        return cls

    @staticmethod
    async def get_data(phone: str):
        return await r_client.get(name=phone)

    @staticmethod
    async def write_data(phone: str, address: str):
        await r_client.set(name=phone, value=address)
