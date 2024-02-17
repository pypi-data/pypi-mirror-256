from lxml import etree
from .drs_file import DrsFile
import logging

class DrsDescriptor():
  
  NSMAP = {
    "mets" : "{http://www.loc.gov/METS/}",
    "hulDrsAdmin" : "{http://hul.harvard.edu/ois/xml/ns/hulDrsAdmin}",
    "premis" : "{info:lc/xmlns/premis-v2}",
    "xsi" : "{http://www.w3.org/2001/XMLSchema-instance}",
  }
  
  def __init__(self, descriptor_file):
    self.files = {}
    self.root = etree.parse(descriptor_file).getroot()
    self._parse()

  def __repr__(self) -> str:
    out = ""
    if len(self.files) > 0:
      for f in self.files:
        out += f'{f}\n'
    else:
      out += 'No files found\n'

    if len(self.amds) > 0:
      for amd in self.amds:
        out += f'{amd}\n'
    else:  
      out += 'No AMDs found\n'

    return out


  def _parse(self):
    # Collect METS:files and their corresponding METS:AmdSecs
    file_grps = self.root.findall('.//{}fileGrp'.format(self.NSMAP['mets']))
    grps = {}
    for file_grp in file_grps:
      file_grp_id = file_grp.get('ID')
      grp = {file_grp_id: {}}

      files = file_grp.findall('{}file'.format(self.NSMAP['mets']))
      for file in files:
        file_id = file.get('ID')
        file_amd_ids = file.get('ADMID')      
        grp[file_grp_id][file_id] = file_amd_ids

      grps.update(grp)
        
    # Associate METS:files with DRS:files
    for grp in grps.values():
      for file_id, amd_ids in grp.items():
        drs_file = self._create_drs_file(amd_ids)
        self.files[drs_file.get_id()] = drs_file

  
  def _create_drs_file(self, amd_ids):
    """
    Given a list of amd_ids, create a DRS file object.
    """
    drs_file = DrsFile()
    amd_secs = self.root.findall(".//{}amdSec".format(self.NSMAP['mets']))

    for amd_id in amd_ids.split():

      amd_premis_file = self._amdSec_premis_file(amd_secs, amd_id)
      if amd_premis_file is not None:
        drs_file.set_id(amd_premis_file.find('.//{}objectIdentifierValue'.format(self.NSMAP['premis'])).text)
        continue

      amd_drs_file = self._amdSec_drs_file(amd_secs, amd_id)
      if amd_drs_file is not None:
        drs_file.set_file_name(amd_drs_file.find('.//{}suppliedFilename'.format(self.NSMAP['hulDrsAdmin'])).text)
        drs_file.set_file_dir(amd_drs_file.find('.//{}suppliedDirectory'.format(self.NSMAP['hulDrsAdmin'])).text)
        continue

    return drs_file 

    
  def _amdSec_premis_file(self, amd_secs, amd_id):    
    for amd_sec in amd_secs:
        if amd_sec.get('ID') == amd_id:
           premis_obj = amd_sec.find('.//{}object'.format(self.NSMAP['premis']))
           if premis_obj is not None and premis_obj.get('{}type'.format(self.NSMAP['xsi'])) == 'premis:file':
              return premis_obj
    return None
  
    
  def _amdSec_drs_file(self, amd_secs, amd_id):
    for amd_sec in amd_secs:
        if amd_sec.get('ID') == amd_id:
           amd_drs_file = amd_sec.find('.//{}drsFile'.format(self.NSMAP['hulDrsAdmin']))
           if amd_drs_file is not None:
              return amd_drs_file
    return None    
  

  def _amdSec_premis_representation(self, amd_secs, amd_id):    
    for amd_sec in amd_secs:
        if amd_sec.get('ID') == amd_id:
           premis_obj = amd_sec.find('.//{}object'.format(self.NSMAP['premis']))
           if premis_obj is not None and premis_obj.get('{}type'.format(self.NSMAP['xsi'])) == 'premis:representation':
              return premis_obj
    return None
  

  def get_batch_name(self):
    mets_hdr = self.root.find("{}metsHdr".format(self.NSMAP['mets']))
    mets_hdr_amd_ids = mets_hdr.get('ADMID')      
    amd_secs = self.root.findall(".//{}amdSec".format(self.NSMAP['mets']))

    for amd_id in mets_hdr_amd_ids.split():
      amd_premis_representation = self._amdSec_premis_representation(amd_secs, amd_id)
      if amd_premis_representation is not None:
        return amd_premis_representation.find('.//{}originalName'.format(self.NSMAP['premis'])).text


  def get_files(self):
    return self.files


