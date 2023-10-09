from fastapi import APIRouter, status, HTTPException, Request

from core.handlers.phone_address_handler import PhoneAddressHandler

phone_router = APIRouter()


@phone_router.get("/check_data", status_code=status.HTTP_200_OK)
async def check_data(phone: str):
    address = PhoneAddressHandler.get_data(phone)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return {
        "phone": phone,
        "address": address
    }


@phone_router.post("/write_data", status_code=status.HTTP_201_CREATED)
async def write_data_post(request: Request):
    json = await request.json()
    if any(key not in json for key in ["phone", "address"]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Couldn't find fields 'phone' or 'address'"
        )
    phone, address = json["phone"], json["address"]
    await PhoneAddressHandler.write_data(phone, address)


@phone_router.put("/write_data", status_code=status.HTTP_200_OK)
async def write_data_put(request: Request):
    json = await request.json()
    if any(key not in json for key in ["phone", "address"]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Couldn't find fields 'phone' or 'address'"
        )
    phone, address = json["phone"], json["address"]
    await PhoneAddressHandler.write_data(phone, address)
