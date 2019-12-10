import os
import pprint
import csv

import driveapi as api

pp = pprint.PrettyPrinter(indent=2)

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Get Drive Service
  service = api.get_authenticated_service2()

  # Get Team Drive
  #pp.pprint(api.get_teamdrive(service, '0ARwZ-TeGhK3jVk9PVA'))
  
  # List Team Drive
  #results = api.list_teamdrive(service)

  #pp.pprint(results)

  #for item in results:
  #  print(item.get('name') +','+item.get('id'))
  
  results = api.list_teamdrive2(service)
  
  for item in results:
    print('"'+item.get('name') +'","'+item.get('id')+'",')

  # Update Team Drive
  #api.api.update_teamdrive(service, '0ARwZ-TeGhK3jVk9PVA','Drive Test')

  # List Drive Files 
  #api.list_drive_files(service, orderBy='modifiedByMeTime desc', pageSize=10)
  #api.list_drive_files2(service, includeItemsFromAllDrives=False, pageSize=100)

  # Add Group to Team Drive 
  #api.add_group(service, '0ARwZ-TeGhK3jVk9PVA', 'user@test.com', role='fileOrganizer')
  
  # Create Team Drive
  #td_id = api.create_teamdrive(service, 'Drive_Teste')