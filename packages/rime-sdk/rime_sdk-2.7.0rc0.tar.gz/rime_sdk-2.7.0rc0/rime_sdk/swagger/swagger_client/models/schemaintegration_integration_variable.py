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

class SchemaintegrationIntegrationVariable(object):
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
        'name': 'str',
        'sensitivity': 'IntegrationVariableSensitivity',
        'value': 'str'
    }

    attribute_map = {
        'name': 'name',
        'sensitivity': 'sensitivity',
        'value': 'value'
    }

    def __init__(self, name=None, sensitivity=None, value=None):  # noqa: E501
        """SchemaintegrationIntegrationVariable - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._sensitivity = None
        self._value = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if sensitivity is not None:
            self.sensitivity = sensitivity
        if value is not None:
            self.value = value

    @property
    def name(self):
        """Gets the name of this SchemaintegrationIntegrationVariable.  # noqa: E501


        :return: The name of this SchemaintegrationIntegrationVariable.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SchemaintegrationIntegrationVariable.


        :param name: The name of this SchemaintegrationIntegrationVariable.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def sensitivity(self):
        """Gets the sensitivity of this SchemaintegrationIntegrationVariable.  # noqa: E501


        :return: The sensitivity of this SchemaintegrationIntegrationVariable.  # noqa: E501
        :rtype: IntegrationVariableSensitivity
        """
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, sensitivity):
        """Sets the sensitivity of this SchemaintegrationIntegrationVariable.


        :param sensitivity: The sensitivity of this SchemaintegrationIntegrationVariable.  # noqa: E501
        :type: IntegrationVariableSensitivity
        """

        self._sensitivity = sensitivity

    @property
    def value(self):
        """Gets the value of this SchemaintegrationIntegrationVariable.  # noqa: E501

        Field \"value\" is plaintext if the variable is not sensitive or nil if it is secret.  # noqa: E501

        :return: The value of this SchemaintegrationIntegrationVariable.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this SchemaintegrationIntegrationVariable.

        Field \"value\" is plaintext if the variable is not sensitive or nil if it is secret.  # noqa: E501

        :param value: The value of this SchemaintegrationIntegrationVariable.  # noqa: E501
        :type: str
        """

        self._value = value

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
        if issubclass(SchemaintegrationIntegrationVariable, dict):
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
        if not isinstance(other, SchemaintegrationIntegrationVariable):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
