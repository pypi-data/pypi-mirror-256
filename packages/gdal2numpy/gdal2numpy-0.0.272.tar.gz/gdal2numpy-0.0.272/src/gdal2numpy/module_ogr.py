# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2021 Luzzi Valerio
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        module_ogr.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     16/06/2021
# -------------------------------------------------------------------------------
import glob
import math
import os
import shutil
import site
from osgeo import gdal, gdalconst
from osgeo import osr, ogr
from .filesystem import justext, juststem, forceext, justpath, strtofile
from .module_open import OpenRaster
from .module_open import OpenShape
from .module_s3 import isfile
from .module_esri_shape import AutoIdentify
 

def create_cpg(fileshp):
    """
    create_file_cpg - add a file.cpg
    :param fileshp:
    :return:
    """
    strtofile("UFT-8", forceext(fileshp, "cpg"))


def ogr_move(src, dst):
    """
    copyshp
    """
    res = shutil.move(src, dst)
    if "shp" == justext(src).lower():
        for ext in (
                "dbf", "shx", "prj", "qpj", "qml", "qix", "idx", "dat", "sbn", "sbx", "fbn", "fbx", "ain", "aih", "atx",
                "qlr", "mta", "cpg"):
            src = forceext(src, ext)
            dst = dst if os.path.isdir(dst) else forceext(dst, ext)
            if os.path.isfile(src):
                if os.path.isfile(forceext(dst, ext)):
                    os.unlink(forceext(dst, ext))
                shutil.move(src, dst)

    return res


def ogr_copy(src, dst):
    """
    copyshp
    """
    res = shutil.copy2(src, dst)
    if "shp" == justext(src).lower():
        for ext in (
                "dbf", "shx", "prj", "qpj", "qml", "qix", "idx", "dat", "sbn", "sbx", "fbn", "fbx", "ain", "aih", "atx",
                "qlr", "mta", "cpg"):
            src = forceext(src, ext)
            filedst = forceext(dst, ext)
            filedst = dst if os.path.isdir(dst) else filedst
            if os.path.isfile(src):
                if os.path.isfile(filedst):
                    os.unlink(filedst)
                shutil.copy2(src, filedst)
    return res


def ogr_remove(filename):
    """
    remove
    """
    if os.path.isfile(filename):
        if justext(filename).lower() in ("shp",):
            driver = ogr.GetDriverByName("ESRI Shapefile")
            driver.DeleteDataSource(filename)
            for ext in ("qlr", "mta", "cpg"):
                fileaux = forceext(filename, ext)
                if os.path.isfile(fileaux):
                    os.unlink(fileaux)
        else:
            os.unlink(filename)
    return not os.path.isfile(filename)


def Haversine(lat1, lon1, lat2, lon2):
    """
    Haversine Distance
    """
    R = 6371008.8  # Earth radius in kilometers

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dLon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def GetPixelSize(filename, um="m"):
    """
    GetPixelSize
    """
    ds = OpenRaster(filename)
    if ds:
        m, n = ds.RasterYSize, ds.RasterXSize
        minx, px, _, maxy, _, py = ds.GetGeoTransform()
        prj = ds.GetProjection()
        ds = None

        # srs = osr.SpatialReference()
        # srs.ImportFromProj4(prj)
        srs = GetSpatialRef(prj)

        if srs.IsGeographic() and um == "m":
            dx = Haversine(maxy, minx, maxy, minx + px * n) / n
            dy = Haversine(maxy, minx, maxy + m * py, minx) / m
            return round(dx, 1), round(dy, 1)

        return px, abs(py)

    return None, None


def GetPixelArea(filename, um="m"):
    """
    GetPixelArea
    """
    px, py = GetPixelSize(filename, um)
    return abs(px * py)


def SamePixelSize(filename1, filename2, decimals=-1):
    """
    SamePixelSize
    """
    size1 = GetPixelSize(filename1)
    size2 = GetPixelSize(filename2)
    if decimals >= 0:
        size1 = [round(item, decimals) for item in size1]
        size2 = [round(item, decimals) for item in size2]
    return size1 == size2


def GetEPSG(srs):
    """
    GetEPSG
    """
    srs = GetSpatialRef(srs)
    if srs:
        authid = srs.GetAuthorityName(
            "PROJCS") if srs.IsProjected() else srs.GetAuthorityName("GEOGCS")
        srid = srs.GetAuthorityCode("PROJCS") if srs.IsProjected(
        ) else srs.GetAuthorityCode("GEOGCS")
        return f"{authid}:{srid}"
    return None


def GetSpatialRef(filename):
    """
    GetSpatialRef
    """
    srs = None
    if isinstance(filename, osr.SpatialReference):
        srs = filename

    elif isinstance(filename, int):
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(filename)
        srs.AutoIdentifyEPSG()

    elif isinstance(filename, str) and filename.lower().startswith("epsg:"):
        code = int(filename.split(":")[1])
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(code)
        srs.AutoIdentifyEPSG()

    elif isinstance(filename, str) and filename.upper().startswith("+proj"):
        proj4text = filename
        srs = osr.SpatialReference()
        srs.ImportFromProj4(proj4text)
        srs.AutoIdentifyEPSG()

    elif isinstance(filename, str) and (filename.upper().startswith("PROJCS[") or filename.upper().startswith("GEOGCS[")):
        wkt = filename
        code = AutoIdentify(wkt)
        srs = osr.SpatialReference()
        if code:
            srs.ImportFromEPSG(code)
        else:
            srs.ImportFromWkt(wkt)
            srs.AutoIdentifyEPSG()

    elif isinstance(filename, str) and isfile(filename) and filename.lower().endswith(".shp"):
        ds = OpenShape(filename)
        if ds:
            srs = ds.GetLayer().GetSpatialRef()
            srs.AutoIdentifyEPSG()

    elif isinstance(filename, str) and isfile(filename) and filename.lower().endswith(".tif"):
        ds = OpenRaster(filename)
        if ds:
            wkt = ds.GetProjection()
            srs = osr.SpatialReference()
            srs.ImportFromWkt(wkt)
            srs.AutoIdentifyEPSG()
    else:
        srs = osr.SpatialReference()

    return srs


def SameSpatialRef(filename1, filename2):
    """
    SameSpatialRef
    """
    srs1 = GetSpatialRef(filename1)
    srs2 = GetSpatialRef(filename2)
    if srs1 and srs2:
        return srs1.IsSame(srs2) or srs1.ExportToProj4() == srs2.ExportToProj4()
    return None


def GetGeometryType(filename):
    """
    GetGeometryType
    :param filename:
    :return:
    """
    ds = OpenShape(filename, 0)
    if ds:
        lyr = ds.GetLayer()
        if lyr:
            geomtype = lyr.GetGeomType()
            name = ogr.GeometryTypeToName(geomtype)
            ds = None
            return name
        ds = None
    return None


def Rectangle(minx, miny, maxx, maxy):
    """
    Rectangle - create ogr polygon from bbox
    """
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint_2D(minx, miny)
    ring.AddPoint_2D(maxx, miny)
    ring.AddPoint_2D(maxx, maxy)
    ring.AddPoint_2D(minx, maxy)
    ring.AddPoint_2D(minx, miny)
    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly


def TransformBBOX(bbox, s_srs=None, t_srs=None):
    """
    TransformBBOX
    """
    if SameSpatialRef(s_srs, t_srs):
        return bbox
    s_minx, s_miny, s_maxx, s_maxy = bbox

    s_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    t_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

    transform = osr.CoordinateTransformation(s_srs, t_srs)
    rect = Rectangle(s_minx, s_miny, s_maxx, s_maxy)
    rect.Transform(transform)
    t_minx, t_maxx, t_miny, t_maxy = rect.GetEnvelope()
    transformed_bbox = (t_minx, t_miny, t_maxx, t_maxy)
    return transformed_bbox


def GetExtent(filename, t_srs=None):
    """
    GetExtent
    """
    s_srs = None
    minx, miny, maxx, maxy = 0, 0, 0, 0
    ext = justext(f"{filename}").lower()
    if isinstance(filename, (list, tuple)):
        minx, miny, maxx, maxy = filename
        s_srs = GetSpatialRef(4326)
        t_srs = GetSpatialRef(t_srs)
        transform = osr.CoordinateTransformation(s_srs, t_srs)
        rect = Rectangle( minx, miny, maxx, maxy)
        rect.Transform(transform)
        minx, miny, maxx, maxy = rect.GetEnvelope()

    elif ext == "tif":
        ds = OpenRaster(filename)
        if ds:
            "{xmin} {ymin} {xmax} {ymax}"
            m, n = ds.RasterYSize, ds.RasterXSize
            gt = ds.GetGeoTransform()
            minx, px, _, maxy, _, py = gt
            maxx = minx + n * px
            miny = maxy + m * py
            miny, maxy = min(miny, maxy), max(miny, maxy)
            wkt = ds.GetProjection()
            s_srs = osr.SpatialReference()
            s_srs.ImportFromWkt(wkt)
            ds = None

    elif ext in ("shp", "dbf"):

        filename = forceext(filename, "shp")
        # driver = ogr.GetDriverByName("ESRI Shapefile")
        # ds = driver.Open(filename, 0)
        ds = OpenShape(filename, 0)
        if ds:
            layer = ds.GetLayer()
            minx, maxx, miny, maxy = layer.GetExtent()
            s_srs = layer.GetSpatialRef()
            ds = None

    if t_srs and not SameSpatialRef(s_srs, t_srs):
        t_srs = GetSpatialRef(t_srs)
        transform = osr.CoordinateTransformation(s_srs, t_srs)
        rect = Rectangle(minx, miny, maxx, maxy)
        rect.Transform(transform)
        if t_srs.IsGeographic():
            miny, maxy, minx, maxx = rect.GetEnvelope()
        else:
            minx, miny, maxx, maxy = rect.GetEnvelope()

    return minx, miny, maxx, maxy


def SameExtent(filename1, filename2, decimals=-1):
    """
    SameExtent
    """
    extent1 = GetExtent(filename1)
    extent2 = GetExtent(filename2)
    if decimals >= 0:
        extent1 = [round(item, decimals) for item in extent1]
        extent2 = [round(item, decimals) for item in extent2]
    return extent1 == extent2


def SetGDALEnv():
    """
    SetGDALEnv
    """
    os.environ["__PROJ_LIB__"] = os.environ["PROJ_LIB"] if "PROJ_LIB" in os.environ else ""
    os.environ["__GDAL_DATA__"] = os.environ["GDAL_DATA"] if "GDAL_DATA" in os.environ else ""
    os.environ["PROJ_LIB"] = find_PROJ_LIB()
    os.environ["GDAL_DATA"] = find_GDAL_DATA()


def RestoreGDALEnv():
    """
    RestoreGDALEnv
    """
    if "__PROJ_LIB__" in os.environ:
        os.environ["PROJ_LIB"] = os.environ["__PROJ_LIB__"]
    if "__GDAL_DATA__" in os.environ:
        os.environ["GDAL_DATA"] = os.environ["__GDAL_DATA__"]


def find_PROJ_LIB():
    """
    find_PROJ_LIB - the path of proj_lib
    """
    pathnames = []
    roots = ["/usr"] + site.getsitepackages()
    for root in roots:
        pathnames += glob.glob(root + "/**/proj.db", recursive=True)
        if len(pathnames):
            break
    return justpath(pathnames[0]) if len(pathnames) else ""


def find_GDAL_DATA():
    """
    find_GDAL_DATA - the path of GDAL_DATA
    """
    pathnames = []
    roots = ["/usr"] + site.getsitepackages()
    for root in roots:
        pathnames += glob.glob(root + "/**/gt_datum.csv", recursive=True)
        if len(pathnames):
            break
    return justpath(pathnames[0]) if len(pathnames) else ""


def CreateRectangleShape(minx, miny, maxx, maxy, srs, fileshp="tempxy...."):
    """
    CreateRectangleShape
    """
    fileshp = fileshp if fileshp else "./tempdir/rect.shp"
    # Write rest to Shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(fileshp):
        driver.DeleteDataSource(fileshp)
    ds = driver.CreateDataSource(fileshp)
    layer = ds.CreateLayer(fileshp, srs, geom_type=ogr.wkbPolygon)
    featureDefn = layer.GetLayerDefn()
    feature = ogr.Feature(featureDefn)
    rect = Rectangle(minx, miny, maxx, maxy)
    feature.SetGeometry(rect)
    layer.CreateFeature(feature)
    feature, layer, ds = None, None, None
    return fileshp


def CreateShapeFileLayer(fileshp, srs, geom_type=ogr.wkbPoint, cpg="UTF-8"):
    """
    CreateShapeFileLayer - wrap CreateDataSource just for shapefiles
    """
    fileshp = forceext(fileshp, "shp")
    ogr_remove(fileshp)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = driver.CreateDataSource(fileshp)
    filecpg = forceext(fileshp, "cpg")
    with open(filecpg, "w") as stream:
        stream.write(cpg)
    srs = GetSpatialRef(srs)
    layer = ds.CreateLayer(juststem(fileshp), srs, geom_type=geom_type)
    ds = None
    return layer


def CopyShape(fileshp, fileout):
    """
    CopyShape
    """
    ds = gdal.VectorTranslate(fileout, fileshp, format='ESRI Shapefile',
                              accessMode='overwrite')
    ds = None  # force flush
