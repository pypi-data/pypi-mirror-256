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

class ConfigvalidatorConfigTypeBody(object):
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
        'config_json': 'str'
    }

    attribute_map = {
        'config_json': 'configJson'
    }

    def __init__(self, config_json=None):  # noqa: E501
        """ConfigvalidatorConfigTypeBody - a model defined in Swagger"""  # noqa: E501
        self._config_json = None
        self.discriminator = None
        if config_json is not None:
            self.config_json = config_json

    @property
    def config_json(self):
        """Gets the config_json of this ConfigvalidatorConfigTypeBody.  # noqa: E501

        The JSON string to validate.  # noqa: E501

        :return: The config_json of this ConfigvalidatorConfigTypeBody.  # noqa: E501
        :rtype: str
        """
        return self._config_json

    @config_json.setter
    def config_json(self, config_json):
        """Sets the config_json of this ConfigvalidatorConfigTypeBody.

        The JSON string to validate.  # noqa: E501

        :param config_json: The config_json of this ConfigvalidatorConfigTypeBody.  # noqa: E501
        :type: str
        """

        self._config_json = config_json

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
        if issubclass(ConfigvalidatorConfigTypeBody, dict):
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
        if not isinstance(other, ConfigvalidatorConfigTypeBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
