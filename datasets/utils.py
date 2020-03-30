from osgeo import ogr

from django.contrib.gis.geos.collections import MultiPolygon, MultiLineString, MultiPoint


def wrap_geos_geometry(geometry):

    if geometry.geom_type == "Polygon":
        return MultiPolygon(geometry)

    elif geometry.geom_type == "LineString":
        return MultiLineString(geometry)

    elif geometry.geom_type == "Point":
        return MultiPoint(geometry)

    else:
        return geometry


def calc_geometry_field(geometry_type):

    if geometry_type == "Polygon":
        return "geom_multipolygon"

    elif geometry_type == "LineString":
        return "geom_multilinestring"

    elif geometry_type == "Point":
        return "geom_multipoint"

    else:
        return "geom_" + geometry_type.lower()


def get_ogr_feature_attribute(attr, feature):
    attr_name = attr.name

    if not feature.IsFieldSet(attr_name):
        return (True, None)

    if attr.type == ogr.OFTInteger:
        value = str(feature.GetFieldAsInteger(attr_name))

    elif attr.type == ogr.OFTIntegerList:
        value = repr(feature.GetFieldAsIntegerList(attr_name))

    elif attr.type == ogr.OFTReal:
        value = feature.GetFieldAsDouble(attr_name)

        value = "%*.*f" % (attr.width, attr.precision, value)

    elif attr.type == ogr.OFTRealList:
        values = feature.GetFieldAsDoubleList(attr_name)
        str_values = []
        for value in values:
            str_values.append("%*.*f" % (attr.width,
            attr.precision, value))
        value = repr(str_values)

    elif attr.type == ogr.OFTString:
        value = feature.GetFieldAsString(attr_name)

    elif attr.type == ogr.OFTStringList:
        value = repr(feature.GetFieldAsStringList(attr_name))

    elif attr.type == ogr.OFTDate:
        parts = feature.GetFieldAsDateTime(attr_name)
        year, month, day, hour, minute, second, tzone = parts
        value = "%d,%d,%d,%d" % (year, month, day, tzone)

    elif attr.type == ogr.OFTTime:
        parts = feature.GetFieldAsDateTime(attr_name)
        year, month, day, hour, minute, second, tzone = parts
        value = "%d,%d,%d,%d" % (hour, minute, second, tzone)

    elif attr.type == ogr.OFTDateTime:
        parts = feature.GetFieldAsDateTime(attr_name)
        year, month, day, hour, minute, second, tzone = parts
        value = "%d,%d,%d,%d,%d,%d,%d" % (year, month, day, hour, minute, second, tzone)

    else:
        return (False, "Unsupported attribute type: " +
                str(attr.type))
    return (True, value)