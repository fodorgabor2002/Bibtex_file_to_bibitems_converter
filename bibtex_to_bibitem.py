from collections import Counter

# filename: bibtex2item.py
# python bibtex2item.py
# keep the bibtex in refs.bib file


def convert(bibtex):
    bibitem = ''
    r = bibtex.split('\n')
    i = 0
    while i < len(r):
        line = r[i].strip()
        if not line: i += 1
        if '@' == line[0]:
            bibitem += "\n\t"
            code = line.split('{')[-1][:-1]
            title = venue = volume = number = pages = year = publisher = howpublished = note = doi = authors, url = None
            #URL-t nem szedi ki
            output_authors = []
            i += 1
            while i < len(r) and ('@' not in r[i] or ('@' in r[i] and '/@' in r[i])):
                line = r[i].strip()
                #print(line)
                if line.startswith("title"):
                    title = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("journal"):
                    venue = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("volume"):
                    volume = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("number"):
                    number = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("pages"):
                    pages = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("doi"):
                    doi = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("year"):
                    year = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("publisher"):
                    publisher = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("howpublished"):
                    howpublished = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("note"):
                    note = line[line.find("{") + 1:line.rfind("}")]
                elif line.startswith("author"):
                    authors = line[line.find("{") + 1:line.rfind("}")]
                    for LastFirst in authors.split('and'):
                        lf = LastFirst.replace(' ', '').split(',')
                        if len(lf) != 2:
                            #output_authors.append("{}.".format(authors.capitalize()))
                            output_authors.append("{}.".format(authors))
                        else:
                            last, first = lf[0], lf[1]
                            #output_authors.append("{}, {}.".format(last.capitalize(), first.capitalize()[0]))
                            output_authors.append("{}, {}.".format(last, first[0]))
                            #print(last, first, first[0])

                        #UniqW = Counter(input)
                        # joins two adjacent elements in iterable way
                        #output_authors = " ".join(Counter(output_authors).keys())
                        output_authors = [name for name in Counter(output_authors).keys()]
                i += 1

            bibitem += "\\bibitem{%s}" % code
            if len(output_authors) == 1:
                bibitem += str(output_authors[0] + " {}. ".format(title))
            else:
                bibitem += ", ".join(_ for _ in output_authors[:-1]) + " & " + output_authors[-1] + " {}. ".format(title)
            if venue:
                bibitem +="{{\\em {}}}.".format(" ".join([_.capitalize() for _ in venue.split(' ')]))
                if volume:
                    bibitem += " \\textbf{{{}}}".format(volume)
                if pages:
                    bibitem += ", {}".format(pages) if number else " pp. {}".format(pages)
                if year:
                    bibitem += " ({})".format(year)
            if publisher and not venue:
                bibitem += "({},{})".format(publisher, year)
            if not venue and not publisher and year:
                bibitem += " ({})".format(year)
            if howpublished:
                bibitem += ", {}".format(howpublished)
            if note:
                bibitem += ", {}".format(note)
                if not "Accessed" in note:
                    bibitem += ", [Accessed 16-05-2024]"
            if not note:
                bibitem += ", [Accessed 16-05-2024]"
            if doi:
                bibitem += ", doi: {}".format(doi)
        while("  " in bibitem):
            bibitem = bibitem.replace("  ", " ")
    return bibitem.replace("_", "\_") + "\n"

fbibtex = open('references.bib', 'r', encoding="utf8").read()
#with open('references.bib', 'r', encoding="utf8") as fbibtex:
#    bibtex = fbibtex.read()

bibitems = convert(fbibtex)
#print(bibitems)

with open("bibitems.txt", 'w+', encoding="utf8") as fbibitems:
    fbibitems.write(bibitems)
print("Done")