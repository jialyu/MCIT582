from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine, select, MetaData, Table
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

#These decorators allow you to use g.session to access the database inside the request code
@app.before_request
def create_session():
    g.session = scoped_session(DBSession) #g is an "application global" https://flask.palletsprojects.com/en/1.1.x/api/#application-globals

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    g.session.commit()
    g.session.remove()

"""
-------- Helper methods (feel free to add your own!) -------
"""

def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    g.session.add(Log(d))
    g.session.commit()

"""
---------------- Endpoints ----------------
"""
    
@app.route('/trade', methods=['POST'])
def trade():
    if request.method == "POST":
        content = request.get_json(silent=True)
        print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
        
        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                error = True
        if error:
            print( json.dumps(content) )
            log_message(content)
            return jsonify( False )
            
        #Your code here
        #Note that you can access the database session using g.session
        result = True
        if content['payload']['platform']=='Ethereum': 
            eth_account.Account.enable_unaudited_hdwallet_features()
            acct, mnemonic = eth_account.Account.create_with_mnemonic()

            eth_pk = acct.address
            eth_sk = acct.key

            eth_encoded_msg = eth_account.messages.encode_defunct(text=json.dumps(content['payload']))
            eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg,eth_sk)

            #Check if signature is valid
            if eth_account.Account.recover_message(eth_encoded_msg,signature=content['sig']) == content['payload']['sender_pk']: 
                result = True #Should only be true if signature validates
                verified_order = Order( sender_pk=content['payload']['sender_pk'],receiver_pk=content['payload']['receiver_pk'], buy_currency=content['payload']['buy_currency'], sell_currency=content['payload']['sell_currency'], buy_amount=content['payload']['buy_amount'], sell_amount=content['payload']['sell_amount'], signature=content['sig'] )
                fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount','signature']
                verified_order = Order(**{f:order[f] for f in fields})
                g.session.add(verified_order)
                g.session.commit()
            else: 
                result = False
                log_message((json.dumps(content['payload'])))
                
        if content['payload']['platform']=='Algorand':
            algo_sk, algo_pk = algosdk.account.generate_account()
            algo_sig_str = algosdk.util.sign_bytes(json.dumps(content['payload']).encode('utf-8'),algo_sk)

            if algosdk.util.verify_bytes(json.dumps(content['payload']).encode('utf-8'),content['sig'],content['payload']['sender_pk']):
                result = True
                verified_order = Order( sender_pk=content['payload']['sender_pk'],receiver_pk=content['payload']['receiver_pk'], buy_currency=content['payload']['buy_currency'], sell_currency=content['payload']['sell_currency'], buy_amount=content['payload']['buy_amount'], sell_amount=content['payload']['sell_amount'], signature=content['sig'] )
                fields = ['sender_pk','receiver_pk','buy_currency','sell_currency','buy_amount','sell_amount','signature']
                verified_order = Order(**{f:order[f] for f in fields})
                g.session.add(verified_order)
                g.session.commit()
            else: 
                result = False
                log_message((json.dumps(content['payload'])))
                
    return (jsonify(result))
        
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