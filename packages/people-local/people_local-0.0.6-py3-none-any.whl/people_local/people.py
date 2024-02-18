import re
from dotenv import load_dotenv
from logger_local.Logger import Logger
from .people_constants import PeopleLocalConstants

load_dotenv()


logger = Logger.create_logger(
    object=PeopleLocalConstants.PEOPLE_LOCAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

# TODO Move to group-local repo
VENTURE_CAPITAL_GROUP_ID = 50001177


# TODO Should person, profile, contact and user inherit PeopleLocal or not?
class PeopleLocal():
    def __init__(self, first_name: str = None, last_name: str = None, full_organization_name: str = None,
                 short_organization_name: str = None, email_address: str = None, url: str = None):
        logger.start(
            object={
                'first_name': first_name, 'last_name': last_name,
                'full_organization_name': full_organization_name,
                'short_organization_name': short_organization_name, 
                'email_address': email_address, 'url': url}
        )
        self.first_name = first_name
        self.last_name = last_name
        self.full_organization_name = full_organization_name
        self.short_organization_name = short_organization_name
        self.email_address = email_address
        self.url = url
        if self.first_name is None or self.first_name == "":
            self.first_name = self.__extract_first_name_from_email_address()
        if self.full_organization_name is None or self.full_organization_name == "":
            self.full_organization_name = self.__extract_full_organization_name_from_email_address()
        if self.short_organization_name is None or self.short_organization_name == "":
            self.short_organization_name = self.__extract_short_organization_name_from_full_organization_name()
        logger.end()

    def _process_first_name(self, method, **kwargs) -> str:
        logger.start()
        try:
            first_name = ''.join(
                [i for i in self.first_name if not i.isdigit()])
            normalized_first_name = first_name.split()[0]
            logger.info("normalized_first_name", object={
                        'normalized_first_name': normalized_first_name})
            kwargs['entity_name'] = normalized_first_name
            method(**kwargs)
        except Exception as e:
            logger.error("error processing first name", object={
                         'self.first_name': self.first_name, 'error': e})
            raise e

        # TODO Please use GenericCrudMl to update person.first_name_table

        # TODO Create group to all people with the same first name and add this contact/profile to the group

        logger.end("success processing first name",
                   object={'normalized_first_name': normalized_first_name})
        return normalized_first_name

    def _process_last_name(self, method, **kwargs) -> str:
        # TODO logger.start() should include all parameters - Please update all methods.
        logger.start()
        try:
            last_name = ''.join(
                [i for i in self.last_name if not i.isdigit()])
            normalized_last_name = last_name.split()[0]
            logger.info("normalized_last_name", object={
                        'normalized_last_name': normalized_last_name})
            kwargs['entity_name'] = normalized_last_name
            method(**kwargs)
        except Exception as e:
            logger.error("error processing last name", object={
                         'self.last_name': self.last_name, 'error': e})
            raise e
        logger.end("success processing last name",
                   object={'normalized_last_name': normalized_last_name})

        # TODO Create a group to the family and add this contact/profile to the group

        return normalized_last_name

    def _process_organization(self, method, **kwargs) -> str:
        logger.start()
        try:
            kwargs['entity_name'] = self.full_organization_name
            if "Ventures" in self.full_organization_name:
                kwargs['group_id'] = VENTURE_CAPITAL_GROUP_ID
            result = method(**kwargs)
        except Exception as e:
            logger.error("error processing organization", object={
                         'self.full_organization_name': self.full_organization_name, 'error': e})
            raise e
        logger.end("success processing organization",
                   object={'result': result})
        return result

    def __extract_full_organization_name_from_email_address(self) -> str:
        logger.start()
        if self.email_address is None:
            logger.warning(log_message="email address is None")
            return None
        domain_part = self.email_address.split('@')[-1]         
        organization_name_parts = domain_part.rsplit('.', 1)[0]
        organization_name = ' '.join(part for part in organization_name_parts.split('.'))
        logger.end(object={'organization_name': organization_name})
        return organization_name.capitalize()

    #  short_organization_name is full_organization_name without "Ltd", "Inc" ...
    def __extract_short_organization_name_from_full_organization_name(self) -> str:
        logger.start()
        if self.full_organization_name is None:
            logger.warning(log_message="full_organization_name is None")
            return None
        pattern = re.compile(r'\b(?:Ltd|Inc|Corporation|Corp|LLC|L.L.C.|GmbH|AG|S.A.|SARL)\b\.?', re.IGNORECASE)
        short_organization_name = re.sub(pattern, '', self.full_organization_name).strip()
        short_organization_name = re.sub(r',\s*$', '', short_organization_name).strip()
        logger.end(object={'short_organization_name': short_organization_name})
        return short_organization_name

    def __extract_full_organization_name_from_url(self, url: str) -> str:
        logger.start()
        if url is None:
            logger.warning(log_message="url is None")
            return None
        organization_name = url.split('//')[-1].split('.')[0]
        logger.end(object={'organization_name': organization_name})
        return organization_name.capitalize()

    def __extract_first_name_from_email_address(self) -> str:
        logger.start()
        if self.email_address is None:
            logger.warning(log_message="email address is None")
            return None
        local_part = self.email_address.split('@')[0]

        for separator in ['.', '_']:
            if separator in local_part:
                first_name = local_part.split(separator)[0]
                break
        else:
            first_name = local_part

        logger.end(object={'first_name': first_name})
        return first_name.capitalize()
