# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

##############################################################

# from typing import List
# from rasa_core_sdk.forms import FormAction, EntityFormField
# from rasa_core_sdk.events import SlotSet
# from requests import (
#     ConnectionError,
#     HTTPError,
#     TooManyRedirects,
#     Timeout
# )
# from api import get_weather_by_day

# class ActionReportWeather(FormAction):
#     RANDOMIZE = True

#     def name(self):
#         # type: () -> Text
#         return "action_report_weather"

#     @staticmethod
#     def required_fields():
#         return [
#             EntityFormField("address", "address"),
#             EntityFormField("date-time", "date-time"),
#         ]

#     def submit(self, dispatcher, tracker, domain):
#         # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
#         address = tracker.get_slot('address')
#         date_time = tracker.get_slot('date-time')

#         date_time_number = text_date_to_number_date(date_time)

#         if isinstance(date_time_number, str):  # parse date_time failed
#             return [SlotSet("matches", "暂不支持查询 {} 的天气".format([address, date_time_number]))]
#         else:
#             weather_data = get_text_weather_date(address, date_time, date_time_number)
#             return [SlotSet("matches", "{}".format(weather_data))]

##############################################################

# This means that forms are no longer implemented using a FormAction, but instead defined in the domain. 
# Any customizations around requesting slots or slot validation can be handled with a FormValidationAction.
# https://rasa.com/docs/rasa/migration-guide/#forms-1

#from typing import List
#from rasa_core_sdk.forms import FormAction, EntityFormField

from rasa_sdk.events import SlotSet

from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)
from api import get_weather_by_day

from typing import Text, List, Any, Dict, Union
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import FormValidationAction
from rasa_sdk.types import DomainDict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

print('---------------------------------------')

# class ActionReportWeather(FormValidationAction):
#     def name(self) -> Text:
#         return "action_report_weather"

#     @staticmethod
#     def cuisine_db() -> List[Text]:
#         """Database of supported cuisines"""
#         return ["caribbean", "chinese", "french"]

#     def validate_cuisine(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate cuisine value."""

#         if slot_value.lower() in self.cuisine_db():
#             # validation succeeded, set the value of the "cuisine" slot to value
#             return {"cuisine": slot_value}
#         else:
#             # validation failed, set this slot to None, meaning the
#             # user will be asked for the slot again
#             return {"cuisine": None}

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_report_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        address = tracker.get_slot('address')
        date_time = tracker.get_slot('date-time')

        print(address)
        print(date_time)

        # print(tracker.slot.get('address'))
        # print(tracker.slot.get('date-time'))
        # dispatcher.utter_message(text="今天上海天气晴天，气温22度。")

        date_time_number = text_date_to_number_date(date_time)

        if isinstance(date_time_number, str):  # parse date_time failed
            return [SlotSet("matches", "暂不支持查询 {} 的天气".format([address, date_time_number]))]
        else:
            weather_data = get_text_weather_date(address, date_time, date_time_number)
            return [SlotSet("matches", "{}".format(weather_data))]

        #return []


##############################################################

def get_text_weather_date(address, date_time, date_time_number):
    try:
        result = get_weather_by_day(address, date_time_number)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """
            {} {} ({}) 的天气情况为：白天：{}；夜晚：{}；气温：{}-{} °C
        """
        text_message = text_message_tpl.format(
            result['location']['name'],
            date_time,
            result['result']['date'],
            result['result']['text_day'],
            result['result']['text_night'],
            result['result']["high"],
            result['result']["low"],
        )
    return text_message


def text_date_to_number_date(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return text_date

    if text_date.startswith("星期"):
        # TODO: using calender to compute relative date
        return text_date

    if text_date.startswith("下星期"):
        # TODO: using calender to compute relative date
        return text_date

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return text_date
    if text_date == "前天":
        return text_date
    if text_date == "大前天":
        return text_date
