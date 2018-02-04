from telegram.ext import BaseFilter


class FilterSteen(BaseFilter):
    def filter(self, message):
        return 'steen' in message.text.lower()

filter_steen = FilterSteen()


class FilterBeterAls(BaseFilter):
    def filter(self, message):
        return 'beter als' in message.text.lower()

filter_beter_als = FilterBeterAls()


class FilterGateHub(BaseFilter):
    def filter(self, message):
        return 'gatehub' in message.text.lower()

filter_gatehub = FilterGateHub()


class FilterLangeBroekAan(BaseFilter):
    def filter(self, message):
        return 'lange broek' in message.text.lower()

filter_lange_broek_aan = FilterLangeBroekAan()