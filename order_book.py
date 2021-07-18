from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #Your code here
    new_order = Order( sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], buy_currency=order['buy_currency'], sell_currency=order['sell_currency'], buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )
    fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount']
    new_order = Order(**{f:order[f] for f in fields})

    session.add(new_order)
    session.commit()
    
    existing_orders = session.query(Order).all()
    
    for order in existing_orders: 
        if (order.filled==None): 
            if (order.buy_currency == new_order.sell_currency) & (order.sell_currency == new_order.buy_currency): 
                if (order.buy_amount>0) & (new_order.sell_amount>0): 
                    if (order.sell_amount / order.buy_amount >= new_order.buy_amount/new_order.sell_amount): 
                        if len(order.counterparty)==0: 
                            order.filled = new_order.timestamp
                            new_order.filled = new_order.timestamp
                            order.counterparty = new_order.counterparty
                            new_order.counterparty = new_order.counterparty
                            order.counterparty_id = new_order.counterparty_id
                            new_order.counterparty_id = new_order.counterparty_id
                            if order.sell_amount < order.buy_amount: 
                                new = Order()
                                new.sender_pk=order.sender_pk
                                new.receiver_pk=order.receiver_pk
                                new.buy_currency=order.buy_currency
                                new.sell_currency=order.sell_currency
                                new.sell_amount=(order.sell_amount/order.buy_amount)
                                new.buy_amount=0
                                new.created_by = order.id
                                session.add(new)
                                session.commit()