from collections import OrderedDict

from rest_framework.routers import APIRootView, DefaultRouter


class OrderedDefaultRouter(DefaultRouter):
    """A DefaultRouter that sorts its endpoints alphabetically.

    Inspired by a stackoverflow answer: https://stackoverflow.com/questions/↵
    24311893/ordering-items-on-the-root-api-view-for-defaultrouter. That
    version, however, does not cooperate well with swagger (grouping of
    available HTTP methods by endpoint is lost).
    """

    def __init__(self, *args, **kwargs):
        super(OrderedDefaultRouter, self).__init__(*args, **kwargs)
        self.extra_api_root_dict = {}
        self.APIRootView = self

    def as_view(self, api_root_dict):
        """Return a root view with sorted endpoints.

        This method intercepts the call to APIRootView.as_view in the
        get_api_root_view method inherited from the superclass, adds
        extra endpoints to be rendered, and sorts the grand total
        before continuing.

        """
        d = dict(api_root_dict)
        d.update(self.extra_api_root_dict)
        d = OrderedDict(sorted(d.items()))
        return APIRootView.as_view(api_root_dict=d)
