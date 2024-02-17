from .action_items_local_constants import ACTION_ITEMS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT
from logger_local.LoggerLocal import Logger
from database_mysql_local.generic_mapping import GenericMapping
from database_mysql_local.generic_crud_ml import GenericCRUDML
from user_context_remote.user_context import UserContext
from language_remote.lang_code import LangCode


DEFAULT_SCHEMA_NAME = 'action_item'
DEFAULT_ENTITY_NAME1 = 'action_item'
DEFAULT_ENTITY_NAME2 = 'contact'
DEFAULT_TABLE_NAME = 'action_item_table'
DEFAULT_ID_COLUMN_NAME = 'action_item_id'
DEFAULT_MAPPING_ID_COLUMN_NAME = 'action_item_contact_id'
DEFAULT_MAPPING_TABLE_NAME = 'action_item_contact_table'

logger = Logger.create_logger(object=ACTION_ITEMS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)
user_context = UserContext()


class ActionItemsLocal(GenericMapping, GenericCRUDML):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2,
                 default_id_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME,
                 default_mapping_id_column_name: str = DEFAULT_MAPPING_TABLE_NAME,
                 default_mapping_table_name: str = DEFAULT_MAPPING_TABLE_NAME,
                 is_test_data: bool = False):

        GenericMapping.__init__(
            self, default_schema_name=default_schema_name, default_entity_name1=default_entity_name1,
            default_entity_name2=default_entity_name2, default_id_column_name=default_mapping_id_column_name,
            default_table_name=default_mapping_table_name,
            is_test_data=is_test_data
        )

        GenericCRUDML.__init__(
            self, default_schema_name=default_schema_name, default_id_column_name=default_id_column_name,
            default_table_name=default_table_name, is_test_data=is_test_data
        )

    def insert_link_action_item_contact(self, data_action_item: dict, contact_id: int,
                                        lang_code: LangCode = None) -> int:
        """
        Insert link action item contact
        :param data_action_item: dict
        :param lang_code: LangCode
        :param contact_id: int
        :return: int
        """
        logger.start(object={"data_action_item": data_action_item, "lang_code": lang_code, "contact_id": contact_id})
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        data_json = {
            'created_user_id': user_context.get_effective_user_id(),
            'updated_user_id': user_context.get_effective_user_id(),
        }
        data_action_item['created_user_id'] = user_context.get_effective_user_id()
        data_action_item['updated_user_id'] = user_context.get_effective_user_id()
        action_item_id, action_item_ml_id = self.add_value(data_ml_json=data_action_item, lang_code=lang_code, data_json=data_json)
        action_item_contact_id = self.insert_mapping(entity_id1=action_item_id, entity_id2=contact_id, ignore_duplicate=True)
        insert_information = {
            "action_item_id": action_item_id,
            "action_item_ml_id": action_item_ml_id,
            "action_item_contact_id": action_item_contact_id
        }
        logger.end(object={"action_item_id": action_item_id, "action_item_ml_id": action_item_ml_id,
                           "action_item_contact_id": action_item_contact_id})
        return insert_information
