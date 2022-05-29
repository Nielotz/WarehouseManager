# WarehouseManager

### Target functionality:
- Organize and store items.
- Check item utilization history and use that data to predict future.
- Set auto alarm when have to resupply to keep item above given threshold.


### Sample usage:
- Creates an account
- Add "Storage" - room / place where items are stored, eg. Home, Garage, Basement, etc. 
- Add "Container" - container in storage, eg. "Green carton", "Red cartoon", etc.
- Add "Item" - what you want to store, eg. "Pasta", "Canned corn", etc.
- [optional] Add "Shop"
- [optional] "Amount unit" - unit in which you want to store item, eg. "kg", etc.
- Add / set "Item amount" - change of amount
- [optional] Add "Alert"

# Credits: <br>
[Penguin logo by Johannes Schröter](https://www.pexels.com/photo/cold-snow-nature-bird-5302686/)


# Development technicals / notes:
- Frontend renders data from DB (duh)
- User selects data (menu at the top of the page)
- On default no data is rendered