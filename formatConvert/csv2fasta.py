import csv
import os


def csv2fasta(csv_dir,
              fasta_dir,
              line_width=6,
              headers=True):

    with open(csv_dir, "r") as csv_file, open(fasta_dir, "w") as fasta_file:
        print("Input fasta directory: {:s}".format(fasta_dir))
        print("Output csv directory: {:s}".format(csv_dir))
        csv_reader = csv.reader(csv_file)
        for idx, entry in enumerate(csv_reader):
            if len(entry) == 0:
                continue
            paras = '>'
            for j in range(len(entry) - 1):
                paras += '{}|'.format(entry[j])
            fasta_file.write(paras + '\n')
            fasta_file.write('{}\n'.format(format_code(entry[-1], line_width)))
            print("Writing entry {:d}".format(idx), end="\r")
        print("Conversion finished. {:d} entries in total.".format(idx))
    

def format_code(code, line_width=80):
    length = len(code)
    output = ""
    for i in range(length // line_width):
        idx = i*line_width
        output += code[idx:idx+line_width]
        output += '\n'
    output += code[idx+line_width:]
    return output


if __name__ == "__main__":
    csv2fasta('C:\\Users\\white\\Desktop\\test.csv', 'C:\\Users\\white\\Desktop\\test_2.fa')