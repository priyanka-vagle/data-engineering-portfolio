import csv

state_mapping = {}
missing_sales_count = 0
invalid_sales_count = 0
rejected_orders = []
with open("data/reference/state_mapping.csv", "r") as mapping_file:
    mapping_reader = csv.DictReader(mapping_file)
    for row in mapping_reader:
        state_mapping[row["source_state"]] = row["standard_state"]
    print(state_mapping)
with open("data/raw/orders.csv","r") as file:
    reader = csv.DictReader(file)
    state_sales={}
    unknown_state_count = 0
    for order in reader:
        if order["sales"] == "":
            missing_sales_count += 1
            order["reason"] = "MISSING_SALES"
            rejected_orders.append(order)
            continue
        try:
            order["sales"]=int(order["sales"])
        except ValueError:
            invalid_sales_count += 1
            order["reason"] = "INVALID_SALES"
            rejected_orders.append(order)
            continue
        state = order["state"].strip().upper()
        if state =="":
            state= "UNKNOWN"
            unknown_state_count += 1
        state = state_mapping.get(state, state)
        if state in state_sales:
            state_sales[state]+=order["sales"]
        else:
            state_sales[state]=order["sales"]
    print(state_sales)
    print("Unknown state records:", unknown_state_count)
    print("Missing sales records:", missing_sales_count)
    print("Invalid sales records:", invalid_sales_count)
    print(rejected_orders)
    total_rejected_records = len(rejected_orders)
    print("Total rejected records:", total_rejected_records)
    with open("data/processed/sales_by_state.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["state", "total_sales"])
        for state, total_sales in state_sales.items():
            writer.writerow([state, total_sales])
    with open("data/rejected/rejected_orders.csv", "w", newline="") as file:
        writer = csv.DictWriter(file,fieldnames=["order_id", "state", "sales", "reason"])
        writer.writeheader()
        for order in rejected_orders:
            writer.writerow(order)
            

