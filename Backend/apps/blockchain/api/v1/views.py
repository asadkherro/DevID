from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions

from django.http import JsonResponse
from apps.blockchain.utils import deploy_contract, get_contract_instance
from web3 import Web3
from django.conf import settings


from .serializers import DeviceSerializer

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
my_address = settings.MY_ADDRESS
private_key = settings.PRIVATE_KEY


class DeployContractView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        contract_info = deploy_contract()
        if contract_info:
            return JsonResponse(
                {
                    "status": "success",
                    "contract_address": contract_info["contract_address"],
                    "abi": contract_info["abi"],
                }
            )
        else:
            return JsonResponse(
                {"status": "failure", "message": "Contract deployment failed."},
                status=500,
            )


# class SetValueView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer = DeviceSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer(data=request.data)
#         if not serializer.is_valid():
#             return JsonResponse(
#                 {"status": "failure", "message": serializer.errors},
#                 status=400
#             )

#         validated_data = serializer.validated_data
#         name = validated_data["name"]
#         ip_address = validated_data["ip_address"]
#         mac_address = validated_data["mac_address"]
#         running_device = validated_data.get("running_device", "")
#         os_cpe = validated_data.get("os_cpe", "")
#         os_details = validated_data.get("os_details", "")
#         os_guesses = validated_data.get("os_guesses", "")

#         try:
#             contract = get_contract_instance()
#             nonce = web3.eth.get_transaction_count(my_address)
#             transaction = contract.functions.set(
#                 name, ip_address, mac_address, running_device, os_cpe, os_details, os_guesses
#             ).build_transaction(
#                 {
#                     "chainId": settings.CHAIN_ID,
#                     "gas": 2000000,
#                     "gasPrice": web3.to_wei("50", "gwei"),
#                     "nonce": nonce,
#                 }
#             )
#             signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
#             tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
#             tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

#             id_hex = None
#             for log in tx_receipt.logs:
#                 id_in_bytes = log.data
#                 res = "".join(format(x, "02x") for x in id_in_bytes)
#                 id_hex = str(res)[:64]

#             if id_hex is None:
#                 return JsonResponse(
#                     {"status": "failure", "message": "DeviceAdded event not found"},
#                     status=500,
#                 )

#             return JsonResponse(
#                 {"status": "success", "tx_hash": tx_hash.hex(), "id": id_hex}
#             )
#         except Exception as e:
#             return JsonResponse(
#                 {"status": "failure", "message": str(e)}, status=500
#             )

# class GetValueView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request, *args, **kwargs):
#         try:
#             contract = get_contract_instance()
#             stored_values = contract.functions.getAllDevices().call()

#             # Converting stored values to JSON serializable format
#             result = []
#             for device in stored_values:
#                 result.append(
#                     {
#                         "id": device[0].hex(),  # Convert bytes32 to hex string
#                         "name": device[1],
#                         "ip_address": device[2],
#                         "mac_address": device[3],
#                         "runningDevice": device[4],
#                         "os_cpe": device[5],
#                         "os_details": device[6],
#                         "os_guesses": device[7],
#                     }
#                 )

#             return JsonResponse({"status": "success", "stored_values": result})
#         except Exception as e:
#             return JsonResponse({"status": "failure", "message": str(e)}, status=500)


# class DeleteDeviceView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def delete(self, request, *args, **kwargs):
#         device_id = kwargs.get("id")

#         if not device_id:
#             return JsonResponse(
#                 {"status": "failure", "message": "Device ID is required."},
#                 status=400
#             )

#         try:
#             contract = get_contract_instance()
#             nonce = web3.eth.get_transaction_count(my_address)
#             transaction = contract.functions.deleteDevice(
#                 Web3.toBytes(hexstr=device_id)
#             ).build_transaction(
#                 {
#                     "chainId": settings.CHAIN_ID,
#                     "gas": 2000000,
#                     "gasPrice": web3.to_wei("50", "gwei"),
#                     "nonce": nonce,
#                 }
#             )
#             signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
#             tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
#             tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

#             return JsonResponse(
#                 {"status": "success", "tx_hash": tx_hash.hex()}
#             )
#         except Exception as e:
#             return JsonResponse(
#                 {"status": "failure", "message": str(e)}, status=500
#             )


class DeviceViewSet(viewsets.ViewSet):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "failure", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        name = validated_data["name"]
        ip_address = validated_data["ip_address"]
        mac_address = validated_data["mac_address"]
        running_device = validated_data.get("running_device", "")
        os_cpe = validated_data.get("os_cpe", "")
        os_details = validated_data.get("os_details", "")
        os_guesses = validated_data.get("os_guesses", "")

        try:
            contract = get_contract_instance()
            nonce = web3.eth.get_transaction_count(my_address)
            transaction = contract.functions.set(
                name,
                ip_address,
                mac_address,
                running_device,
                os_cpe,
                os_details,
                os_guesses,
            ).build_transaction(
                {
                    "chainId": settings.CHAIN_ID,
                    "gas": 2000000,
                    "gasPrice": web3.to_wei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            signed_txn = web3.eth.account.sign_transaction(
                transaction, private_key=private_key
            )
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            id_hex = None
            for log in tx_receipt.logs:
                id_in_bytes = log.data
                res = "".join(format(x, "02x") for x in id_in_bytes)
                id_hex = str(res)[:64]

            if id_hex is None:
                return Response(
                    {"status": "failure", "message": "DeviceAdded event not found"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"status": "success", "tx_hash": tx_hash.hex(), "id": id_hex}
            )
        except Exception as e:
            return Response(
                {"status": "failure", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            contract = get_contract_instance()
            device = contract.functions.getDeviceById(Web3.toBytes(hexstr=pk)).call()
            result = {
                "id": device[0].hex(),  # Convert bytes32 to hex string
                "name": device[1],
                "ip_address": device[2],
                "mac_address": device[3],
                "running_device": device[4],
                "os_cpe": device[5],
                "os_details": device[6],
                "os_guesses": device[7],
            }
            return Response({"status": "success", "device": result})
        except Exception as e:
            return Response(
                {"status": "failure", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def list(self, request):
        try:
            contract = get_contract_instance()
            stored_values = contract.functions.getAllDevices().call()

            result = []
            for device in stored_values:
                result.append(
                    {
                        "id": device[0].hex(),  # Convert bytes32 to hex string
                        "name": device[1],
                        "ip_address": device[2],
                        "mac_address": device[3],
                        "running_device": device[4],
                        "os_cpe": device[5],
                        "os_details": device[6],
                        "os_guesses": device[7],
                    }
                )

            return Response({"status": "success", "devices": result})
        except Exception as e:
            return Response(
                {"status": "failure", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "failure", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        name = validated_data.get("name", "")
        ip_address = validated_data.get("ip_address", "")
        mac_address = validated_data.get("mac_address", "")
        running_device = validated_data.get("running_device", "")
        os_cpe = validated_data.get("os_cpe", "")
        os_details = validated_data.get("os_details", "")
        os_guesses = validated_data.get("os_guesses", "")

        try:
            contract = get_contract_instance()
            device_id = bytes.fromhex(pk)  # Convert hex string to bytes
            nonce = web3.eth.get_transaction_count(my_address)
            transaction = contract.functions.updateDevice(
                device_id,
                name,
                ip_address,
                mac_address,
                running_device,
                os_cpe,
                os_details,
                os_guesses,
            ).build_transaction(
                {
                    "chainId": settings.CHAIN_ID,
                    "gas": 2000000,
                    "gasPrice": web3.to_wei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            signed_txn = web3.eth.account.sign_transaction(
                transaction, private_key=private_key
            )
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            return Response({"status": "success", "tx_hash": tx_hash.hex()})
        except Exception as e:
            return Response(
                {"status": "failure", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        try:
            contract = get_contract_instance()
            device_id = Web3.to_bytes(hexstr=pk)  # Convert hex string to bytes32

            nonce = web3.eth.get_transaction_count(my_address)
            transaction = contract.functions.deleteDeviceById(
                device_id
            ).build_transaction(
                {
                    "chainId": settings.CHAIN_ID,
                    "gas": 2000000,
                    "gasPrice": web3.to_wei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            signed_txn = web3.eth.account.sign_transaction(
                transaction, private_key=private_key
            )
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            web3.eth.wait_for_transaction_receipt(tx_hash)

            return Response({"status": "success", "tx_hash": tx_hash.hex()})
        except Exception as e:
            return Response(
                {"status": "failure", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
