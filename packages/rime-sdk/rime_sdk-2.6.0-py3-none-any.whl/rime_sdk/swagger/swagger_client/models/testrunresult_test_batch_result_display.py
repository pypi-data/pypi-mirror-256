# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: dev@robustintelligence.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TestrunresultTestBatchResultDisplay(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'summary_details': 'str',
        'table_columns_to_show': 'list[RimeTableColumn]',
        'long_description_tabs': 'list[RimeLongDescriptionTab]',
        'description_html': 'str'
    }

    attribute_map = {
        'summary_details': 'summaryDetails',
        'table_columns_to_show': 'tableColumnsToShow',
        'long_description_tabs': 'longDescriptionTabs',
        'description_html': 'descriptionHtml'
    }

    def __init__(self, summary_details=None, table_columns_to_show=None, long_description_tabs=None, description_html=None):  # noqa: E501
        """TestrunresultTestBatchResultDisplay - a model defined in Swagger"""  # noqa: E501
        self._summary_details = None
        self._table_columns_to_show = None
        self._long_description_tabs = None
        self._description_html = None
        self.discriminator = None
        if summary_details is not None:
            self.summary_details = summary_details
        if table_columns_to_show is not None:
            self.table_columns_to_show = table_columns_to_show
        if long_description_tabs is not None:
            self.long_description_tabs = long_description_tabs
        if description_html is not None:
            self.description_html = description_html

    @property
    def summary_details(self):
        """Gets the summary_details of this TestrunresultTestBatchResultDisplay.  # noqa: E501

        Summary details are marshalled JSON, the field is not used and is empty.  # noqa: E501

        :return: The summary_details of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :rtype: str
        """
        return self._summary_details

    @summary_details.setter
    def summary_details(self, summary_details):
        """Sets the summary_details of this TestrunresultTestBatchResultDisplay.

        Summary details are marshalled JSON, the field is not used and is empty.  # noqa: E501

        :param summary_details: The summary_details of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :type: str
        """

        self._summary_details = summary_details

    @property
    def table_columns_to_show(self):
        """Gets the table_columns_to_show of this TestrunresultTestBatchResultDisplay.  # noqa: E501


        :return: The table_columns_to_show of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :rtype: list[RimeTableColumn]
        """
        return self._table_columns_to_show

    @table_columns_to_show.setter
    def table_columns_to_show(self, table_columns_to_show):
        """Sets the table_columns_to_show of this TestrunresultTestBatchResultDisplay.


        :param table_columns_to_show: The table_columns_to_show of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :type: list[RimeTableColumn]
        """

        self._table_columns_to_show = table_columns_to_show

    @property
    def long_description_tabs(self):
        """Gets the long_description_tabs of this TestrunresultTestBatchResultDisplay.  # noqa: E501

        More detailed information about the test batch.  # noqa: E501

        :return: The long_description_tabs of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :rtype: list[RimeLongDescriptionTab]
        """
        return self._long_description_tabs

    @long_description_tabs.setter
    def long_description_tabs(self, long_description_tabs):
        """Sets the long_description_tabs of this TestrunresultTestBatchResultDisplay.

        More detailed information about the test batch.  # noqa: E501

        :param long_description_tabs: The long_description_tabs of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :type: list[RimeLongDescriptionTab]
        """

        self._long_description_tabs = long_description_tabs

    @property
    def description_html(self):
        """Gets the description_html of this TestrunresultTestBatchResultDisplay.  # noqa: E501

        Description of the test batch result that may contain HTML.  # noqa: E501

        :return: The description_html of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :rtype: str
        """
        return self._description_html

    @description_html.setter
    def description_html(self, description_html):
        """Sets the description_html of this TestrunresultTestBatchResultDisplay.

        Description of the test batch result that may contain HTML.  # noqa: E501

        :param description_html: The description_html of this TestrunresultTestBatchResultDisplay.  # noqa: E501
        :type: str
        """

        self._description_html = description_html

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TestrunresultTestBatchResultDisplay, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TestrunresultTestBatchResultDisplay):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
