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

class V1firewallfirewallFirewallIdUuidFirewall(object):
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
        'firewall_id': 'object',
        'project_id': 'RimeUUID',
        'model_id': 'RimeUUID',
        'bin_size': 'str',
        'ref_data_id': 'str',
        'scheduled_ct_info': 'FirewallScheduledCTInfo',
        'risk_scores': 'list[RiskscoreRiskScore]',
        'test_category_severities': 'list[FirewallTestCategorySeverity]',
        'latest_run_info': 'FirewallLatestRunInfo'
    }

    attribute_map = {
        'firewall_id': 'firewallId',
        'project_id': 'projectId',
        'model_id': 'modelId',
        'bin_size': 'binSize',
        'ref_data_id': 'refDataId',
        'scheduled_ct_info': 'scheduledCtInfo',
        'risk_scores': 'riskScores',
        'test_category_severities': 'testCategorySeverities',
        'latest_run_info': 'latestRunInfo'
    }

    def __init__(self, firewall_id=None, project_id=None, model_id=None, bin_size=None, ref_data_id=None, scheduled_ct_info=None, risk_scores=None, test_category_severities=None, latest_run_info=None):  # noqa: E501
        """V1firewallfirewallFirewallIdUuidFirewall - a model defined in Swagger"""  # noqa: E501
        self._firewall_id = None
        self._project_id = None
        self._model_id = None
        self._bin_size = None
        self._ref_data_id = None
        self._scheduled_ct_info = None
        self._risk_scores = None
        self._test_category_severities = None
        self._latest_run_info = None
        self.discriminator = None
        if firewall_id is not None:
            self.firewall_id = firewall_id
        if project_id is not None:
            self.project_id = project_id
        if model_id is not None:
            self.model_id = model_id
        if bin_size is not None:
            self.bin_size = bin_size
        if ref_data_id is not None:
            self.ref_data_id = ref_data_id
        if scheduled_ct_info is not None:
            self.scheduled_ct_info = scheduled_ct_info
        if risk_scores is not None:
            self.risk_scores = risk_scores
        if test_category_severities is not None:
            self.test_category_severities = test_category_severities
        if latest_run_info is not None:
            self.latest_run_info = latest_run_info

    @property
    def firewall_id(self):
        """Gets the firewall_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501

        Unique ID of an object in RIME.  # noqa: E501

        :return: The firewall_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: object
        """
        return self._firewall_id

    @firewall_id.setter
    def firewall_id(self, firewall_id):
        """Sets the firewall_id of this V1firewallfirewallFirewallIdUuidFirewall.

        Unique ID of an object in RIME.  # noqa: E501

        :param firewall_id: The firewall_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: object
        """

        self._firewall_id = firewall_id

    @property
    def project_id(self):
        """Gets the project_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501


        :return: The project_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this V1firewallfirewallFirewallIdUuidFirewall.


        :param project_id: The project_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: RimeUUID
        """

        self._project_id = project_id

    @property
    def model_id(self):
        """Gets the model_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501


        :return: The model_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this V1firewallfirewallFirewallIdUuidFirewall.


        :param model_id: The model_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: RimeUUID
        """

        self._model_id = model_id

    @property
    def bin_size(self):
        """Gets the bin_size of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501


        :return: The bin_size of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: str
        """
        return self._bin_size

    @bin_size.setter
    def bin_size(self, bin_size):
        """Sets the bin_size of this V1firewallfirewallFirewallIdUuidFirewall.


        :param bin_size: The bin_size of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: str
        """

        self._bin_size = bin_size

    @property
    def ref_data_id(self):
        """Gets the ref_data_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501

        The semantic ID of the reference dataset. This should correspond with the primary key in the Dataset Registry.  # noqa: E501

        :return: The ref_data_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: str
        """
        return self._ref_data_id

    @ref_data_id.setter
    def ref_data_id(self, ref_data_id):
        """Sets the ref_data_id of this V1firewallfirewallFirewallIdUuidFirewall.

        The semantic ID of the reference dataset. This should correspond with the primary key in the Dataset Registry.  # noqa: E501

        :param ref_data_id: The ref_data_id of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: str
        """

        self._ref_data_id = ref_data_id

    @property
    def scheduled_ct_info(self):
        """Gets the scheduled_ct_info of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501


        :return: The scheduled_ct_info of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: FirewallScheduledCTInfo
        """
        return self._scheduled_ct_info

    @scheduled_ct_info.setter
    def scheduled_ct_info(self, scheduled_ct_info):
        """Sets the scheduled_ct_info of this V1firewallfirewallFirewallIdUuidFirewall.


        :param scheduled_ct_info: The scheduled_ct_info of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: FirewallScheduledCTInfo
        """

        self._scheduled_ct_info = scheduled_ct_info

    @property
    def risk_scores(self):
        """Gets the risk_scores of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501


        :return: The risk_scores of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: list[RiskscoreRiskScore]
        """
        return self._risk_scores

    @risk_scores.setter
    def risk_scores(self, risk_scores):
        """Sets the risk_scores of this V1firewallfirewallFirewallIdUuidFirewall.


        :param risk_scores: The risk_scores of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: list[RiskscoreRiskScore]
        """

        self._risk_scores = risk_scores

    @property
    def test_category_severities(self):
        """Gets the test_category_severities of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501


        :return: The test_category_severities of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: list[FirewallTestCategorySeverity]
        """
        return self._test_category_severities

    @test_category_severities.setter
    def test_category_severities(self, test_category_severities):
        """Sets the test_category_severities of this V1firewallfirewallFirewallIdUuidFirewall.


        :param test_category_severities: The test_category_severities of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: list[FirewallTestCategorySeverity]
        """

        self._test_category_severities = test_category_severities

    @property
    def latest_run_info(self):
        """Gets the latest_run_info of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501


        :return: The latest_run_info of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :rtype: FirewallLatestRunInfo
        """
        return self._latest_run_info

    @latest_run_info.setter
    def latest_run_info(self, latest_run_info):
        """Sets the latest_run_info of this V1firewallfirewallFirewallIdUuidFirewall.


        :param latest_run_info: The latest_run_info of this V1firewallfirewallFirewallIdUuidFirewall.  # noqa: E501
        :type: FirewallLatestRunInfo
        """

        self._latest_run_info = latest_run_info

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
        if issubclass(V1firewallfirewallFirewallIdUuidFirewall, dict):
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
        if not isinstance(other, V1firewallfirewallFirewallIdUuidFirewall):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
