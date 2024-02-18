

import logging
import json
import re
import collections
import warnings
import jwt
import pandas as pd

import ibm_aigov_facts_client._wrappers.requests as requests


from ..utils.client_errors import *
from typing import BinaryIO, Dict, List,Any,Sequence

from ibm_aigov_facts_client.client import fact_trace
from ibm_aigov_facts_client.factsheet.asset_utils_model import ModelAssetUtilities
from ibm_aigov_facts_client.factsheet.asset_utils_prompt import AIGovAssetUtilities
from ibm_aigov_facts_client.factsheet.asset_utils_me import ModelUsecaseUtilities
from ibm_aigov_facts_client.factsheet.asset_utils_me_prompt import AIUsecaseUtilities
from ibm_aigov_facts_client.utils.enums import AssetContainerSpaceMap, AssetContainerSpaceMapExternal,ContainerType, FactsType, ModelEntryContainerType, AllowedDefinitionType,FormatType,AttachmentFactDefinitionType,Status,Risk
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator,CloudPakForDataAuthenticator

from ibm_aigov_facts_client.utils.utils import validate_enum,validate_type,STR_TYPE
from ibm_aigov_facts_client.utils.me_containers_meta import AssetsContainersDefinitions
from ibm_aigov_facts_client.utils.constants import *
from ibm_aigov_facts_client.utils.config import *
from ibm_aigov_facts_client.utils.doc_annotations import deprecated


_logger = logging.getLogger(__name__) 

class Assets:
    
    def __init__(self, facts_client: 'fact_trace.FactsClientAdapter'):
        self._container_type= facts_client._container_type
        self._container_id= facts_client._container_id
        self._asset_id=None
        self._model_id=None
        self._model_usecase_id=None
        self._current_model=None
        self._current_model_usecase=None
        self._facts_type=None
        self._cpd_configs=None
        self._is_cp4d=facts_client._is_cp4d
        self._facts_client=facts_client
        self._external_model=self._facts_client._external
        if self._is_cp4d:
            self._cpd_configs=facts_client.cp4d_configs
            self._cp4d_version=facts_client._cp4d_version
        self._cpd_op_enabled=False
        self._facts_definitions=None
                
    
    
    def create_custom_facts_definitions(self, csvFilePath, type_name:str=None,section_name:str=None, overwrite=True):
        """
            Utility to add custom facts attribute properties of model or model usecase.
            
            :param str csvFilePath: File path of csv having the asset properties.
            :param str type_name: Asset type user needs to add/update. Current options are `modelfacts_user`,`model_entry_user`. Default is set to `modelfacts_user`.
            :param str section_name: Custom name to show for custom attribute section. Applies only to `model_entry_user` type.
            :param bool overwrite: (Optional) Merge or replace current properties. Default is True.
            

            A way you might use me is:

            >>> client.assets.create_custom_facts_definitions("Asset_type_definition.csv") # uses default type `modelfacts_user` type
            >>> client.assets.create_custom_facts_definitions("Asset_type_definition.csv",type_name="model_entry_user", localized_name=<custom name for attributes section>,overwrite=False)

        """

        validate_enum(type_name,
                      "type_name", FactsType, False)

        if section_name and type_name!=FactsType.MODEL_USECASE_USER:
            raise ClientError("localized name change is only supported for `model_entry_user` type")

        if self._is_cp4d:
            cur_bss_id = self._get_bss_id_cpd()
        else:
            cur_bss_id = self._get_bss_id()

        self.type_name = type_name or FactsType.MODEL_FACTS_USER
        _logger.info("Creating definitions for type {}".format(self.type_name))

        asset_conf_data = self._format_data(
            csvFilePath, overwrite, self.type_name,section_name)

        if asset_conf_data:
            self._update_props(asset_conf_data, cur_bss_id, self.type_name)
        else:
            raise ClientError("Error formatting properties data from file")

    
    def get_facts_definitions(self,type_name:str,container_type:str=None,container_id:str=None)->Dict:

        """
            Get all facts definitions

            :param str type_name: Asset fact type. Current options are `modelfacts_user` and `model_entry_user`.
            :param str container_type: (Optional) Asset container type. Options are `project`, `space` or `catalog`. Default to container type used when initiating client.
            :param str container_id: (Optional) Asset container id. Default to container id when initiating client

            :rtype: dict

            A way you might use me is:

            >>> client.assets.get_facts_definitions(type_name=<fact type>) # uses container type and id used initializing facts client
            >>> client.assets.get_facts_definitions(type_name=<fact type>,container_type=<container type>,container_id=<container id>)

        """

        validate_enum(type_name,
                      "type_name", FactsType, True)
        validate_enum(container_type,
                      "container_type", ContainerType, False)

        if self._external_model:
            container_type=container_type or MODEL_USECASE_CONTAINER_TYPE_TAG
            container_id=container_id or self._get_pac_catalog_id()
        else:
            container_type=container_type or self._container_type
            container_id=container_id or self._container_id

        if not container_type or not container_id:
            raise ClientError("Please provide a valid container type and container id")

        if self._is_cp4d:
            url = self._cpd_configs["url"] + \
                    "/v2/asset_types/" + type_name + "?" + container_type + "_id=" + container_id
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    "/v2/asset_types/" + type_name + "?" + container_type + "_id=" + container_id
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    "/v2/asset_types/" + type_name + "?" + container_type + "_id=" + container_id
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    "/v2/asset_types/" + type_name + "?" + container_type + "_id=" + container_id

        response = requests.get(url, headers=self._get_headers())
        if not response.ok:
            raise ClientError("User facts definitions not found. ERROR {}. {}".format(response.status_code,response.text))
        else:
            return response.json()
    
    
    
    def get_prompt(self, prompt_id: str=None, container_type: str=None, container_id: str=None)-> AIGovAssetUtilities:

        """
            Get prompt asset.

            :param str prompt_id: Id of the prompt asset.
            :param str container_type: Name of the container where prompt is saved. Currently supported container_type are `space` or `project`. 
            :param str container_id: Id of the container where prompt asset is saved.

            :rtype: AIGovAssetUtilities

            The way to use me is:

            >>> client.assets.get_prompt(prompt_id=<prompt_id>,container_type=<project>,container_id=<project id>)

        
        """

        if self._is_cp4d:
            raise ClientError("Mismatch: This functionality is only supported in SaaS IBM Cloud")

        if not prompt_id or prompt_id=="":
            raise ClientError("Prompt id is required and can not be empty value")
        if not container_type or container_type=="":
            raise ClientError("Container_type is required and can not be empty value")
        if not container_id or container_id=="":
            raise ClientError("container_id is required and can not be empty value")
        
        validate_enum(container_type,"container_type", ContainerType, False)
        return self.get_model(prompt_id, container_type, container_id, is_prompt=True)


    # def get_model(self, model_id: str=None, container_type: str=None, container_id: str=None, wml_stored_model_details:dict=None, is_prompt: bool=False)-> ModelAssetUtilities:
    def get_model(self, model_id: str=None, container_type: str=None, container_id: str=None, wml_stored_model_details:dict=None, is_prompt: bool=False):
        
        """
            Get model asset.

            :param str model_id: (Optional) Id of the model asset.
            :param str container_type: (Optional) Name of the container where model is saved. Currently supported container_type are `space` or `project`. For external models it is not needed and defaulted to `catalog`.
            :param str container_id: (Optional) Id of the container where model asset is saved. For external models, it refers to catalog id where model stub is saved. if not provided for external models,if available and user have access, default platform asset catalog is used 
            :param dict wml_stored_model_details: (Optional) Watson machine learning model details. Applied to Watson Machine Learning models only.

            :rtype: ModelAssetUtilities

            The way to use me is:

            >>> client.assets.get_model(model_id=<model_id>) # uses container type and id used to initiate client
            >>> client.assets.get_model(model_id=<model id>,container_type=<space or project>,container_id=<space or project id>)
            >>> client.assets.get_model(wml_stored_model_details=<wml model details>) # uses model id, container type and id part of model details

            for external models,

            >>> client.assets.get_model(model_id=<model_id>) # uses available platform asset catalog id as container_id
            >>> client.assets.get_model(model_id=<model_id>,container_id=<catalog id>)
        
        """

        if  wml_stored_model_details and (model_id or container_type or container_id):
            raise ClientError("Model and container info is not needed when providing wml_stored_model_details")


        validate_enum(container_type,"container_type", ContainerType, False)

        if is_prompt:
            replace_name = "prompt"
        else:
            replace_name = "model"
            
        if not self._external_model and model_id and container_type and container_id:
            url=self._get_assets_url(model_id,container_type,container_id)
            response = requests.get(url, headers=self._get_headers())
            if response.status_code==200:
                get_type=response.json()["metadata"][ASSET_TYPE_TAG]

                if get_type==EXT_MODEL:
                    self._external_model=True
            else:
                raise ClientError("Provide correct details for retrieving a {}".format(replace_name))

        if not self._external_model and container_type==ContainerType.CATALOG:
            raise ClientError("Container type should be `space` or `project` for non-external models")

        if self._external_model:
            self._asset_id=model_id
            self._container_type=container_type or MODEL_USECASE_CONTAINER_TYPE_TAG
            self._container_id=container_id or self._get_pac_catalog_id()
            if not self._container_id:
                raise ClientError("Container id is not provided and no platform asset catalog found to use as default. Please provide a valid catalog id as container_id")
        else:
            if wml_stored_model_details:
                
                try:
                    model_meta=wml_stored_model_details["metadata"]
                    self._asset_id=model_meta.get("id")
                    if model_meta.get(CONTAINER_SPACE):
                        self._container_type=ContainerType.SPACE
                        self._container_id=model_meta.get(CONTAINER_SPACE)
                    elif model_meta.get(CONTAINER_PROJECT):
                        self._container_type=ContainerType.PROJECT
                        self._container_id=model_meta.get(CONTAINER_PROJECT)
                    else:
                        raise ClientError("Failed to get container type from {} details {}".format(replace_name,model_meta))
                    
                except:
                    raise ClientError("Failed to get model details from provided wml_stored_model_details")
            else:
                if not model_id or model_id=="":
                    raise ClientError("Model id is required and can not be empty value")
                self._asset_id=model_id
                self._container_type=container_type or self._facts_client._container_type
                self._container_id=container_id or self._facts_client._container_id

        self._facts_type=FactsType.MODEL_FACTS_USER

        if self._container_type and self._container_id and self._asset_id:
            url=self._get_assets_url(self._asset_id,self._container_type,self._container_id)
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code==404:
                raise ClientError ("Invalid asset id or container id. ERROR {}. {}".format(response.status_code,response.text))
            elif response.status_code==200:
                if is_prompt:
                    self._current_model=AIGovAssetUtilities(self,model_id=self._asset_id,container_type=self._container_type,container_id=self._container_id,facts_type=self._facts_type)
                else:
                    self._current_model=ModelAssetUtilities(self,model_id=self._asset_id,container_type=self._container_type,container_id=self._container_id,facts_type=self._facts_type)
                _logger.info("Current {} information: {}".format(replace_name,self._current_model.to_dict()))
            else:
                raise ClientError("Asset information not found for {} id {}. ERROR {}. {}".format(replace_name,self._asset_id,response.status_code,response.text))
        else:
            raise ClientError("Could not get current {} {}".format(replace_name,self._current_model.to_dict()))

        return self._current_model
    
    def get_ai_usecase(self, ai_usecase_id: str, catalog_id:str=None)->AIUsecaseUtilities:

        """
            Get AI usecase asset.

            :param str ai_usecase_id: Id of the ai usecase.
            :param str catalog_id: Id of the catalog where ai usecase is saved.

            :rtype: AIUsecaseUtilities
            
            The way to use me is:
            
            >>> client.assets.get_ai_usecase(ai_usecase_id=<ai usecase id>, catalog_id=<catalog id>)
        
        """

        if self._is_cp4d:
            raise ClientError("Mismatch: This functionality is only supported in SaaS IBM Cloud")
        
        if (ai_usecase_id is None or ai_usecase_id == ""):
            raise MissingValue("id", "AI usecase asset ID is missing")
    
        return self.get_model_usecase(ai_usecase_id, catalog_id, is_prompt=True)


    def get_model_usecase(self, model_usecase_id: str,catalog_id:str=None, is_prompt: bool=False)->ModelUsecaseUtilities:

        """
            Get model usecase asset.

            :param str model_usecase_id: Id of the model usecase.
            :param str catalog_id: Id of the catalog where model usecase is saved.

            :rtype: ModelUsecaseUtilities
            
            The way to use me is:
            
            >>> client.assets.get_model_usecase(model_usecase_id=<model usecase id>, catalog_id=<catalog id>)
        
        """

        if is_prompt:
            replace_name = "AI"
        else:
            replace_name = "model"
        
        if (model_usecase_id is None or model_usecase_id == ""):
            raise MissingValue("model_usecase_id", "model usecase asset ID is missing")
        if (catalog_id is None or catalog_id == ""):
            raise MissingValue("catalog_id", "Catalog ID is missing")

        self._facts_type=FactsType.MODEL_USECASE_USER
        #catalog_id=catalog_id or self._get_pac_catalog_id()
        catalog_id=catalog_id
        
        #if not catalog_id:
        #    raise ClientError("Catalog id is not provided and no platform asset catalog found to use as default. Please provide a valid catalog id for used model usecase")

        if model_usecase_id and catalog_id:
            url=self._get_assets_url(model_usecase_id,MODEL_USECASE_CONTAINER_TYPE_TAG,catalog_id)
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code==404:
                raise ClientError ("Invalid {} usecase id or catalog id. ERROR {}. {}".format(replace_name,response.status_code,response.text))
            elif response.status_code==200:
                if is_prompt:
                    self._current_model_usecase= AIUsecaseUtilities(self,model_usecase_id=model_usecase_id,container_type=MODEL_USECASE_CONTAINER_TYPE_TAG,container_id=catalog_id,facts_type=self._facts_type)
                else:
                    self._current_model_usecase= ModelUsecaseUtilities(self,model_usecase_id=model_usecase_id,container_type=MODEL_USECASE_CONTAINER_TYPE_TAG,container_id=catalog_id,facts_type=self._facts_type)
                _logger.info("Current {} usecase information: {}".format(replace_name,self._current_model_usecase.to_dict()))
                return self._current_model_usecase
            else:
                raise ClientError("{} usecase information is not found. ERROR {}. {}".format(replace_name,response.status_code,response.text))
    
   
    def get_default_inventory_details(self):
     """
    
      Retrieves details for the default inventory along with the username also.
     
     Usage:
       >>> client.assets.get_default_inventory_details()
     """
    
     if self._is_cp4d:
        raise ClientError("Mismatch: This functionality is only supported in SaaS IBM Cloud")
     else:
        url = self._retrieve_default_inventory_status_url()
        response = requests.get(url, headers=self._get_headers())

        if response.status_code == 200:
            api_response = response.json()
            external_model_admin = api_response.get("external_model_admin")
            external_model_tracking = api_response.get("external_model_tracking")
            inventory_name = api_response.get("inventory_name")

            new_url = self._retrieve_user_profile_url(external_model_admin)
            new_response = requests.get(new_url, headers=self._get_headers())

            if new_response.status_code == 200:
                new_api_response = new_response.json()
                user_names = [
                    resource['entity'].get('name', 'N/A')
                    for resource in new_api_response.get('resources', [])
                    if resource.get('entity', {}).get('iam_id') == external_model_admin
                ] or ['N/A']

                result_string = (
                    f"Default Inventory Details:\n"
                    f"ExternalModel Inventory Enabled: {external_model_tracking}\n"
                    f"Inventory Name: {inventory_name}\n"
                    f"ExternalModel AdminID: {external_model_admin}\n"
                    f"User Names: {', '.join(user_names)}\n"
                )

                _logger.info(result_string)
            else:
                raise ClientError("Failed to fetch the user profile. Unable to proceed.")
        else:
            error_message = "External Model Inventory is not enabled"
            raise ClientError(f"Failed to retrieve members for catalog. Reason: {error_message}")



     

    def remove_asset(self,asset_id:str,container_type:str=None,container_id:str=None):
        """Remove a model or prompt or model usecase asset

        :param asset_id: Id of the asset
        :type asset_id: str
        :param container_type: container where asset is stored, defaults to container type use when initiating client
        :type container_type: str, optional
        :param container_id: container id where asset is stored, defaults to container id used when initiating client. For external models, if not provided, uses available platform asset catalog.
        :type container_id: str, optional
        :raises ClientError: Report exception details

        The way you can use me is :

        >>> client.assets.remove_asset(asset_id=<model or model usecase id>)
        >>> client.assets.remove_asset(asset_id=<model or model usecase id>,container_type=<space,project or catalog>, container_id=<container id>)

        """

        if self._external_model:
            container_type=container_type or MODEL_USECASE_CONTAINER_TYPE_TAG
            container_id=container_id or self._get_pac_catalog_id()
        else:
            container_type=container_type or self._container_type
            container_id=container_id or self._container_id

        url=self._get_assets_url(asset_id,container_type,container_id)
        response = requests.delete(url, headers=self._get_headers())

        if response.status_code==204:
            _logger.info("Successfully deleted asset id {} in {} {}".format(asset_id,container_type,container_id))
        else:
            raise ClientError("Failed to delete asset {}. ERROR {}. {}".format(asset_id,response.status_code,response.text))

    
    @deprecated(alternative="client.assets.get_model_usecases()")
    def list_model_usecases(self, catalog_id:str=None)-> list:
        
        """
            Returns WKC Model usecase assets

            :param str catalog_id: Catalog ID where registered model usecase. if not provided, dafault shows all model usecases in all catalogs across all accounts to which the user has access.
            
            :return: All WKC Model usecase assets for a catalog
            :rtype: list

            Example:

            >>> client.assets.list_model_usecases(catalog_id=<catalog_id>)
            >>> client.assets.list_model_usecases()

        """

        if catalog_id:
            validate_type(catalog_id, u'catalog_id', STR_TYPE, True)
            list_url=WKC_MODEL_LIST_FROM_CATALOG.format(catalog_id)
        else:
            list_url=WKC_MODEL_LIST_ALL

        if self._is_cp4d:
            url=self._cpd_configs["url"] + \
            list_url
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                list_url
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    list_url
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    list_url
        
        #request=self._facts_client.prepare_request(method='GET',url=url,headers=self._get_headers())
        
        response = requests.get(url,
                                headers=self._get_headers()
                                )
        #response=self._facts_client.send(request)

        if response.status_code == 200:
            return response.json()["results"]

        else:
            error_msg = u'WKC Model Entries listing failed'
            reason = response.text
            _logger.info(error_msg)
            raise ClientError(error_msg + '. Error: ' + str(response.status_code) + '. ' + reason)

    
    def _get_pac_catalog_id(self):
            if self._is_cp4d:
                bss_id=self._get_bss_id_cpd()
            else:
                bss_id=self._get_bss_id()

            if self._is_cp4d:
                url = self._cpd_configs["url"] + \
                    '/v2/catalogs/ibm-global-catalog?bss_account_id='+ bss_id
            else:
                if get_env() == 'dev':
                    url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                        '/v2/catalogs/ibm-global-catalog?bss_account_id='+ bss_id
                elif get_env() == 'test':
                    url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                        '/v2/catalogs/ibm-global-catalog?bss_account_id='+ bss_id
                else:
                    url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/catalogs/ibm-global-catalog?bss_account_id='+ bss_id

            response = requests.get(url, headers=self._get_headers())
            catalog_id=response.json()["metadata"]["guid"]
            
            return catalog_id
    
    def _retrieve_default_inventory_status_url(self):
        if self._is_cp4d:
            bss_id = self._get_bss_id_cpd()
        else:
            bss_id = self._get_bss_id()
        if self._is_cp4d:
            url = self._cpd_configs['url'] + \
                  '/v1/aigov/model_inventory/externalmodel_config?bss_account_id' + bss_id
        else:
            if get_env() == 'dev':
                url =dev_config['DEFAULT_DEV_SERVICE_URL']+ \
                    '/v1/aigov/model_inventory/externalmodel_config?bss_account_id='+bss_id
            elif get_env() == 'test':
               url =test_config['DEFAULT_TEST_SERVICE_URL']+ \
                    '/v1/aigov/model_inventory/externalmodel_config?bss_account_id='+bss_id
            else:
               url =prod_config['DEFAULT_SERVICE_URL']+ \
                    '/v1/aigov/model_inventory/externalmodel_config?bss_account_id='+bss_id
        return url
    
    def _retrieve_user_profile_url(self, external_model_admin: str) -> str:
        if self._is_cp4d:
            url = self._cpd_configs['url'] + \
                  '/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin
        else:
            if get_env() == 'dev':
                 url =dev_config['DEFAULT_DEV_SERVICE_URL']+'/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin
            elif get_env() == 'test':
                 url =test_config['DEFAULT_TEST_SERVICE_URL']+'/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin
            else:
                url =prod_config['DEFAULT_SERVICE_URL']+'/v2/user_profiles?q=iam_id%20IN%20'+external_model_admin
        
        return url
                
    def _get_bss_id(self):
        try:
            token = self._facts_client._authenticator.token_manager.get_token() if ( isinstance(self._facts_client._authenticator, IAMAuthenticator) or (isinstance(self._facts_client.authenticator, CloudPakForDataAuthenticator))) else self._facts_client.authenticator.bearer_token
            decoded_bss_id = jwt.decode(token, options={"verify_signature": False})["account"]["bss"]
        except jwt.ExpiredSignatureError:
            raise
        return decoded_bss_id

    def _get_bss_id_cpd(self):
        decoded_bss_id="999"
        return decoded_bss_id

    def _update_props(self, data, bss_id, type_name):
        
        if self._is_cp4d:
            url = self._cpd_configs["url"] + \
                 '/v2/asset_types/'+type_name
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                '/v2/asset_types/'+type_name
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/asset_types/'+type_name
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/asset_types/'+type_name

        params = {"bss_account_id": bss_id}

        response = requests.put(url=url,
                                headers=self._get_headers(),
                                params=params,
                                data=json.dumps(data))

        if response.status_code == 401:
            _logger.exception("Expired token found.")
            raise
        elif response.status_code == 200 or response.status_code == 202:
            _logger.info("Custom facts definitions updated Successfully for account {}".format(bss_id))
        else:
            _logger.exception(
                "Error updating properties. ERROR {}. {}".format(response.status_code,response.text))
    
    def _get_current_assets_prop(self, asset_type):
        current_asset_prop=None
        
        if self._is_cp4d:
            cur_bss_id = self._get_bss_id_cpd()
        else:
            cur_bss_id = self._get_bss_id(self.api_key)

        params = {"bss_account_id": cur_bss_id}

        if self._is_cp4d:
            url = self._cpd_configs["url"] + \
                 '/v2/asset_types/'+ asset_type
        else:
        
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/asset_types/' + asset_type
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/asset_types/'+asset_type
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/asset_types'+asset_type

        response = requests.get(url=url,
                                headers=self._get_headers(),
                                params=params)

        if not response:
            _logger.exception("Current asset properties not found for type {}".format(asset_type))

        elif response.status_code == 403:
            _logger.exception(response.json()['message'])
            
        elif response.status_code == 401:
            _logger.exception("Expired token found.")
        
        elif response.status_code == 200:
            current_asset_prop = response.json()
        return current_asset_prop

    def _file_data_validation(self, name, props):

        if not name or not props['type'] or not props['label']:
            raise MissingValue("Property name or type or label")

        if props["type"].lower() != "string" and props["type"].lower() != "integer" and props["type"].lower() != "date":
            raise UnexpectedValue(
                "Only string, integer and date type is supported ")

        if (props["type"].lower() == "string") and (props["minimum"] != '' or props["maximum"] != ''):
            raise UnexpectedValue(
                "For String type, ONLY min and max length should be defined if applicable")

        if (props["type"].lower() == "integer") and (props["min_length"] != '' or props["max_length"] != ''):
            raise UnexpectedValue(
                "For Integer type, ONLY minimum and maximum value should be defined if applicable")

    def _get_props_from_file(self, data):
        props = {}
        fields = []
        global_search = []

        for _, row in data.iterrows():
            tmp_props = {}

            name = row["name"]
            tmp_props["type"] = row["type"]
            tmp_props["description"] = row["description"]
            tmp_props["placeholder"] = row["placeholder"]

            tmp_props["is_array"] = row["is_array"] or False
            tmp_props["required"] = row["required"] or True
            tmp_props["hidden"] = row["hidden"] or False
            tmp_props["readonly"] = row["readonly"] or False

            tmp_props["default_value"] = row["default_value"]
            tmp_props["minimum"] = row["minimum"]
            tmp_props["maximum"] = row["maximum"]
            tmp_props["min_length"] = row["min_length"]
            tmp_props["max_length"] = row["max_length"]
            tmp_props["label"] = {"default": row["label"], "en": row["label"]}
            is_searchable = row["is_searchable"] or False

            props[row["name"]] = tmp_props
            self._file_data_validation(name, tmp_props)

            if is_searchable is True:
                fields_prop = {}
                fields_prop["key"] = row["name"]
                fields_prop["type"] = row["type"]
                fields_prop["facet"] = False
                fields_prop["is_array"] = row["is_array"]
                fields_prop["search_path"] = row["name"]
                fields_prop["is_searchable_across_types"] = False

                fields.append(fields_prop)

                global_search.append(name)
        return props, fields, global_search

    def _format_data(self, csvFilePath, overwrite, asset_type,section_name):
        props = {}
        fields = []
        global_search = []
        csv_data = pd.read_csv(csvFilePath, sep=",", na_filter=False)

        if csv_data.empty:
            raise ClientError("File can not be empty")

        props, fields, global_search = self._get_props_from_file(csv_data)

        if overwrite:
            final_dict = {}
            final_dict["description"] = "The model fact user asset type to capture user defined attributes."
            final_dict["fields"] = fields
            final_dict["relationships"] = []
            final_dict["global_search_searchable"] = global_search
            final_dict["properties"] = props

            if asset_type == FactsType.MODEL_USECASE_USER:
                final_dict["decorates"] = [{"asset_type_name": "model_entry"}]

            if section_name:
                final_dict["localized_metadata_attributes"] = {"name": {"default": section_name, "en": section_name}}
            else:
                final_dict["localized_metadata_attributes"] = {"name": {"default": "Additional details", "en": "Additional details"}}

            return final_dict
        else:
            current_asset_props = self._get_current_assets_prop(asset_type)

            if current_asset_props and current_asset_props.get("properties"):

                if (current_asset_props["properties"] and props) or (not current_asset_props["properties"] and props):
                    current_asset_props["properties"].update(props)

                if (current_asset_props["fields"] and fields) or (not current_asset_props["fields"] and fields):
                    for field in fields:
                        current_asset_props["fields"].append(field)

                if (current_asset_props["global_search_searchable"] and global_search) or (not current_asset_props["global_search_searchable"] and global_search):
                    for global_search_item in global_search:
                        current_asset_props["global_search_searchable"].append(
                            global_search_item)
                entries_to_remove = ["name", "version", "scope"]
                list(map(current_asset_props.pop, entries_to_remove))

            elif current_asset_props and not current_asset_props.get("properties"):
                current_asset_props["properties"] = props
                if (current_asset_props["fields"] and fields) or (not current_asset_props["fields"] and fields):
                    for field in fields:
                        current_asset_props["fields"].append(field)

                if (current_asset_props["global_search_searchable"] and global_search) or (not current_asset_props["global_search_searchable"] and global_search):
                    for global_search_item in global_search:
                        current_asset_props["global_search_searchable"].append(
                            global_search_item)
                entries_to_remove = ["name", "version", "scope"]
                list(map(current_asset_props.pop, entries_to_remove))

            else:
                raise ClientError("Existing properties not found")

            return current_asset_props

    def _check_if_op_enabled(self):
        url=self._cpd_configs["url"] + "/v1/aigov/model_inventory/grc/config"
        response = requests.get(url,
                    headers=self._get_headers()
                    )

        if response.status_code==404:
            raise ClientError("Could not check if Openpages enabled in the platform or not. Make sure you have factsheet installed in same namespace as WKC/WSL. ERROR {}. {}".format(response.status_code,response.text))
        elif response.status_code==200:
            return response.json().get("grc_integration")
        else:
            raise ClientError("Failed not find openpages integrations config details. ERROR {}. {}".format(response.status_code,response.text))
    
    def _get_assets_url(self,asset_id:str=None,container_type:str=None,container_id:str=None):

        if self._is_cp4d:
            url = self._cpd_configs["url"] + \
                '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        return url


    
    #utils============================
    
    def _get_headers(self):
        token = self._facts_client._authenticator.token_manager.get_token() if  ( isinstance(self._facts_client._authenticator, IAMAuthenticator) or (isinstance(self._facts_client.authenticator, CloudPakForDataAuthenticator))) else self._facts_client.authenticator.bearer_token
        iam_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % token
        }
        return iam_headers 

    def _get_fact_definition_properties(self,fact_id):
        
        if self._facts_definitions:
            props=self._facts_definitions.get(PROPERTIES)
            props_by_id=props.get(fact_id)
        else:
            data=self.get_user_fact_definitions()
            props=data.get(PROPERTIES)
            props_by_id=props.get(fact_id)

        if not props_by_id:
            raise ClientError("Could not find properties for fact id {} ".format(fact_id))

        return props_by_id

    
    def _type_check_by_id(self,id,val):
        cur_type=self._get_fact_definition_properties(id).get("type")
        is_arr=self._get_fact_definition_properties(id).get("is_array")

        if cur_type=="integer" and not isinstance(val, int):
            raise ClientError("Invalid value used for type of Integer")
        elif cur_type=="string" and not isinstance(val, str) and not is_arr:
            raise ClientError("Invalid value used for type of String")
        elif (cur_type=="string" and is_arr) and (not isinstance(val, str) and not isinstance(val, list)) :
            raise ClientError("Invalid value used for type of String. Value should be either a string or list of strings")
    
    

    def _get_assets_url(self,asset_id:str=None,container_type:str=None,container_id:str=None):
       

        asset_id=asset_id or self._asset_id
        container_type=container_type or self._container_type
        container_id= container_id or self._container_id

        if self._is_cp4d:
            url = self._cpd_configs["url"] + \
                '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + \
                    '/v2/assets/' + asset_id + '?'+ container_type + '_id=' + container_id
        return url


    
    def create_model_usecase(self,catalog_id:str=None,name:str=None,description:str=None)-> ModelUsecaseUtilities:

        """
            Returns WKC Model usecase

            :param str catalog_id:  Catalog ID where this model usecase needs to create.
            :param str name: Name of model usecase
            :param str description: (Optional) Model usecase description

            :rtype: ModelUsecaseUtilities

            :return: WKC Model usecase asset
            
            Example:

            >>> client.assets.create_model_usecase(catalog_id=<catalog_id>,name=<model usecase name>,description=<model usecase description>)

        """

        if (catalog_id is None or catalog_id == ""):
            raise MissingValue("catalog_id", "catalog ID is missing")
        if (name is None or name == ""):
            raise MissingValue("name", "Model usecase name is missing")

        if catalog_id:
            validate_type(catalog_id, u'catalog_id', STR_TYPE, True)
        
        if name:
            body={
                    "name": name,
                    "description": description
                }
        else:
            raise ClientError("Provide model usecase name")

        url=self._get_create_usecase_url(catalog_id)

        response = requests.post(url,data=json.dumps(body), headers=self._get_headers())
        
        if response.status_code ==201:
            _logger.info("Model usecase created successfully")
            retResponse = response.json()
            retrieved_catalog_id = retResponse["metadata"]["catalog_id"]
            retrieved_asset_id = retResponse["metadata"]["asset_id"]
            self._current_model_usecase = ModelUsecaseUtilities(self,model_usecase_id=retrieved_asset_id,container_type=MODEL_USECASE_CONTAINER_TYPE_TAG,container_id=retrieved_catalog_id)
            return self._current_model_usecase
        else:
            raise ClientError("Failed while creating model usecase. ERROR {}. {}".format(response.status_code,response.text))

    def _get_create_usecase_url(self,catalog_id:str=None):
        
        usecase_url = '/v1/aigov/model_inventory/model_entries?catalog_id=' + catalog_id

        if self._is_cp4d:
            url = self._cpd_configs["url"] + usecase_url
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + usecase_url
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + usecase_url
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + usecase_url
        return url



    def get_ai_usecases(self, catalog_id:str=None)-> list:

        """
            Returns AI usecase assets

            :param str catalog_id:  (Optional) Catalog ID where AI usecase are registered. if not provided, dafault shows all AI usecases in all catalogs across all accounts to which the user has access.
            
            :rtype: list(AIUsecaseUtilities)

            :return: All AI usecase assets for a catalog

            Example:

            >>> client.assets.get_ai_usecases(catalog_id=<catalog_id>)
            >>> client.assets.get_ai_usecases()

        """

        if self._is_cp4d:
            raise ClientError("Mismatch: This functionality is only supported in SaaS IBM Cloud")
        
        return self.get_model_usecases(catalog_id, is_prompt=True)
    

    def get_model_usecases(self, catalog_id:str=None, is_prompt: bool=False)-> list:
        
        """
            Returns WKC Model usecase assets

            :param str catalog_id:  (Optional) Catalog ID where model usecase are registered. if not provided, dafault shows all model usecases in all catalogs across all accounts to which the user has access.
            
            :rtype: list(ModelUsecaseUtilities)

            :return: All WKC Model usecase assets for a catalog

            Example:

            >>> client.assets.get_model_usecases(catalog_id=<catalog_id>)
            >>> client.assets.get_model_usecases()

        """

        if catalog_id:
            validate_type(catalog_id, u'catalog_id', STR_TYPE, True)
            list_url=WKC_MODEL_LIST_FROM_CATALOG.format(catalog_id)
        else:
            list_url=WKC_MODEL_LIST_ALL

        if is_prompt:
            replace_name = "AI"
        else:
            replace_name = "model"
        
        if self._is_cp4d:
            url=self._cpd_configs["url"] + list_url
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + list_url
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + list_url
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + list_url
        
        response = requests.get(url,headers=self._get_headers())

        if response.status_code == 200:

            usecase_list = response.json()["results"]
            usecase_list_values = []
            for usecaseVal in usecase_list:
                retrieved_catalog_id = usecaseVal["metadata"]["catalog_id"]
                retrieved_asset_id = usecaseVal["metadata"]["asset_id"]

                if is_prompt:
                    usecase_list_values.append(AIUsecaseUtilities(self,model_usecase_id=retrieved_asset_id,container_type=MODEL_USECASE_CONTAINER_TYPE_TAG,container_id=retrieved_catalog_id))
                else:
                    usecase_list_values.append(ModelUsecaseUtilities(self,model_usecase_id=retrieved_asset_id,container_type=MODEL_USECASE_CONTAINER_TYPE_TAG,container_id=retrieved_catalog_id))
            _logger.info("{} usecases retrieved successfully".format(replace_name))
            return usecase_list_values
        else:
            error_msg = u'Usecase listing failed'
            reason = response.text
            _logger.info(error_msg)
            raise ClientError(error_msg + '. Error: ' + str(response.status_code) + '. ' + reason)


    def get_PAC_id(self)->str:

        """
            Get Platform Asset Catalog ( PAC ) ID.

            :rtype: PAC ID
            
            The way to use me is:
            
            >>> client.assets.get_PAC_id()
        
        """

        return self._get_pac_catalog_id()
    


    def get_attachment_definitions(self,type_name:str=None)->List:
         
        """
            Get all attachment fact definitions for model or model_usecase. Supported for CPD version >=4.6.5

            :return: All attachment fact definitions for model or model_usecase
            :rtype: list()

            The way to use me is:

            >>> client.assets.get_attachment_definitions(type_name=<model or model_usecase>)

        """

        if self._is_cp4d and self._cp4d_version < "4.6.5":
            raise ClientError("Version mismatch: Retrieving attachment fact definitions functionality is only supported in CP4D version 4.6.4.0 or higher. Current version of CP4D is "+self._cp4d_version)

        validate_enum(type_name, "type_name", AttachmentFactDefinitionType, True)
        
        url=self._get_attachment_definitions_url(type_name)

        response = requests.get(url, headers=self._get_headers())

        if response.status_code ==200:
            _logger.info("Attachment fact definitions retrieved successfully")
            return response.json()
        else:
            raise ClientError("Failed in retrieving attachment fact definitions. ERROR {}. {}".format(response.status_code,response.text))


    def _get_attachment_definitions_url(self,type_name:str=None):
        
        append_url = '/v1/aigov/factsheet/attachment_fact_definitions/' + type_name
        
        if self._is_cp4d:
            url = self._cpd_configs["url"] + append_url
        else:
            if get_env() == 'dev':
                url = dev_config["DEFAULT_DEV_SERVICE_URL"] + append_url
            elif get_env() == 'test':
                url = test_config["DEFAULT_TEST_SERVICE_URL"] + append_url
            else:
                url = prod_config["DEFAULT_SERVICE_URL"] + append_url

        return url
    

    def create_ai_usecase(self,catalog_id:str=None,name:str=None,description:str=None,status:str=None,risk:str=None,tags:list=None)-> AIUsecaseUtilities:

        """
            Returns AI usecase

            :param str catalog_id:  Catalog ID where this model usecase needs to create.
            :param str name: Name of model usecase
            :param str description: (Optional) Model usecase description
            :param str status: (Optional) AI Usecase status. It can be one of the following keywords: "draft", "awaiting development", "developed", "promoted to pre-production", "Deployed for validation", "Validated", "Approved", "Promoted to production", "Deployed for operation", "In operation", "Under revision", "Decommissioned"
            :param str risk: (Optional) AI Usecase risk. It can be one of the following keywords: "High", "Medium", "Low", "Custom", "None"
            :param list tags: (Optional) AI usecase tags. Provide list of tags, for example ["usecase for prod","model for prod"]

            :rtype: AIUsecaseUtilities

            :return: AI usecase asset
            
            Example:

            >>> client.assets.create_ai_usecase(catalog_id=<catalog_id>,name=<AI usecase name>,description=<AI usecase description>)

        """

        if self._is_cp4d:
            raise ClientError("Mismatch: This functionality is only supported in SaaS IBM Cloud")
    
        if (catalog_id is None or catalog_id == ""):
            raise MissingValue("catalog_id", "catalog ID is missing")
        if (name is None or name == ""):
            raise MissingValue("name", "AI usecase name is missing")
        if not (tags is None or tags == "") and not isinstance(tags, list):
            raise MissingValue("tags", "If AI usecase tags is provided then tags should be list of values")

        validate_enum(status,"Status", Status, False)
        validate_enum(risk,"Risk", Risk, False)
            
        if catalog_id:
            validate_type(catalog_id, u'catalog_id', STR_TYPE, True)
        
        if name:
            body={
                    "name": name
                }
        if description:
                body["description"] = description
        if status:
                body["status"] = status
        if risk:
                body["risk_level"] = risk
        if tags:
                body["tags"] = tags

        url=self._get_create_usecase_url(catalog_id)

        response = requests.post(url,data=json.dumps(body), headers=self._get_headers())
        
        if response.status_code ==201:
            _logger.info("AI usecase created successfully")
            retResponse = response.json()
            retrieved_catalog_id = retResponse["metadata"]["catalog_id"]
            retrieved_asset_id = retResponse["metadata"]["asset_id"]
            self._current_model_usecase = AIUsecaseUtilities(self,model_usecase_id=retrieved_asset_id,container_type=MODEL_USECASE_CONTAINER_TYPE_TAG,container_id=retrieved_catalog_id,facts_type="model_entry_user")
            return self._current_model_usecase
        else:
            raise ClientError("Failed while creating AI usecase. ERROR {}. {}".format(response.status_code,response.text))