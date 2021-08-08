from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from datetime import datetime
import sys

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.before_request
def create_session():
    g.session = scoped_session(DBSession)

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()


""" Suggested helper methods """

def check_sig(payload,sig):
    result = True
    if payload['platform']=='Ethereum': 
        eth_account.Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = eth_account.Account.create_with_mnemonic()

        eth_pk = acct.address
        eth_sk = acct.key

        eth_encoded_msg = eth_account.messages.encode_defunct(text=json.dumps(payload))
        eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg,eth_sk)

        #Check if signature is valid
        if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == payload['sender_pk']: 
            result = True #Should only be true if signature validates
            verified_order = Order( sender_pk=payload['sender_pk'],receiver_pk=payload['receiver_pk'], buy_currency=payload['buy_currency'], sell_currency=payload['sell_currency'], buy_amount=payload['buy_amount'], sell_amount=payload['sell_amount'], signature=content['sig'] )
            # fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount','signature']
            # verified_order = Order(**{f:order[f] for f in fields})
            # g.session.add(verified_order)
            # g.session.commit()
        else: 
            result = False
            log_message((json.dumps(payload)))
            
    if payload['platform']=='Algorand':
        algo_sk, algo_pk = algosdk.account.generate_account()
        algo_sig_str = algosdk.util.sign_bytes(json.dumps(payload).encode('utf-8'),algo_sk)

        if algosdk.util.verify_bytes(json.dumps(payload).encode('utf-8'),sig,payload['sender_pk']):
            result = True
            verified_order = Order( sender_pk=payload['sender_pk'],receiver_pk=payload['receiver_pk'], buy_currency=payload['buy_currency'], sell_currency=payload['sell_currency'], buy_amount=payload['buy_amount'], sell_amount=payload['sell_amount'], signature=sig )
            # fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount','signature']
            # verified_order = Order(**{f:order[f] for f in fields})
            # g.session.add(verified_order)
            # g.session.commit()
        else: 
            result = False
            log_message((json.dumps(payload)))

    return verified_order, result

def fill_order(order,txes=[]):
    new_order = Order( sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], buy_currency=order['buy_currency'], sell_currency=order['sell_currency'], buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )
    fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount']
    new_order = Order(**{f:order[f] for f in fields})

    g.session.add(new_order)
    g.session.commit()
    
    existing_orders = session.query(Order).all()
    
    for order in existing_orders: 
        if (order.filled==None): 
            if (order.buy_currency == new_order.sell_currency) & (order.sell_currency == new_order.buy_currency): 
                if (order.buy_amount>0) & (new_order.sell_amount>0): 
                    if (order.sell_amount / order.buy_amount >= new_order.buy_amount/new_order.sell_amount): 
                        if order.counterparty_id==None: 
                            order.filled = datetime.now()
                            new_order.filled = datetime.now()
                            order.counterparty_id = new_order.id
                            new_order.counterparty_id = order.id
                            if order.sell_amount < order.buy_amount: 
                                new = Order()
                                new.sender_pk=new_order.sender_pk
                                new.receiver_pk=new_order.receiver_pk
                                new.buy_currency=new_order.buy_currency
                                new.sell_currency=new_order.sell_currency
                                new.buy_amount=random.randint(1,10)
                                new.sell_amount=new_order.sell_amount*(new.buy_amount/new_order.buy_amount)
                                new.created_by = new_order.id
                                new.creator_id = new_order.id
                                g.session.add(new)
                            g.session.commit()
                            break
  
def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    # Hint: use json.dumps or str() to get it in a nice string form
    g.session.add(json.dumps(d))
    g.session.commit()

""" End of helper methods """

@app.route('/trade', methods=['POST'])
def trade():
    print("In trade endpoint")
    if request.method == "POST":
        content = request.get_json(silent=True)
        print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]

        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
        
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
            
        #Your code here
        #Note that you can access the database session using g.session

        # TODO: Check the signature
        verified_order, result = check_sig(content['payload'], content['sig'])
        # TODO: Add the order to the database
        g.session.add(verified_order)
        g.session.commit()
        # TODO: Fill the order
        fill_order(verified_order)
        # TODO: Be sure to return jsonify(True) or jsonify(False) depending on if the method was successful
        return jsonify(result)

@app.route('/order_book')
def order_book():
    #Your code here
    #Note that you can access the database session using g.session
    existing_orders = g.session.query(Order).all()
    orders_dict = {}
    orders_list = []
    for order in existing_orders: 
        order_dict = {}
        order_dict['sender_pk'] = order.sender_pk
        order_dict['receiver_pk'] = order.receiver_pk
        order_dict['buy_currency'] = order.buy_currency
        order_dict['sell_currency'] = order.sell_currency
        order_dict['buy_amount'] = order.buy_amount
        order_dict['sell_amount'] = order.sell_amount
        order_dict['signature'] = order.signature
        orders_list.append(order_dict)
    orders_dict['data'] = orders_list
    return jsonify(orders_dict)

if __name__ == '__main__':
    app.run(port='5002')