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

class TestrunresultTestCaseDisplay(object):
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
        'table_info': 'str',
        'details': 'str',
        'details_layout': 'list[str]'
    }

    attribute_map = {
        'table_info': 'tableInfo',
        'details': 'details',
        'details_layout': 'detailsLayout'
    }

    def __init__(self, table_info=None, details=None, details_layout=None):  # noqa: E501
        """TestrunresultTestCaseDisplay - a model defined in Swagger"""  # noqa: E501
        self._table_info = None
        self._details = None
        self._details_layout = None
        self.discriminator = None
        if table_info is not None:
            self.table_info = table_info
        if details is not None:
            self.details = details
        if details_layout is not None:
            self.details_layout = details_layout

    @property
    def table_info(self):
        """Gets the table_info of this TestrunresultTestCaseDisplay.  # noqa: E501

        Table info contains information for displaying the test case in a table in the FE.  # noqa: E501

        :return: The table_info of this TestrunresultTestCaseDisplay.  # noqa: E501
        :rtype: str
        """
        return self._table_info

    @table_info.setter
    def table_info(self, table_info):
        """Sets the table_info of this TestrunresultTestCaseDisplay.

        Table info contains information for displaying the test case in a table in the FE.  # noqa: E501

        :param table_info: The table_info of this TestrunresultTestCaseDisplay.  # noqa: E501
        :type: str
        """

        self._table_info = table_info

    @property
    def details(self):
        """Gets the details of this TestrunresultTestCaseDisplay.  # noqa: E501

        Details includes ML-specified details for the test case. This can include graphs, HTML, etc.  # noqa: E501

        :return: The details of this TestrunresultTestCaseDisplay.  # noqa: E501
        :rtype: str
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this TestrunresultTestCaseDisplay.

        Details includes ML-specified details for the test case. This can include graphs, HTML, etc.  # noqa: E501

        :param details: The details of this TestrunresultTestCaseDisplay.  # noqa: E501
        :type: str
        """

        self._details = details

    @property
    def details_layout(self):
        """Gets the details_layout of this TestrunresultTestCaseDisplay.  # noqa: E501


        :return: The details_layout of this TestrunresultTestCaseDisplay.  # noqa: E501
        :rtype: list[str]
        """
        return self._details_layout

    @details_layout.setter
    def details_layout(self, details_layout):
        """Sets the details_layout of this TestrunresultTestCaseDisplay.


        :param details_layout: The details_layout of this TestrunresultTestCaseDisplay.  # noqa: E501
        :type: list[str]
        """

        self._details_layout = details_layout

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
        if issubclass(TestrunresultTestCaseDisplay, dict):
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
        if not isinstance(other, TestrunresultTestCaseDisplay):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
