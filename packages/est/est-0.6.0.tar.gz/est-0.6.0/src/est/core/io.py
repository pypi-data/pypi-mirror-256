"""simple helper functions to insure a simple link with the `io` module (and XASObject)"""

import logging
from typing import Optional, Union

import h5py
from silx.io.url import DataUrl

from est.units import ur
from est import settings
from est.io import read_xas, write_xas
from est.core.types import XASObject
from est.core.types import dimensions as dimensions_mod
from est.io.utils.information import InputInformation
from est.io.utils.ascii import build_ascii_data_url


_logger = logging.getLogger(__name__)

DEFAULT_SPECTRA_PATH = "/data/NXdata/data"

DEFAULT_CHANNEL_PATH = "/data/NXdata/Channel"

DEFAULT_CONF_PATH = "/configuration"


def read_from_url(
    spectra_url,
    channel_url,
    dimensions: Optional[dimensions_mod.DimensionsType] = None,
    config_url=None,
    energy_unit=ur.eV,
    timeout=settings.DEFAULT_READ_TIMEOUT,
) -> XASObject:
    """

    :param DataUrl spectra_url: data url to the spectra
    :param DataUrl channel_url: data url to the channel / energy
    :param DataUrl config_url: data url to the process configuration
    :param dimensions: way the data has been stored.
                       Usually is (X, Y, channels) of (Channels, Y, X).
                       If None, by default is considered to be (Z, Y, X)
    :type: tuple
    :return:
    :rtype: XASObject
    """
    input_information = InputInformation(
        spectra_url=spectra_url,
        channel_url=channel_url,
        config_url=config_url,
        dimensions=dimensions,
        energy_unit=energy_unit,
    )
    return read_from_input_information(input_information, timeout=timeout)


def read_from_input_information(
    information: InputInformation, timeout=settings.DEFAULT_READ_TIMEOUT
) -> XASObject:
    spectra, energy, configuration = read_xas(information=information, timeout=timeout)
    return XASObject(spectra=spectra, energy=energy, configuration=configuration)


def read_from_file(
    file_path: str,
    energy_unit=ur.eV,
    dimensions: Optional[dimensions_mod.DimensionsType] = None,
    columns_names: Optional[dict] = None,
    scan_title: Optional[str] = None,
    timeout=settings.DEFAULT_READ_TIMEOUT,
) -> XASObject:
    """

    :param str file_path: path to the file containing the spectra. Must be a
                          .dat file that pymca can handle or a .h5py with
                          default path
    :param tuple dimensions: dimensions of the input data. For ASCII file can
                             be (X, Y) or (Y, X)
    :param Union[None,tuple] columns: name of the column to take for .dat...
                                      files.
    :return XasObject created from the input
    :rtype: XASObject
    """
    if file_path in (None, ""):
        return
    input_information = _init_input_information(
        file_path,
        energy_unit=energy_unit,
        dimensions=dimensions,
        columns_names=columns_names,
        scan_title=scan_title,
    )
    return read_from_input_information(input_information, timeout=timeout)


def _init_input_information(
    file_path: str,
    energy_unit=ur.eV,
    dimensions: Optional[dimensions_mod.DimensionsType] = None,
    columns_names=None,
    scan_title=None,
) -> InputInformation:
    # TODO: we should be able to avoid calling the creation of an InputInformation
    if h5py.is_hdf5(file_path):
        return InputInformation(
            spectra_url=DataUrl(
                file_path=file_path,
                scheme="silx",
                data_path=DEFAULT_SPECTRA_PATH,
            ),
            channel_url=DataUrl(
                file_path=file_path,
                scheme="silx",
                data_path=DEFAULT_CHANNEL_PATH,
            ),
            config_url=DataUrl(
                file_path=file_path, scheme="silx", data_path="configuration"
            ),
            energy_unit=energy_unit,
            dimensions=dimensions,
        )
    return InputInformation(
        spectra_url=build_ascii_data_url(
            file_path=file_path,
            col_name=columns_names["mu"],
            scan_title=scan_title,
        ),
        channel_url=build_ascii_data_url(
            file_path=file_path,
            col_name=columns_names["energy"],
            scan_title=scan_title,
        ),
        energy_unit=energy_unit,
        dimensions=dimensions,
    )


def dump_xas(h5_file: str, xas_obj: Union[dict, XASObject]) -> None:
    """
    Save a XASObject in an hdf5 file.
    """
    if isinstance(xas_obj, dict):
        xas_obj = XASObject.from_dict(xas_obj)

    if not h5_file:
        _logger.warning("no output file defined, please give path to the output file")
        h5_file = input()

    _logger.info("dump xas obj to '%s'", h5_file)

    write_xas(
        h5_file=h5_file,
        energy=xas_obj.energy,
        mu=xas_obj.absorbed_beam(),
        entry=xas_obj.entry,
    )
