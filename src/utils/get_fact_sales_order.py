import awswrangler as wr
from awswrangler import _utils
pg8000_native = _utils.import_optional_dependency("pg8000.native")
from pg8000.native import literal, identifier, DatabaseError
import datetime
from decimal import Decimal
import logging

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)

def get_fact_sales_order(con, time_of_last_query):
    try:
        table = 'sales_order'
        keys = ['sales_order_id', 'created_at', 'last_updated',
                'design_id', 'staff_id', 'counterparty_id', 'units_sold',
                'unit_price', 'currency_id', 'agreed_delivery_date',
                'agreed_payment_date', 'agreed_delivery_location_id']

        query = f"""SELECT * FROM {identifier(table)} 
                WHERE last_updated>{literal(time_of_last_query)};"""
        rows = con.run(query)


        fact_sales_order={'fact_sales_order':[]}
        for row in rows:
            data_point = {}
            for ii,(k,v) in enumerate(zip(keys, row)):
                if ii==1:
                    data_point['created_date'] = v.date()
                    data_point['created_time'] = v.time()
                elif ii==2:
                    data_point['last_updated_date'] = v.date()
                    data_point['last_updated_time'] = v.time()
                elif ii==4:
                    data_point['sales_staff_id'] = v
                elif ii==7:
                    data_point[k] = Decimal(round(v,2))
                elif ii==9:
                    data_point[k]=datetime.datetime.strptime(v,'%Y-%m-%d').date()
                elif ii==10:
                    data_point[k]=datetime.datetime.strptime(v,'%Y-%m-%d').date()
                else:
                    data_point[k] = v
            fact_sales_order['fact_sales_order'].append(data_point)
        return fact_sales_order
    except Exception as e:
        logger.error(e)

    

if __name__ == "__main__":
    get_fact_sales_order(None, datetime.datetime.now())