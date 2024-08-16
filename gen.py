import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(num_products=500, percentage_delayed=15, percentage_returns=10):
    # parameters 
    num_shipments = 2000
    num_orders = 10000
    num_returns = 5000

    # inventory data
    np.random.seed(0)
    product_ids = np.arange(1001, 1001 + num_products)
    product_names = [f'Product {i}' for i in range(num_products)]
    locations = np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], num_products)
    stock_levels = np.random.randint(0, 300, num_products)
    reorder_points = np.random.randint(10, 50, num_products)

    inventory_data = {
        "Product ID": product_ids,
        "Product Name": product_names,
        "Warehouse Location": locations,
        "Current Stock Level": stock_levels,
        "Reorder Point": reorder_points
    }

    inventory_df = pd.DataFrame(inventory_data)

    shipment_ids = np.arange(2001, 2001 + num_shipments)
    origins = np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], num_shipments)
    destinations = np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], num_shipments)
    statuses = np.random.choice(['In Transit', 'Delivered', 'Delayed'], num_shipments)
    arrival_times = [datetime.now() + timedelta(hours=np.random.randint(1, 24)) for _ in range(num_shipments)]

    transportation_data = {
        "Shipment ID": shipment_ids,
        "Origin": origins,
        "Destination": destinations,
        "Status": statuses,
        "Estimated Arrival Time": arrival_times
    }

    transportation_df = pd.DataFrame(transportation_data)

    order_ids = np.arange(3001, 3001 + num_orders)
    customer_ids = np.random.randint(4001, 5001, num_orders)
    product_ids_orders = np.random.choice(product_ids, num_orders)
    order_dates = [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(num_orders)]

    
    fulfillment_statuses = np.random.choice(
        ['On Time', 'Delayed'],
        num_orders,
        p=[1 - percentage_delayed / 100, percentage_delayed / 100]
    )

    order_data = {
        "Order ID": order_ids,
        "Customer ID": customer_ids,
        "Product ID": product_ids_orders,
        "Order Date": order_dates,
        "Fulfillment Status": fulfillment_statuses
    }

    order_df = pd.DataFrame(order_data)

    num_returns = int(num_orders * percentage_returns / 100)  
    return_ids = np.arange(5001, 5001 + num_returns)
    product_ids_returns = np.random.choice(product_ids, num_returns)
    return_reasons = np.random.choice(['Defective', 'Changed Mind', 'Wrong Item', 'Damaged Packaging'], num_returns)
    return_dates = [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(num_returns)]
    processing_times = np.random.randint(1, 10, num_returns)  

    reverse_logistics_data = {
        "Return ID": return_ids,
        "Product ID": product_ids_returns,
        "Return Reason": return_reasons,
        "Return Date": return_dates,
        "Processing Time": processing_times
    }

    reverse_logistics_df = pd.DataFrame(reverse_logistics_data)
    inventory_df.to_csv("inventory_data.csv", index=False)
    transportation_df.to_csv("transportation_data.csv", index=False)
    order_df.to_csv("order_data.csv", index=False)
    reverse_logistics_df.to_csv("reverse_logistics_data.csv", index=False)

    print("Large sample data created and saved as CSV files.")
# mutable dataset acc to requirement
generate_data(num_products=500, percentage_delayed=15, percentage_returns=10)
