import datetime
import azure.keyvault.secrets as secrets
from azure.identity import ClientSecretCredential
import azure
from env.logger import CustomLogging
from typing import Optional

logger=CustomLogging().get_logger('standard')


def get_secret_from_key_vault(key_vault_url,
                              secret_name,
                              managed_identity=True,
                              tenant_id=Optional[str],
                              client_id=Optional[str],
                              client_secret=Optional[str]):
    """
      This utility function fetches the secret value from a key vault.
      You need to provide two mandatory arguments key_vault_url and  secret_name.

      Be default it will try to use managed identity for authentication.
      For service principle way of authentication , you need to set managed_identity flag to False and
      you should provide tenant_id,client_id and client_secret.

    :param key_vault_url: Key vault url
    :param secret_name: secret name for your secret
    :param managed_identity : Optional, default is True. This is for controlling authentication method.
    By setting this False, function will assume that you are asking for a service principle authentication.
    Then You should provide tenant_id, client_id and client_secret of service principle.
    :param tenant_id: Optional, default is None. Tenant id of service principle
    :param client_id: Optional, default is None. client_id of service principle
    :param client_secret: Optional, default is None. client_secret of service principle
    :return: returns secret value for the secret name
    """
    if managed_identity:
        logger.info("Trying for Managed identity authentication")
        credential = azure.identity.ManagedIdentityCredential()
        credential.get_token(key_vault_url + '.default')
    else:
        logger.info("Trying for Service principle authentication.")

        # Setting life span of credential to 2 hours from time of generation using expires_on optional argument

        expires_on_timestamp = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        credential = ClientSecretCredential(tenant_id, client_id, client_secret, expires_on=expires_on_timestamp)
    client = azure.keyvault.secrets.SecretClient(vault_url=key_vault_url, credential=credential)
    return client.get_secret(secret_name).value
