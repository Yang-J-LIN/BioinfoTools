import csv
import os


def fasta2csv(fasta_dir,
              csv_dir,
              columns=None):
    with open(fasta_dir, "r") as fasta_file, open(csv_dir, "w") as csv_file:
        print("Input fasta directory: {:s}".format(fasta_dir))
        print("Output csv directory: {:s}".format(csv_dir))
        csv_writer = csv.writer(csv_file) 
        entry = columns
        entry_num = 0
        while True:
            line = fasta_file.readline()
            if line is None or line == "":
                break
            elif line == "\n":
                continue
            line = line.split("\n")[0]
            if line[0] == ">":
                if entry is not None:
                    csv_writer.writerow(entry)
                    print("Writing entry {:d}".format(entry_num), end="\r")
                    entry_num += 1
                entry = line.split("|")
                entry[0] = entry[0][1:]
            else:
                entry[-1] = entry[-1] + line
        csv_writer.writerow(entry)
        entry_num += 1
        print("Conversion finished. {:d} entries in total.".format(entry_num))


if __name__ == "__main__":
    fasta2csv('C:\\Users\\white\\Desktop\\test.fa', 'C:\\Users\\white\\Desktop\\test.csv')