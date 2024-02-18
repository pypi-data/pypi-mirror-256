from typing import Dict, TypedDict, List, Union
from typing_extensions import Required


class SpanEvent(TypedDict, total=False):
    """ span_event. """

    event_id: "_Uuid"
    organization_id: "_Uint"
    project_id: Required["_Uint"]
    """ Required property """

    trace_id: Required["_Uuid"]
    """ Required property """

    span_id: Required[str]
    """
    The span ID is a unique identifier for a span within a trace. It is an 8 byte hexadecimal string.

    Required property
    """

    parent_span_id: str
    """ The parent span ID is the ID of the span that caused this span. It is an 8 byte hexadecimal string. """

    segment_id: str
    """ The segment ID is a unique identifier for a segment within a trace. It is an 8 byte hexadecimal string. """

    profile_id: "_Uuid"
    is_segment: Required[bool]
    """
    Whether this span is a segment or not.

    Required property
    """

    start_timestamp_ms: Required["_Uint"]
    """ Required property """

    duration_ms: Required["_Uint32"]
    """ Required property """

    exclusive_time_ms: Required["_PositiveFloat"]
    """ Required property """

    retention_days: Required["_Uint16"]
    """ Required property """

    received: Required["_PositiveFloat"]
    """ Required property """

    description: str
    tags: Union[Dict[str, str], None]
    """  Manual key/value tag pairs. """

    sentry_tags: "_SentryExtractedTags"
    measurements: Dict[str, "_MeasurementValue"]
    _metrics_summary: Dict[str, List["_MetricSummaryValue"]]


class _MeasurementValue(TypedDict, total=False):
    value: Required[Union[int, float]]
    """ Required property """

    unit: str


class _MetricSummaryValue(TypedDict, total=False):
    min: Union[int, float]
    max: Union[int, float]
    sum: Union[int, float]
    count: Union[int, float]
    tags: Dict[str, str]


_PositiveFloat = Union[int, float]
""" minimum: 0 """



_SentryExtractedTags = Union["_SentryExtractedTagsAnyof0"]
""" Tags extracted by sentry. These are kept separate from customer tags """



_SentryExtractedTagsAnyof0 = TypedDict('_SentryExtractedTagsAnyof0', {
    'http.method': str,
    'action': str,
    'domain': str,
    'module': str,
    'group': str,
    'system': str,
    'status': str,
    'status_code': str,
    'transaction': str,
    'transaction.op': str,
    'op': str,
    'transaction.method': str,
}, total=False)


_Uint = int
""" minimum: 0 """



_Uint16 = int
"""
minimum: 0
maximum: 65535
"""



_Uint32 = int
"""
minimum: 0
maximum: 4294967295
"""



_Uuid = str
"""
minLength: 32
maxLength: 36
"""

