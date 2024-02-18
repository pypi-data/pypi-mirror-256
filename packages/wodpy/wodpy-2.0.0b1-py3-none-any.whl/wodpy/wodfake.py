import numpy
from datetime import datetime, timedelta

class WodFake(object):
	'''
	class to mock a WOD profile object for convenience when testing other applications that consume wodpy
	'''

	def __init__(self, o):
		'''
		input object o (all keys optional):
		{
			depth: [[pressures], [mask]]
		}
		'''

		# simple single scalars and plain lists
		for key in ['latitude', 'latitude_unc', 'longitude', 'longitude_unc', 'uid', 'n_levels', 'year', 'month', 'day', 'time', 'cruise', 'PIs', 'originator_cruise', 'originator_station', 'originator_flag_type', 'probe_type', 't_profile_qc', 't_metadata', 's_profile_qc', 's_metadata']:
			if key in o:
				setattr(self, key, o[key])

		# level data (masked arrays)
		for key in ['z', 'z_unc', 'z_level_qc', 't', 't_unc', 't_qc_mask', 't_level_qc', 's', 's_unc', 's_qc_mask', 's_level_qc', 'oxygen', 'phosphate', 'silicate', 'pH', 'p']:
			if key in o:
				setattr(self, key, self.validate_mask(o[key])) 

	def validate_mask(self, o):
		if len(o) == 2 and isinstance(o[0], list):
			assert len(o[0]) == len(o[1]), "mask must either be omitted or be the same length as the list of values"
			return numpy.ma.masked_array(o[0], mask=o[1])
		else:
			return numpy.ma.masked_array(o, mask=[False]*len(o))

	def latitude(self):
		return self.latitude

	def latitude_unc(self):
		return self.latitude_unc

	def longitude(self):
		return self.longitude

	def longitude_unc(self):
		return self.longitude_unc

	def uid(self):
		return self.uid

	def n_levels(self):
		return self.n_levels

	def year(self):
		return self.year

	def month(self):
		return self.month

	def day(self):
		return self.day

	def time(self):
		return self.time

	def datetime(self):
	    """ Returns the date and time as a datetime object. """
	    time  = self.time()
	    if time is None or time < 0 or time >= 24:
	        time = 0

	    try:
	        d = datetime(self.year(), self.month(), self.day()) + \
	                timedelta(hours=time)
	        return d
	    except:
	        return

	def cruise(self):
		return self.cruise

	def PIs(self):
		return self.PIs

	def originator_cruise(self):
		return self.originator_cruise

	def originator_station(self):
		return self.originator_station

	def originator_flag_type(self):
		return self.originator_flag_type

	def probe_type(self):
		return self.probe_type

	def z(self):
		return self.z

	def z_unc(self):
		return self.z_unc

	def z_level_qc(self):
		return self.z_level_qc

	# var_* helpers: tbd what makes sense here

	def t(self):
		return self.t

	def t_unc(self):
		return self.t_unc

	def t_qc_mask(self):
		return self.t_qc_mask

	def t_level_qc(self):
		return self.t_level_qc

	def t_profile_qc(self):
		return self.t_profile_qc

	def t_metadata(self):
		return self.t_metadata

	def s(self):
		return self.s

	def s_unc(self):
		return self.s_unc

	def s_qc_mask(self):
		return self.s_qc_mask

	def s_level_qc(self):
		return self.s_level_qc

	def s_profile_qc(self):
		return self.s_profile_qc

	def s_metadata(self):
		return self.s_metadata

	def oxygen(self):
		return self.oxygen

	def phosphate(self):
		return self.phosphate

	def silicate(self):
		return self.silicate

	def pH(self):
		return self.pH

	def p(self):
		return self.p
