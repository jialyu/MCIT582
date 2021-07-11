from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    result = True
    
    if content['payload']['platform']=='Ethereum': 
        eth_account.Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = eth_account.Account.create_with_mnemonic()

        eth_pk = acct.address
        eth_sk = acct.key

        eth_encoded_msg = eth_account.messages.encode_defunct(text=json.dumps(content['payload']))
        eth_sig_obj = eth_account.Account.sign_message(eth_encoded_msg,eth_sk)


        #Check if signature is valid
        if eth_account.Account.recover_message(eth_encoded_msg,signature=content['sig']) == content['payload']['pk']: 
            result = True #Should only be true if signature validates
        else: 
            result = False
    
    if content['payload']['platform']=='Algorand':
        algo_sk, algo_pk = algosdk.account.generate_account()
        algo_sig_str = algosdk.util.sign_bytes(json.dumps(content['payload']).encode('utf-8'),algo_sk)

        if algosdk.util.verify_bytes(json.dumps(content['payload']).encode('utf-8'),content['sig'],content['payload']['pk']):
            result = True
        else: 
            result = False
        
    return jsonify(result)


if __name__ == '__main__':
    app.run(port='5002')
