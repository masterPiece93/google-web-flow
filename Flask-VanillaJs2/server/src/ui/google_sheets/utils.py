import re

def get_specific_sheets(sheet: object, sheet_id: str, range: str) -> list:

    result = (
          sheet.values()
          .get(spreadsheetId=sheet_id, range=range)
          .execute()
      )
    values: list = result.get("values", [])
    return values

def get_all_sheets_data(sheet: object, sheet_id: str, without_headers: bool =False) -> list:
    """
    - properties:
        - gridProperties:
            - columnCount: 26
            - rowCount: 1000
        - index: 1
        - sheetId: 546508778
        - sheetType: 'GRID'
        - title: 'Sheet2'
    """
    result = (
          sheet
          .get(spreadsheetId=sheet_id)
          .execute()
      )
    sheet_metadata: list = result.get("sheets", [])
    values = []
    for indivisual_sheet in sheet_metadata:
        _: str = indivisual_sheet.get('properties', {}).get('sheetId')
        title: str = indivisual_sheet.get('properties', {}).get('title')
        
        _range = f"{title}"
        if without_headers == True:
            _range = _range + "!" +"A2:z999999"
        values.append(get_specific_sheets(sheet, sheet_id, range=_range))
    return values

def extract_id_gid( url) -> tuple:
        """
        Extracts the ID and gid from a Google Sheet URL.

        Args:
            url: The Google Sheet URL.

        Returns:
            A tuple containing the ID and gid, or (None, None) if not found.
        """
        match = re.search(r"/d/([a-zA-Z0-9-_]+)(?:.*?gid=([0-9]+))?", url)
        if match:
            sheet_id = match.group(1)
            gid = match.group(2)
            return sheet_id, gid
        return None, None
    