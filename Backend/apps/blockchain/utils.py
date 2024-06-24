import os
import json
from solcx import compile_standard
from web3 import Web3
from django.conf import settings

web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
chain_id = settings.CHAIN_ID
my_address = settings.MY_ADDRESS
private_key = settings.PRIVATE_KEY

def deploy_contract():
    try:
        # Read Solidity source code
        contract_path = os.path.join('apps','blockchain', 'contracts', 'storage.sol')
        with open(contract_path, "r") as file:
            simple_storage_file = file.read()

        # Compile Solidity code
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"storage.sol": {"content": simple_storage_file}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                    }
                },
            },
            solc_version="0.8.0",
        )

        # Extract bytecode and ABI
        bytecode = compiled_sol["contracts"]["storage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
        abi = compiled_sol["contracts"]["storage.sol"]["SimpleStorage"]["abi"]

        # Create contract instance
        SimpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)

        # Get nonce
        nonce = web3.eth.get_transaction_count(my_address)

        # Build transaction
        transaction = SimpleStorage.constructor().build_transaction({
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
            "gas": 6721975,
            "gasPrice": web3.to_wei('50', 'gwei'),
        })

        # Sign transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

        # Send transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for transaction receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # Save compiled code to JSON file with contract address
        compiled_sol["contracts"]["storage.sol"]["SimpleStorage"]["address"] = tx_receipt.contractAddress
        compiled_contract_path = os.path.join('apps','blockchain', 'contracts', 'compiled_code.json')
        with open(compiled_contract_path, "w") as file:
            json.dump(compiled_sol, file)

        # Return contract address and ABI
        return {
            "contract_address": tx_receipt.contractAddress,
            "abi": abi
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_contract_instance():
    compiled_contract_path = os.path.join('apps','blockchain', 'contracts', 'compiled_code.json')
    with open(compiled_contract_path) as f:
        compiled_sol = json.load(f)
    abi = compiled_sol["contracts"]["storage.sol"]["SimpleStorage"]["abi"]
    contract_address = compiled_sol["contracts"]["storage.sol"]["SimpleStorage"].get("address")
    if not contract_address:
        raise ValueError("Contract address not found")
    return web3.eth.contract(address=contract_address, abi=abi)
