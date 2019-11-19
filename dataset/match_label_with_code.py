import os
import csv


def match(matched_dir,
          matching_dir,
          output_dir,
          matched_key_column=0,
          matching_key_column=0,
          matched_column=-1,
          matching_column=-1,
          matched_header=True,
          matching_header=True,
          output_header=True,
          insert=True,
          delimiter=','):
    """ Match two files.

    Match two files with the key. The keys in both files should be in ascending
    order.

    If the matched_dir is directed to the csv file as follows:
        idx,attr1
        E1,RRR
        E2,OOO
        E3,MMM
    and the matching_dir is directed to the csv file as follows:
        idx,attr2
        E1,LLLLLLLLLLLLL
        E3,MMMMMMMMMMMMM
        E7,AAAAAAAAAAAAA
    then match(matched_dir, matching_dir, output_dir) will creates a csv file
    as follows:
        idx,attr1,attr2
        E1,RRR,LLLLLLLLLLLLL
        E3,MMM,MMMMMMMMMMMMM

    Args:
        matched_dir: directory of matched file. The matching column will be
                     added to this file according to the key.
        matching_dir: directory of matching file.
        matched_key_column: column index of the matched key.
        matching_key_column: column index of the matching key.
        matched_column: column to be inserted or overwritten.
        matching_column: column to be added to the matched file.
        matched_header: whether the csv file contains the header.
        matching_header: whether the csv file contains the header.
        insert: insertion if true; else overwriting.
    """
    with open(matched_dir, 'r') as matched, \
            open(matching_dir, 'r') as matching, \
            open(output_dir, 'w', newline='') as output:
        csv_writer = csv.writer(output)
        if matched_header is True:
            matched_headers = \
                matched.readline().split('\n')[0].split(delimiter)
        if matching_header is True:
            matching_headers = \
                matching.readline().split('\n')[0].split(delimiter)
        if output_header is True:
            if matched_header is not True or matching_header is not True:
                print('Header information not found.')
            else:
                if insert is True:
                    matched_headers.insert(
                        matched_column % (len(matched_headers) + 1),
                        matching_headers[matching_column]
                    )
                else:
                    matched_headers[matched_column] = \
                        matching_headers[matching_column]
                csv_writer.writerow(matched_headers)

        matching_line = matching.readline()
        while True:
            matched_line = matched.readline()
            if not matched_line:
                break
            matched_entry = matched_line.split('\n')[0].split(delimiter)
            output_entry = matched_entry.copy()
            while True:
                if not matching_line:
                    break
                matching_entry = matching_line.split('\n')[0].split(delimiter)
                if matching_entry[matching_key_column] < \
                        matched_entry[matched_key_column]:
                    matching_line = matching.readline()
                    continue
                elif matching_entry[matching_key_column] == \
                        matched_entry[matched_key_column]:
                    if insert is True:
                        output_entry.insert(
                            matched_column % (len(matched_entry) + 1),
                            matching_entry[matching_column]
                        )
                    else:
                        output_entry[matched_column] = \
                            matching_entry[matching_column]
                    csv_writer.writerow(output_entry)
                    break
                else:
                    break


if __name__ == "__main__":
    match(
        'C:\\Users\\white\\Desktop\\FILE1.CSV',
        'C:\\Users\\white\\Desktop\\FILE2.CSV',
        'C:\\Users\\white\\Desktop\\FILE3.CSV'
    )
