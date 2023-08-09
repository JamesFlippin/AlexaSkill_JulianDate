# -*- coding: utf-8 -*-

# Programmer: James Flippin
# About me: https://JamesFlippin.github.io
# GitHub profile page: https://github.com/JamesFlippin
# GitHub Source Code for this skill can be found at: https://github.com/JamesFlippin/AlexaSkill_JulianDate
# License: GNU GENERAL PUBLIC LICENSE, Version 3
# Version: 2023-08-09

# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This code is built/based on using the handler classes approach in skill builder.

# -------------------------------------------------
# Imports - My additional imports
# -------------------------------------------------
import datetime
from datetime import date
import calendar
# -------------------------------------------------
# -------------------------------------------------

# -------------------------------------------------
# Imports - Alexa Standard
# -------------------------------------------------
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
# -------------------------------------------------
# -------------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# -------------------------------------------------
# My Added Class for AboutIntentHandler()
# -------------------------------------------------
class AboutIntentHandler(AbstractRequestHandler):
    """Handler for About Intent. Tells the skill user a little about me and how they can find out more about me."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("about")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output="This skill was written by James Flippin as an Amazon Alexa skills learning experience. It was inspired by Dawn, who is the inspiration for so much of what I do. For more information about me please visit https://JamesFlippin.github.io"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# My Added Class for IsYearALeapYearIntentHandler()
# -------------------------------------------------
class IsYearALeapYearIntentHandler(AbstractRequestHandler):
    """Handler for IsYearALeapYear Intent. It checks to see if the user provided year (number) is a leap year or not."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("IsYearALeapYear")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Create an object to reference and retrieve slot variable values
        slots = handler_input.request_envelope.request.intent.slots
        # Convert the user provided year slot value to an integer value, we are relying on the Amazon.number
        # data type and the model to prevent non-numbers being provided
        userYear = int(slots["userYear"].value)

        futureTag = "" # Just for fun, a variable to hold additional output text if the date is substantially in the future
        
        #Gregorian calendar - https://en.wikipedia.org/wiki/Gregorian_calendar
        # The current Gregorian calendar went into effect in October 1582 October 1582, so lets not look before 1582
        if userYear < 1582:
            speak_output = "I'm sorry, but the current Gregorian calendar went into effect in October 1582 AD."
            speak_output += "Please choose a date that is after 1528 AD. "
            speak_output += "For more information on the Gregorian calendar and leap years, please visit 'Gregorian Calender' on www.wikipedia.org"
        else:
            # A little fun for someone asking about the future
            if userYear > 2232: # Captain Kirk
                futureTag = " Wow! You must be from the future. Say 'Hi'! to Captain Kirk for me, he was born March 22, 2233."
                
            # Logic below courtesy of ChatGPT and OpenAI (https://chat.openai.com)
            # Check to see if the year is divisible by 4 and not divisible by 100, or if it's divisible by 400
            if (userYear % 4 == 0 and userYear % 100 != 0) or (userYear % 400 == 0):
                speak_output = str(userYear) + " is a leap year." + futureTag # It is a leap year 
            else:
                speak_output = str(userYear) + " is not a leap year." + futureTag # It isn't a leap year

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# My Added Class for getJulianDateIntentHandler()
# -------------------------------------------------
class getJulianDateIntentHandler(AbstractRequestHandler):
    """Handler for getJulianDate Intent. It uses the current date value to provide feedback on the current date and Julian Date."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("getJulianDate")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # new Output
        speak_output="For " + date.today().strftime('%B %d %Y')  + " the Julian Date is " + date.today().strftime('%j')

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# My modified default Alexa LaunchRequestHandler()
# -------------------------------------------------
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch. It gives an imediate response with the current date and Julian datae and also informs the user of specific response options for this Alexa skill"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # New Output
        speak_output="Welcome, for " + date.today().strftime('%B %d %Y')  + ", the Julian Date is " + date.today().strftime('%j') + ". Commands you can say are: 'Current Julian Date' or 'For Today' or 'Today' or 'About'. You can also ask 'Is [year number, such as 2024] a leap year?' Which would you like to try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
# -------------------------------------------------
# -------------------------------------------------

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Commands you can say are: 'Current Julian Date' or 'For Today' or 'Today' or 'About'. You can also ask 'Is [year number, such as 2024] a leap year?' How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

# -------------------------------------------------
# Added My custom Handlers for this skill
# -------------------------------------------------
sb.add_request_handler(getJulianDateIntentHandler()) # Added Handler for AboutIntentHandler()
sb.add_request_handler(AboutIntentHandler()) # Added Handler for AboutIntentHandler()
sb.add_request_handler(IsYearALeapYearIntentHandler()) # Added Handler for IsYearALeapYearIntentHandler()
# -------------------------------------------------
# -------------------------------------------------

# -------------------------------------------------
# Default Alexa Skill handlers
# -------------------------------------------------
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
