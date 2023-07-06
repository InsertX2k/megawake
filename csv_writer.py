"""
CSV Writer module for megawake

This file here comes as a fix or an extension to the functionality of Python's built-in CSV module, especially to address the issues it had when using it with megawake program.

This module allows you to:

* Write your rows (must be specified in a list) to a csv file
* Access Defined Exception classes in this module for later use in any other modules

License:

    A CSV Writer module for the program 'megawake' and other programs licensed under the same license.
    
    Copyright (C) 2023 Insertx2k Dev (Mr.X) or Ziad Ahmed (Mr.X)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
class ErrorOpeningTargetCSVFile(Exception):
    def __init__(self, *args: object) -> None:
        """
        Class for the raised exception when an occurs while trying to open the target CSV File for writing.
        """
        super().__init__(*args)

class ErrorWritingRowsToCSVFile(Exception):
    def __init__(self, *args: object) -> None:
        """
        Class for raised exception when an error occurs while trying to write the rows to the target CSV file.
        """
        super().__init__(*args)

def write_list_to_csv_file(csvFileName, csvRowsList):
    """
    Write the given row(s) from the list `csvRowsList` into the given csv file specified in `csvFileName` parameter.
    """
    try:
        csv_writer = open(csvFileName, mode='w', encoding='utf-8')
    except Exception as errorOpeningCSVFile:
        raise ErrorOpeningTargetCSVFile(errorOpeningCSVFile)
    
    
    # emptying the file first.
    try:
        csv_writer.write('')
        for row in csvRowsList:
            csv_writer.write(f"{row[0]},{row[1]},{row[2]},{row[3]}\n")
        csv_writer.close() # IMPORTANT!!!
    except Exception as errorWritingToTargetCSVFile:
        raise ErrorWritingRowsToCSVFile(errorWritingToTargetCSVFile)

    return

if __name__ == '__main__':
    pass