from rest_framework.views import APIView
from rest_framework import permissions

from django.http import JsonResponse
from apps.blockchain.utils import deploy_contract, get_contract_instance
from web3 import Web3
from django.conf import settings

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
my_address = settings.MY_ADDRESS
private_key = settings.PRIVATE_KEY

class DeployContractView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        contract_info = deploy_contract()
        if contract_info:
            return JsonResponse({"status": "success", "contract_address": contract_info["contract_address"], "abi": contract_info["abi"]})
        else:
            return JsonResponse({"status": "failure", "message": "Contract deployment failed."}, status=500)

class SetValueView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        value = request.data.get('value')
        if value is not None:
            try:
                contract = get_contract_instance()
                nonce = web3.eth.get_transaction_count(my_address)
                transaction = contract.functions.set(value).build_transaction({
                    'chainId': settings.CHAIN_ID,
                    'gas': 2000000,
                    'gasPrice': web3.to_wei('50', 'gwei'),
                    'nonce': nonce,
                })
                signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                web3.eth.wait_for_transaction_receipt(tx_hash)
                return JsonResponse({"status": "success", "tx_hash": tx_hash.hex()})
            except Exception as e:
                return JsonResponse({"status": "failure", "message": str(e)}, status=500)
        return JsonResponse({"status": "failure", "message": "Invalid value."}, status=400)
    

class GetValueView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            contract = get_contract_instance()
            stored_values = contract.functions.get().call()
            return JsonResponse({"status": "success", "stored_values": stored_values})
        except Exception as e:
            return JsonResponse({"status": "failure", "message": str(e)}, status=500)
