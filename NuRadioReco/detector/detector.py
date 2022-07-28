import NuRadioReco.detector.detector_base
import NuRadioReco.detector.generic_detector
import json

class Detector(object):
    def __new__(
            cls,
            json_filename,
            source='json',
            dictionary=None,
            assume_inf=True,
            antenna_by_depth=True
    ):
        """
        Initialize the stations detector properties.
        This method will check if the JSON file containing the detector description is set up to be used by
        the DetectorBase or GenericDetector class and cause the correct class to be created.

        Parameters
        ----------
        json_filename : str
            the path to the json detector description file (if first checks a path relative to this directory, then a
            path relative to the current working directory of the user)
            default value is 'ARIANNA/arianna_detector_db.json'
        source: str
            'json' or 'dictionary'
            default value is 'json'
            If 'json' is passed, the JSON dictionary at the location specified
            by json_filename will be used
            If 'dictionary' is passed, the dictionary specified by the parameter
            'dictionary' will be used
        dictionary: dict
            If 'dictionary' is passed to the parameter source, the dictionary
            passed to this parameter will be used for the detector description.
        assume_inf : Bool
            Default to True, if true forces antenna madels to have infinite boundary conditions, otherwise the antenna
            madel will be determined by the station geometry.
        antenna_by_depth: bool (default True)
            if True the antenna model is determined automatically depending on the depth of the antenna.
            This is done by appending e.g. '_InfFirn' to the antenna model name.
            if False, the antenna model as specified in the database is used.
        """
        if source == 'json':
            f = open(json_filename, 'r')
            station_dict = json.load(f)
        elif source == 'dictionary':
            station_dict = dictionary
        else:
            raise ValueError('Source must be either json or dictionary!')
        reference_entry_found = False
        for station in station_dict['stations']:
            if 'reference_station' in station_dict['stations'][station].keys():
                reference_entry_found = True
                break
        for channel in station_dict['channels']:
            if 'reference_channel' in station_dict['channels'][channel].keys() or 'reference_station' in \
                    station_dict['channels'][channel].keys():
                reference_entry_found = True
                break
        if source == 'json':
            f.close()
        if reference_entry_found:
            det = object.__new__(NuRadioReco.detector.generic_detector.GenericDetector)
            det.__init__(
                json_filename=json_filename,
                source='json',
                dictionary=None,
                assume_inf=True,
                antenna_by_depth=True
            )
        else:
            det =  object.__new__(NuRadioReco.detector.detector_base.DetectorBase)
            det.__init__(
                source='json',
                json_filename=json_filename,
                dictionary=None,
                assume_inf=True,
                antenna_by_depth=True
            )
        return det