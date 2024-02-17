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

class RimeUserWithRole(object):
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
        'user_id': 'RimeUUID',
        'user_role': 'RimeActorRole'
    }

    attribute_map = {
        'user_id': 'userId',
        'user_role': 'userRole'
    }

    def __init__(self, user_id=None, user_role=None):  # noqa: E501
        """RimeUserWithRole - a model defined in Swagger"""  # noqa: E501
        self._user_id = None
        self._user_role = None
        self.discriminator = None
        if user_id is not None:
            self.user_id = user_id
        if user_role is not None:
            self.user_role = user_role

    @property
    def user_id(self):
        """Gets the user_id of this RimeUserWithRole.  # noqa: E501


        :return: The user_id of this RimeUserWithRole.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this RimeUserWithRole.


        :param user_id: The user_id of this RimeUserWithRole.  # noqa: E501
        :type: RimeUUID
        """

        self._user_id = user_id

    @property
    def user_role(self):
        """Gets the user_role of this RimeUserWithRole.  # noqa: E501


        :return: The user_role of this RimeUserWithRole.  # noqa: E501
        :rtype: RimeActorRole
        """
        return self._user_role

    @user_role.setter
    def user_role(self, user_role):
        """Sets the user_role of this RimeUserWithRole.


        :param user_role: The user_role of this RimeUserWithRole.  # noqa: E501
        :type: RimeActorRole
        """

        self._user_role = user_role

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
        if issubclass(RimeUserWithRole, dict):
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
        if not isinstance(other, RimeUserWithRole):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
