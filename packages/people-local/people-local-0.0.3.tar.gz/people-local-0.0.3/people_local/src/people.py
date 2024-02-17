from functools import wraps
import inspect
from dotenv import load_dotenv
from contact_group_local.contact_group import ContactGroup
from logger_local.Logger import Logger
from .people_constants import PeopleLocalConstants

load_dotenv()


logger = Logger.create_logger(
    object=PeopleLocalConstants.PEOPLE_LOCAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)


# TODO Shall we inherit from GroupsRemote?
# TODO Should person, profile, contact and user inherit PeopleLocal or not?
class PeopleLocal():
    def __init__(self):
        pass


    def process_first_name(self, original_first_name: str, method, **kwargs) -> str:
        logger.start(object={'original_first_name': original_first_name})
        try:
            first_name = ''.join(
                [i for i in original_first_name if not i.isdigit()])
            normalized_first_name = first_name.split()[0]
            logger.info("normalized_first_name", object={
                        'normalized_first_name': normalized_first_name})
            kwargs['entity_name'] = normalized_first_name
            method(**kwargs)
        except Exception as e:
            logger.error("error processing first name", object={
                         'original_first_name': original_first_name, 'error': e})
            raise e

        # TODO Please use GenericCrudMl to update person.first_name_table

        # TODO Create group to all people with the same first name and add this contact/profile to the group
        
        logger.end("success processing first name",
                   object={'normalized_first_name': normalized_first_name})
        return normalized_first_name


    def process_last_name(self, original_last_name: str, method, **kwargs) -> str:
        # TODO logger.start() should include all parameters - Please update all methods.
        logger.start(object={'original_last_name': original_last_name})
        try:
            last_name = ''.join(
                [i for i in original_last_name if not i.isdigit()])
            normalized_last_name = last_name.split()[0]
            logger.info("normalized_last_name", object={
                        'normalized_last_name': normalized_last_name})
            kwargs['entity_name'] = normalized_last_name
            method(**kwargs)
        except Exception as e:
            logger.error("error processing last name", object={
                         'original_last_name': original_last_name, 'error': e})
            raise e
        logger.end("success processing last name",
                   object={'normalized_last_name': normalized_last_name})

        # TODO Create a group to the family and add this contact/profile to the group

        return normalized_last_name


    def process_organization(self, organization_name: str, email_address: str, method, **kwargs) -> str:
        logger.start(object={'organization_name': organization_name})
        try:
            if organization_name is None or organization_name == "":
                organization_name = self.extract_organization_from_email_address(
                    email_address=email_address)
                kwargs['entity_name'] = organization_name
            else:
                kwargs['entity_name'] = organization_name
            result = method(**kwargs)
        except Exception as e:
            logger.error("error processing organization", object={
                         'organization_name': organization_name, 'error': e})
            raise e
        logger.end("success processing organization",
                   object={'result': result})
        return result

    def extract_organization_from_email_address(self, email_address: str) -> str:
        logger.start(object={'email_address': email_address})
        try:
            organization_name = email_address.split('@')[1].split('.')[0]
        except Exception as e:
            logger.error("error extracting organization from email address", object={
                         'email_address': email_address, 'error': e})
            raise e
        logger.end("success extracting organization from email address",
                   object={'organization_name': organization_name})
        return organization_name

    def extract_organization_from_url(self, url: str) -> str:
        logger.start(object={'url': url})
        try:
            organization_name = url.split('.')[1]
        except Exception as e:
            logger.error("error extracting organization from url", object={
                         'url': url, 'error': e})
            raise e
        logger.end("success extracting organization from url",
                   object={'organization_name': organization_name})
        return organization_name

