from django.apps import AppConfig
import os
from apps.blockchain.utils import deploy_contract


class BlockchainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blockchain'

    def ready(self) -> None:
        if os.environ.get("RUN_MAIN") == 'true':
            print("========== CONTRACT DEPLOYED ========")
            deploy_contract()
