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

class TestrunresultTestFeatureResult(object):
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
        'url_safe_feature_id': 'str',
        'feature_name': 'str',
        'feature_type': 'RimeFeatureType',
        'severity': 'RimeSeverity',
        'summary_counts': 'TestrunresultResultSummaryCounts',
        'failing_tests': 'list[str]',
        'num_failing_rows': 'str',
        'failing_rows_html': 'str',
        'drift_statistic': 'RimeNamedDouble',
        'model_impact': 'RimeNamedDouble',
        'feature_infos': 'list[str]',
        'display': 'TestrunresultTestFeatureResultDisplay'
    }

    attribute_map = {
        'url_safe_feature_id': 'urlSafeFeatureId',
        'feature_name': 'featureName',
        'feature_type': 'featureType',
        'severity': 'severity',
        'summary_counts': 'summaryCounts',
        'failing_tests': 'failingTests',
        'num_failing_rows': 'numFailingRows',
        'failing_rows_html': 'failingRowsHtml',
        'drift_statistic': 'driftStatistic',
        'model_impact': 'modelImpact',
        'feature_infos': 'featureInfos',
        'display': 'display'
    }

    def __init__(self, url_safe_feature_id=None, feature_name=None, feature_type=None, severity=None, summary_counts=None, failing_tests=None, num_failing_rows=None, failing_rows_html=None, drift_statistic=None, model_impact=None, feature_infos=None, display=None):  # noqa: E501
        """TestrunresultTestFeatureResult - a model defined in Swagger"""  # noqa: E501
        self._url_safe_feature_id = None
        self._feature_name = None
        self._feature_type = None
        self._severity = None
        self._summary_counts = None
        self._failing_tests = None
        self._num_failing_rows = None
        self._failing_rows_html = None
        self._drift_statistic = None
        self._model_impact = None
        self._feature_infos = None
        self._display = None
        self.discriminator = None
        if url_safe_feature_id is not None:
            self.url_safe_feature_id = url_safe_feature_id
        if feature_name is not None:
            self.feature_name = feature_name
        if feature_type is not None:
            self.feature_type = feature_type
        if severity is not None:
            self.severity = severity
        if summary_counts is not None:
            self.summary_counts = summary_counts
        if failing_tests is not None:
            self.failing_tests = failing_tests
        if num_failing_rows is not None:
            self.num_failing_rows = num_failing_rows
        if failing_rows_html is not None:
            self.failing_rows_html = failing_rows_html
        if drift_statistic is not None:
            self.drift_statistic = drift_statistic
        if model_impact is not None:
            self.model_impact = model_impact
        if feature_infos is not None:
            self.feature_infos = feature_infos
        if display is not None:
            self.display = display

    @property
    def url_safe_feature_id(self):
        """Gets the url_safe_feature_id of this TestrunresultTestFeatureResult.  # noqa: E501

        The URL-compatible (base 64) encoding of feature name.  # noqa: E501

        :return: The url_safe_feature_id of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: str
        """
        return self._url_safe_feature_id

    @url_safe_feature_id.setter
    def url_safe_feature_id(self, url_safe_feature_id):
        """Sets the url_safe_feature_id of this TestrunresultTestFeatureResult.

        The URL-compatible (base 64) encoding of feature name.  # noqa: E501

        :param url_safe_feature_id: The url_safe_feature_id of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: str
        """

        self._url_safe_feature_id = url_safe_feature_id

    @property
    def feature_name(self):
        """Gets the feature_name of this TestrunresultTestFeatureResult.  # noqa: E501

        The human-readable feature name.  # noqa: E501

        :return: The feature_name of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: str
        """
        return self._feature_name

    @feature_name.setter
    def feature_name(self, feature_name):
        """Sets the feature_name of this TestrunresultTestFeatureResult.

        The human-readable feature name.  # noqa: E501

        :param feature_name: The feature_name of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: str
        """

        self._feature_name = feature_name

    @property
    def feature_type(self):
        """Gets the feature_type of this TestrunresultTestFeatureResult.  # noqa: E501


        :return: The feature_type of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: RimeFeatureType
        """
        return self._feature_type

    @feature_type.setter
    def feature_type(self, feature_type):
        """Sets the feature_type of this TestrunresultTestFeatureResult.


        :param feature_type: The feature_type of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: RimeFeatureType
        """

        self._feature_type = feature_type

    @property
    def severity(self):
        """Gets the severity of this TestrunresultTestFeatureResult.  # noqa: E501


        :return: The severity of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: RimeSeverity
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this TestrunresultTestFeatureResult.


        :param severity: The severity of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: RimeSeverity
        """

        self._severity = severity

    @property
    def summary_counts(self):
        """Gets the summary_counts of this TestrunresultTestFeatureResult.  # noqa: E501


        :return: The summary_counts of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: TestrunresultResultSummaryCounts
        """
        return self._summary_counts

    @summary_counts.setter
    def summary_counts(self, summary_counts):
        """Sets the summary_counts of this TestrunresultTestFeatureResult.


        :param summary_counts: The summary_counts of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: TestrunresultResultSummaryCounts
        """

        self._summary_counts = summary_counts

    @property
    def failing_tests(self):
        """Gets the failing_tests of this TestrunresultTestFeatureResult.  # noqa: E501

        The list of tests that fail for the feature.  # noqa: E501

        :return: The failing_tests of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._failing_tests

    @failing_tests.setter
    def failing_tests(self, failing_tests):
        """Sets the failing_tests of this TestrunresultTestFeatureResult.

        The list of tests that fail for the feature.  # noqa: E501

        :param failing_tests: The failing_tests of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: list[str]
        """

        self._failing_tests = failing_tests

    @property
    def num_failing_rows(self):
        """Gets the num_failing_rows of this TestrunresultTestFeatureResult.  # noqa: E501

        The number of rows that fail.  # noqa: E501

        :return: The num_failing_rows of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: str
        """
        return self._num_failing_rows

    @num_failing_rows.setter
    def num_failing_rows(self, num_failing_rows):
        """Sets the num_failing_rows of this TestrunresultTestFeatureResult.

        The number of rows that fail.  # noqa: E501

        :param num_failing_rows: The num_failing_rows of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: str
        """

        self._num_failing_rows = num_failing_rows

    @property
    def failing_rows_html(self):
        """Gets the failing_rows_html of this TestrunresultTestFeatureResult.  # noqa: E501

        The names of the rows that fail; may contain HTML.  # noqa: E501

        :return: The failing_rows_html of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: str
        """
        return self._failing_rows_html

    @failing_rows_html.setter
    def failing_rows_html(self, failing_rows_html):
        """Sets the failing_rows_html of this TestrunresultTestFeatureResult.

        The names of the rows that fail; may contain HTML.  # noqa: E501

        :param failing_rows_html: The failing_rows_html of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: str
        """

        self._failing_rows_html = failing_rows_html

    @property
    def drift_statistic(self):
        """Gets the drift_statistic of this TestrunresultTestFeatureResult.  # noqa: E501


        :return: The drift_statistic of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: RimeNamedDouble
        """
        return self._drift_statistic

    @drift_statistic.setter
    def drift_statistic(self, drift_statistic):
        """Sets the drift_statistic of this TestrunresultTestFeatureResult.


        :param drift_statistic: The drift_statistic of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: RimeNamedDouble
        """

        self._drift_statistic = drift_statistic

    @property
    def model_impact(self):
        """Gets the model_impact of this TestrunresultTestFeatureResult.  # noqa: E501


        :return: The model_impact of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: RimeNamedDouble
        """
        return self._model_impact

    @model_impact.setter
    def model_impact(self, model_impact):
        """Sets the model_impact of this TestrunresultTestFeatureResult.


        :param model_impact: The model_impact of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: RimeNamedDouble
        """

        self._model_impact = model_impact

    @property
    def feature_infos(self):
        """Gets the feature_infos of this TestrunresultTestFeatureResult.  # noqa: E501

        The list of feature information used.  # noqa: E501

        :return: The feature_infos of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._feature_infos

    @feature_infos.setter
    def feature_infos(self, feature_infos):
        """Sets the feature_infos of this TestrunresultTestFeatureResult.

        The list of feature information used.  # noqa: E501

        :param feature_infos: The feature_infos of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: list[str]
        """

        self._feature_infos = feature_infos

    @property
    def display(self):
        """Gets the display of this TestrunresultTestFeatureResult.  # noqa: E501


        :return: The display of this TestrunresultTestFeatureResult.  # noqa: E501
        :rtype: TestrunresultTestFeatureResultDisplay
        """
        return self._display

    @display.setter
    def display(self, display):
        """Sets the display of this TestrunresultTestFeatureResult.


        :param display: The display of this TestrunresultTestFeatureResult.  # noqa: E501
        :type: TestrunresultTestFeatureResultDisplay
        """

        self._display = display

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
        if issubclass(TestrunresultTestFeatureResult, dict):
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
        if not isinstance(other, TestrunresultTestFeatureResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
