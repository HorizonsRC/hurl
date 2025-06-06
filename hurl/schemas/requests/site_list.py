"""Hilltop SiteList request parameters."""

from pydantic import Field, field_validator, model_validator

from hurl.schemas.requests.base import BaseHilltopRequest
from hurl.exceptions import HilltopRequestError


class SiteListRequest(BaseHilltopRequest):
    """Request parameters for Hilltop SiteList."""

    request: str = Field(default="SiteList", serialization_alias="Request")
    location: str | None = Field(default=None, serialization_alias="Location")
    bounding_box: str | None = Field(default=None, serialization_alias="BBox")
    measurement: str | None = Field(default=None, serialization_alias="Measurement")
    collection: str | None = Field(default=None, serialization_alias="Collection")
    site_parameters: str | None = Field(
        default=None, serialization_alias="SiteParameters"
    )
    target: str | None = Field(default=None, serialization_alias="Target")
    syn_level: str | None = Field(default=None, serialization_alias="SynLevel")
    fill_cols: str | None = Field(default=None, serialization_alias="FillCols")

    @field_validator("request", mode="before")
    def validate_request(cls, value):
        """Validate the request parameter."""
        if value != "SiteList":
            raise ValueError("Request must be 'SiteList'")
        return value

    @field_validator("location", mode="before")
    def validate_location(cls, value):
        """
        Validate the location parameter.

        Acceptable values are 'Yes', 'LatLong', or None.

        'Yes': Provide location in easting and northing format.
        'LatLong': Provide location in latitude and longitude format (NZGD2000).

        """
        if value not in ["Yes", "LatLong", None]:
            raise HilltopRequestError("Location must be 'Yes', 'LatLong', or None")
        return value

    @field_validator("bounding_box", mode="before")
    def validate_bounding_box(cls, value):
        """
        Validate the bounding box parameter.

        The BBox key accepts two easting and northing pairs by default. These define
        two points diagonally opposite to each other. The order of the pairs is not
        important, but the easting precedes the northing in each pair.

        The BBox key can be in lat/long if you wish and you use a shortened version of
        the OGC format. For example to send a bounding box in WGS84:

        >>> BBox=-46.48797124,167.65999182,-44.73293297,168.83236546,EPSG:4326

        Valid EPSG codes are:
        - EPSG:4326 (WGS84)
        - EPSG:2193 (NZTM 2000)
        - EPSG:27200 (NZMG)
        - EPSG:4167 (NZGD 2000)

        """
        if value is None:
            return value
        if value is not None and not isinstance(value, str):
            raise HilltopRequestError("Bounding box must be a string")

        # Split the bounding box into parts
        parts = value.split(",") if value else []

        if len(parts) < 4:
            raise HilltopRequestError(
                "Bounding box must contain at least four values "
                "(two pairs of coordinates)"
            )
        if len(parts) > 5:
            raise HilltopRequestError(
                "Bounding box must contain at most five values "
                "(two pairs of coordinates and an optional EPSG code)"
            )
        epsg_code = parts[-1] if len(parts) == 5 else None
        coordinates = parts[:-1] if epsg_code else parts

        if epsg_code not in ["EPSG:4326", "EPSG:2193", "EPSG:27200", "EPSG:4167"]:
            raise HilltopRequestError(
                "Invalid EPSG code. Valid codes are: "
                "EPSG:4326 (WGS84), "
                "EPSG:2193 (NZTM 2000), "
                "EPSG:27200 (NZMG), "
                "EPSG:4167 (NZGD 2000). "
                "Disregard the name in the parenthesis, only supply EPSG:XXXX. "
            )

        for coord in coordinates:
            try:
                float(coord)
            except ValueError:
                raise HilltopRequestError(
                    "Bounding box coordinates must be numeric values"
                )

        return value

    @field_validator("target", mode="before")
    def validate_target(cls, value):
        """Validate the target parameter."""
        if value is None:
            return value
        if value != "HtmlSelect":
            raise HilltopRequestError(
                "Only JSON and XML response formats are supported. "
                "Use 'HtmlSelect' to request JSON, or leave it blank for XML."
            )
        if not isinstance(value, str):
            raise HilltopRequestError("Target must be a string")
        return value

    @model_validator(mode="after")
    def validate_syn_level_and_fill_cols(self) -> "self":
        """
        Validate the SynLevel and FillCols parameters.

        SynLevel only valid when 'Target' is 'HtmlSelect'.
        FillCols only valid when SiteParameters are supplied.

        The syn_level key accepts the numbers 1 or 2.
        The FillCols key accepts the word "Yes".

        """
        # Check if the target is 'HtmlSelect'
        if self.target == "HtmlSelect":
            if self.syn_level not in ["1", "2", None]:
                raise HilltopRequestError(
                    "SynLevel must be '1' or '2' or blank when Target is 'HtmlSelect'"
                )
        else:
            # If target is not 'HtmlSelect', syn_level should be None
            if self.syn_level is not None:
                raise HilltopRequestError(
                    "SynLevel must be None when Target is not 'HtmlSelect'"
                )

        if self.site_parameters:
            if self.fill_cols not in ["Yes", None]:
                raise HilltopRequestError(
                    "FillCols must be 'Yes' or left blank when "
                    "SiteParameters are supplied"
                )
        else:
            # If target is not 'HtmlSelect', syn_level should be None
            if self.fill_cols is not None:
                raise HilltopRequestError(
                    "FillCols must be None when no SiteParameters are supplied"
                )

        return self
