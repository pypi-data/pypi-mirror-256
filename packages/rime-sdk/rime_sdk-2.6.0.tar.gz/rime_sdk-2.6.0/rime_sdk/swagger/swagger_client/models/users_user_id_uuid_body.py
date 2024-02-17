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

class UsersUserIdUuidBody(object):
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
        'user': 'V1usersuserIdUuidUser',
        'mask': 'RimeUserWriteMask'
    }

    attribute_map = {
        'user': 'user',
        'mask': 'mask'
    }

    def __init__(self, user=None, mask=None):  # noqa: E501
        """UsersUserIdUuidBody - a model defined in Swagger"""  # noqa: E501
        self._user = None
        self._mask = None
        self.discriminator = None
        if user is not None:
            self.user = user
        if mask is not None:
            self.mask = mask

    @property
    def user(self):
        """Gets the user of this UsersUserIdUuidBody.  # noqa: E501


        :return: The user of this UsersUserIdUuidBody.  # noqa: E501
        :rtype: V1usersuserIdUuidUser
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this UsersUserIdUuidBody.


        :param user: The user of this UsersUserIdUuidBody.  # noqa: E501
        :type: V1usersuserIdUuidUser
        """

        self._user = user

    @property
    def mask(self):
        """Gets the mask of this UsersUserIdUuidBody.  # noqa: E501


        :return: The mask of this UsersUserIdUuidBody.  # noqa: E501
        :rtype: RimeUserWriteMask
        """
        return self._mask

    @mask.setter
    def mask(self, mask):
        """Sets the mask of this UsersUserIdUuidBody.


        :param mask: The mask of this UsersUserIdUuidBody.  # noqa: E501
        :type: RimeUserWriteMask
        """

        self._mask = mask

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
        if issubclass(UsersUserIdUuidBody, dict):
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
        if not isinstance(other, UsersUserIdUuidBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
