# -*- coding: utf-8 -*-
import random

import logging

from typing import Union, List

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler,AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model.services.monetization import (EntitledState, PurchasableState, InSkillProductsResponse, Error,InSkillProduct)
from ask_sdk_model.interfaces.monetization.v1 import PurchaseResult
from ask_sdk_model import Response, IntentRequest
from ask_sdk_model.interfaces.connections import SendRequestDirective

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Data for the skill

# Static list of facts across 3 categories that serve as
# the free and premium content served by the Skill
all_facts = [
    {
        "type": "science",
        "fact": "The current status of NSO is:"
    },
    ]

skill_name = "Infinity Labs"

# Utility functions

def get_all_entitled_products(in_skill_product_list):
    """Get list of in-skill products in ENTITLED state."""
    # type: (List[InSkillProduct]) -> List[InSkillProduct]
    entitled_product_list = [ l for l in in_skill_product_list if (l.entitled == EntitledState.ENTITLED)]
    return entitled_product_list

def get_random_from_list(facts):
    """Return the fact message from randomly chosen list element."""
    # type: (List) -> str
    fact_item = random.choice(facts)
    return fact_item.get("fact")

def get_random_yes_no_question():
    """Return random question for YES/NO answering."""
    # type: () -> str
    questions = [
        "Do you want to know about current available automation packages, devices, VPN Or You want to create new vpn service.......?"
        ]
    return random.choice(questions)
    
def create_service():
    import json
    import time
    import requests
    """Return random question for YES/NO answering."""
    # type: () -> str
    code= requests.get("http://203.122.19.100:6661/api/operational/devices",headers={"Accept": "application/vnd.yang.data+json"},auth=("admin","admin"))
    y = code.json()
    w=y['tailf-ncs:devices']
    m=w['device']
    x=json.dumps(m)
    db=json.loads(x)
    items = []
    for item in db:
        items.append(item['name'])
    return "Please Provide the new vpn name....",items
    
def check_status():
    import json
    import time
    import requests
    code= requests.get('http://203.122.19.100:6661/api/running',auth=("admin","admin"))
    if (code.status_code == 200):
        return "The current status of Orchestrator is: running......."
    else:
        return "The current status of Orchestrator is not  running..........."
        
def package_info():
    import requests
    import time
    import json    
    code= requests.get("http://203.122.19.100:6661/api/operational/packages",headers={"Accept": "application/vnd.yang.data+json"},auth=("admin","admin"))
    y = code.json()
    w=y['tailf-ncs:packages']
    m=w['package']
    x=json.dumps(m)
    db=json.loads(x)
    items = []
    for item in db:
        items.append(item['name'])
    return "Current available packages are..",items
    
def welcome_script():
    return "Guest Welcome script I will provide in a while for any other question the answer will be as below:"
    
def get_random_config():
    """Return random config message."""
    # type: () -> str
    questions = [
        "Do you want to know more about NSO ?"
        ]
    return random.choice(questions)

def get_random_configure():
    """Return random config message."""
    # type: () -> str
    questions = [
        "Do you want to know more about NSO ?"
        ]
    return random.choice(questions)

def get_random_configs():
    """Return random config message."""
    # type: () -> str
    questions = [
        "Do you want to know more about NSO?"
        ]
    return random.choice(questions)
    
def get_random_configsz():
    """Return random config message."""
    # type: () -> str
    questions = [
        " "
        ]
    return random.choice(questions)    
    
def get_random_configz():
    """Return random config message."""
    # type: () -> str
    questions = [
        ""
        ]
    return random.choice(questions)
    
def service_info():
    import requests
    import time
    import json    
    code= requests.get("http://203.122.19.100:6661/api/operational/services",headers={"Accept": "application/vnd.yang.data+json"},auth=("admin","admin"))
    y = code.json()
    w=y['tailf-ncs:services']
    m=w['l2vpn1:l2vpn1']
    x=json.dumps(m)
    db=json.loads(x)
    items = []
    for item in db:
        items.append(item['name'])
    return "Current running services are" ,items
    
def delete_service(request):
    import requests
    import time
    import json
    code= requests.get("http://203.122.19.100:6661/api/operational/services",headers={"Accept": "application/vnd.yang.data+json"},auth=("admin","admin"))
    y = code.json()
    w=y['tailf-ncs:services']
    m=w['l2vpn1:l2vpn1']
    x=json.dumps(m)
    db=json.loads(x)
    items = []
    for item in db:
        items.append(item['name'])
    value = items
    slot_values = request.intent.slots["delete_service"].value
    for ext in value:
        if ext in slot_values:
            requests.delete("http://203.122.19.100:6661/api/running/services/l2vpn1/{}".format(slot_values) ,auth=("admin","admin"))
            return ("Service has been deleted")
        else :
            return ("Service name is not found ............ please try again")
    
def service_create(request):
    import requests
    import time
    import json
    import collections
    slot_device = request.intent.slots["device_name"].value
    slot_de = slot_device.upper()
    slot_dev = request.intent.slots["device_no"].value
    slot_d = slot_dev.upper()
    slot_value = request.intent.slots["Service_name"].value
    slot_val = request.intent.slots['pw_id'].value
    slot_loopback = request.intent.slots["loopback_ip"].value
    slot_interface = request.intent.slots['interface_number'].value
    slot_interfac = slot_interface.replace(' ', '/')
    slot_interf = request.intent.slots['interface_no'].value
    slot_inte = slot_interf.replace(' ','/')
    slot_remote = request.intent.slots['ip_address'].value
    
    payload = {
    "l2vpn1:l2vpn1": {
        "name": slot_value,
        "pw-id": slot_val,
        "link": [
            {
                "device": slot_de,
                "ios": {
                    "intf-number": str(slot_interfac)
                },
                "remote-ip": str(slot_remote)
            },
            {
                "device": slot_d,
                "iosxr": {
                    "intf-number": str(slot_inte)
                },
                "remote-ip": str(slot_loopback)
            }
         ]
        }
    }
    code = requests.post("http://203.122.19.100:6661/api/running/services/",headers={"Content-Type": "application/vnd.yang.data+json"}, auth=("admin","admin"), data=json.dumps(payload))
    code = requests.post("http://203.122.19.100:6661/api/running/services/",headers={"Content-Type": "application/vnd.yang.data+json"}, auth=("admin","admin"), json=payload)
    cod= requests.get("http://203.122.19.100:6661/api/running/services/l2vpn1/",headers={"Accept": "application/vnd.yang.collection+json"},auth=("admin","admin"))
    y = cod.json()
    w=y['collection']
    m=w['l2vpn1:l2vpn1']
    x=json.dumps(m)
    db=json.loads(x)
    items = []
    for item in db:
        items.append(item['pw-id'])
    if any(list == slot_val for list in items): 
        return "Pw-id has been already exist..... Please try again"
    elif (code.status_code == 400):
        return "Service is not created... Please try again"
    else :
        return "Service has been created"
    
def device_info():
    import requests
    import time
    import json    
    code= requests.get("http://203.122.19.100:6661/api/operational/devices",headers={"Accept": "application/vnd.yang.data+json"},auth=("admin","admin"))
    y = code.json()
    w=y['tailf-ncs:devices']
    m=w['device']
    x=json.dumps(m)
    db=json.loads(x)
    items = []
    for item in db:
        items.append(item['name'])
    return "Current running devices are",items

def get_random_goodbye():
    """Return random goodbye message."""
    # type: () -> str
    goodbyes = ["OK.  Goodbye!", "Have a great day!", "Come back again soon!"]
    return random.choice(goodbyes)

def get_speakable_list_of_products(entitled_products_list):
    """Return product list in speakable form."""
    # type: (List[InSkillProduct]) -> str
    product_names = [item.name for item in entitled_products_list]
    if len(product_names) > 1:
        # If more than one, add and 'and' in the end
        speech = " and ".join(
            [", ".join(product_names[:-1]), product_names[-1]])
    else:
        # If one or none, then return the list content in a string
        speech = ", ".join(product_names)
    return speech

def get_resolved_value(request, slot_name):
    """Resolve the slot name from the request using resolutions."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return (request.intent.slots[slot_name].resolutions.resolutions_per_authority[0].values[0].value.name)
    except (AttributeError, ValueError, KeyError, IndexError):
        return None

def get_spoken_value(request, slot_name):
    """Resolve the slot to the spoken value."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return request.intent.slots[slot_name].value
    except (AttributeError, ValueError, KeyError, IndexError):
        return None

def in_skill_product_response(handler_input):
    """Get the In-skill product response from monetization service."""
    # type: (HandlerInput) -> Union[InSkillProductsResponse, Error]
    locale = handler_input.request_envelope.request.locale
    ms = handler_input.service_client_factory.get_monetization_service()
    return ms.get_in_skill_products(locale)

# Skill Handlers

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Launch Requests.

    The handler gets the in-skill products for the user, and provides
    a custom welcome message depending on the ownership of the products
    to the user.
    User says: Alexa, open <skill_name>.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")

        in_skill_response = in_skill_product_response(handler_input)
        if isinstance(in_skill_response, InSkillProductsResponse):
            entitled_prods = get_all_entitled_products(in_skill_response.in_skill_products)
            if entitled_prods:
                speech = (
                    "Welcome to {}. You currently own {} products. "
                    "To hear a random fact, you could say, 'Tell me a fact', "
                    "or you can ask for a specific category you have "
                    "purchased, for example, say 'Tell me a science fact'. "
                    "To know what else you can buy, say, 'What can i buy?'. "
                    "So, what can I help you with?").format(skill_name,get_speakable_list_of_products(entitled_prods))
            else:
                logger.info("No entitled products")
                speech = (
                    "Hello.......Welcome to InfinityLabs.... A Technology "
                    "consulting and Software Solutions Company. Providing"
                    "expert IT services in the areas of Automation,"
                    "Network Design and Deployment, IT Security,"
                    "Data Centre Management, Cloud computing,"
                    "Virtualization, machine learning and analytic,....."
                    "What would you want me to help you with today ?"
                    ).format(skill_name)
            reprompt = "I didn't catch that. What can I help you with?"
        else:
            logger.info("Error calling InSkillProducts API: {}".format(in_skill_response.message))
            speech = "Something went wrong in loading your purchase history."
            reprompt = speech

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class WelcomeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WelcomeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("WelcomeIntentHandler")
        fact_rest = welcome_script()
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_configsz())).ask(get_random_configsz()).response
        
        
class YesHandler(AbstractRequestHandler):
    """If the user says Yes, they want another fact."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In YesHandler")
        fact_text = get_random_from_list(all_facts)
        fact_rest = check_status()
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_yes_no_question())).ask(get_random_yes_no_question()).response
        

class NoHandler(AbstractRequestHandler):
    """If the user says No, then the skill should be exited."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NoHandler")
        return handler_input.response_builder.speak(get_random_goodbye()).set_should_end_session(True).response


class RouterinformationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RouterinformationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RouterinformationHandler")
        fact_rest = package_info()
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_configsz())).ask(get_random_configsz()).response
    

class ServicesinformationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ServicesinformationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ServicesinformationHandler")
        fact_rest = service_info()
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_configsz())).ask(get_random_configsz()).response


class CreateserviceHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CreateserviceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CreateserviceHandler")
        fact_rest = create_service()
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_configz())).ask(get_random_configz()).response


class DeviceinformationHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeviceinformationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In DeviceinformationHandler")
        fact_rest = device_info()
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_configsz())).ask(get_random_configsz()).response

        
class CancelSubscriptionHandler(AbstractRequestHandler):
    """
    Following handler demonstrates how Skills would receive Cancel requests
    from customers and then trigger a cancel request to Alexa
    User says: Alexa, ask premium facts to cancel <product name>
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CancelSubscriptionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelSubscriptionHandler")

        in_skill_response = in_skill_product_response(handler_input)
        if in_skill_response:
            product_category = get_resolved_value(handler_input.request_envelope.request, "productCategory")

            # No entity resolution match
            if product_category is None:
                product_category = "all_access"
            else:
                product_category += "_pack"

            product = [l for l in in_skill_response.in_skill_products
                       if l.reference_name == product_category]
            return handler_input.response_builder.add_directive(
                SendRequestDirective(
                    name="Cancel",
                    payload={
                        "InSkillProduct": {
                            "productId": product[0].product_id
                        }
                    },
                    token="correlationToken")
            ).response


class BuyResponseHandler(AbstractRequestHandler):
    """This handles the Connections.Response event after a buy occurs."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Buy")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In BuyResponseHandler")
        in_skill_response = in_skill_product_response(handler_input)
        product_id = handler_input.request_envelope.request.payload.get("productId")

        if in_skill_response:
            product = [l for l in in_skill_response.in_skill_products
                       if l.product_id == product_id]
            logger.info("Product = {}".format(str(product)))
            if handler_input.request_envelope.request.status.code == "200":
                speech = None
                reprompt = None
                purchase_result = handler_input.request_envelope.request.payload.get(
                    "purchaseResult")
                if purchase_result == PurchaseResult.ACCEPTED.value:
                    category_facts = all_facts
                    if product[0].reference_name != "all_access":
                        category_facts = [l for l in all_facts if
                                          l.get("type") ==
                                          product[0].reference_name.replace(
                                              "_pack", "")]
                    speech = ("You have unlocked the {}.  Here is your {} "
                              "fact: {}  {}").format(
                        product[0].name,
                        product[0].reference_name.replace(
                            "_pack", "").replace("all_access", ""),
                        get_random_from_list(category_facts),
                        get_random_yes_no_question())
                    reprompt = get_random_yes_no_question()
                elif purchase_result in (
                        PurchaseResult.DECLINED.value,
                        PurchaseResult.ERROR.value,
                        PurchaseResult.NOT_ENTITLED.value):
                    speech = ("Thanks for your interest in {}.  "
                              "Would you like another random fact?".format(
                        product[0].name))
                    reprompt = "Would you like another random fact?"
                elif purchase_result == PurchaseResult.ALREADY_PURCHASED.value:
                    logger.info("Already purchased product")
                    speech = " Do you want to hear a fact?"
                    reprompt = "What can I help you with?"
                else:
                    # Invalid purchase result value
                    logger.info("Purchase result: {}".format(purchase_result))
                    return FallbackIntentHandler().handle(handler_input)

                return handler_input.response_builder.speak(speech).ask(
                    reprompt).response
            else:
                logger.log("Connections.Response indicated failure. "
                           "Error: {}".format(
                    handler_input.request_envelope.request.status.message))

                return handler_input.response_builder.speak(
                    "There was an error handling your purchase request. "
                    "Please try again or contact us for help").response


class CancelResponseHandler(AbstractRequestHandler):
    """This handles the Connections.Response event after a cancel occurs."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Cancel")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelResponseHandler")
        in_skill_response = in_skill_product_response(handler_input)
        product_id = handler_input.request_envelope.request.payload.get(
            "productId")

        if in_skill_response:
            product = [l for l in in_skill_response.in_skill_products
                       if l.product_id == product_id]
            logger.info("Product = {}".format(str(product)))
            if handler_input.request_envelope.request.status.code == "200":
                speech = None
                reprompt = None
                purchase_result = handler_input.request_envelope.request.payload.get(
                        "purchaseResult")
                purchasable = product[0].purchasable
                if purchase_result == PurchaseResult.ACCEPTED.value:
                    speech = ("You have successfully cancelled your "
                              "subscription. {}".format(
                        get_random_yes_no_question()))
                    reprompt = get_random_yes_no_question()

                if purchase_result == PurchaseResult.DECLINED.value:
                    if purchasable == PurchasableState.PURCHASABLE:
                        speech = ("You don't currently have a "
                              "subscription. {}".format(
                            get_random_yes_no_question()))
                    else:
                        speech = get_random_yes_no_question()
                    reprompt = get_random_yes_no_question()

                return handler_input.response_builder.speak(speech).ask(
                    reprompt).response
            else:
                logger.log("Connections.Response indicated failure. "
                           "Error: {}".format(
                    handler_input.request_envelope.request.status.message))

                return handler_input.response_builder.speak(
                        "There was an error handling your cancellation "
                        "request. Please try again or contact us for "
                        "help").response
                        
    
class UpsellResponseHandler(AbstractRequestHandler):
    """This handles the Connections.Response event after an upsell occurs."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("Connections.Response")(handler_input) and
                handler_input.request_envelope.request.name == "Upsell")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In UpsellResponseHandler")

        if handler_input.request_envelope.request.status.code == "200":
            if handler_input.request_envelope.request.payload.get(
                    "purchaseResult") == PurchaseResult.DECLINED.value:
                speech = ("Ok. Here's a random fact: {} {}".format(
                    get_random_from_list(all_facts),
                    get_random_yes_no_question()))
                reprompt = get_random_yes_no_question()
                return handler_input.response_builder.speak(speech).ask(reprompt).response
        else:
            logger.log("Connections.Response indicated failure. "
                       "Error: {}".format(
                handler_input.request_envelope.request.status.message))
            return handler_input.response_builder.speak(
                "There was an error handling your Upsell request. "
                "Please try again or contact us for help.").response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help message to users."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        in_skill_response = in_skill_product_response(handler_input)

        if isinstance(in_skill_response, InSkillProductsResponse):
            speech = (
                "To hear about NSO you can say "
                "'infinity', or to hear about How to create a NSO service using CLI, 'Please follow cisco documents' "
            )
            reprompt = "I didn't catch that. What can I help you with?"
        else:
            logger.info("Error calling InSkillProducts API: {}".format(
                in_skill_response.message))
            speech = "Something went wrong in loading your purchase history."
            reprompt = speech
        return handler_input.response_builder.speak(speech).ask(reprompt).response

class ServiceNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ServiceNameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ServiceNameIntentHandler")
        fact_rest = service_create(handler_input.request_envelope.request)
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_configsz())).ask(get_random_configsz()).response
        
class DeleteserviceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DeleteserviceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In DeleteserviceIntentHandler")
        fact_rest = delete_service(handler_input.request_envelope.request)
        return handler_input.response_builder.speak("{} {}".format(fact_rest,get_random_configsz())).ask(get_random_configsz()).response        
    
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for fallback intent.

    2018-July-12: AMAZON.FallbackIntent is currently available in all
    English locales. This handler will not be triggered except in that
    locale, so it can be safely deployed for any locale. More info
    on the fallback intent can be found here: https://developer.amazon.com/docs/custom-skills/standard-built-in-intents.html#fallback
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = (
                "Sorry. I cannot help with that."
                "..........."
                "To hear about N S O you can say,. 'infinity' "
                "............Or say....."
                "'Help me'...... "
            )
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(
            reprompt).response


class SessionEndedHandler(AbstractRequestHandler):
    """Handler for session end request, stop or cancel intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("SessionEndedRequest")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("AMAZON.CancelIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedHandler")
        return handler_input.response_builder.speak(
            get_random_goodbye()).set_should_end_session(True).response

# Skill Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """One exception handler to catch all exceptions."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, I can't understand the command. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

# Request and Response Loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info("Request Envelope: {}".format(
            handler_input.request_envelope))

class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info("Response: {}".format(response))


sb = StandardSkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(YesHandler())
sb.add_request_handler(NoHandler())
sb.add_request_handler(RouterinformationHandler())
sb.add_request_handler(BuyResponseHandler())
sb.add_request_handler(CancelResponseHandler())
sb.add_request_handler(UpsellResponseHandler())
sb.add_request_handler(ServicesinformationHandler())
sb.add_request_handler(CreateserviceHandler())
sb.add_request_handler(DeviceinformationHandler())
sb.add_request_handler(CancelSubscriptionHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedHandler())
sb.add_request_handler(ServiceNameIntentHandler())
sb.add_request_handler(DeleteserviceIntentHandler())
sb.add_request_handler(WelcomeIntentHandler())

sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()