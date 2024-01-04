import PyPDF2
import re

# 3 example pdf's im using for now
pdf_path1 = 'Data_Project_Sample_Letter.pdf'
pdf_path2 = 'sample2.pdf'
pdf_path3 = 'sample3.pdf'

start_flag = False


# Function that, given a path to a pdf file, extracts the first 2 pages of data and stores in variable pdf_text. (I only scan first 2 pages because I've yet to run into a file that
# has the data I need past page 1 or 2)
def get_text(path):
    pdf_text = ""
    with open(path, 'rb') as pdf_file: 
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for i in range(2):
            pdf_text += pdf_reader.pages[i].extract_text()
    pdf_file.close()
    return pdf_text

# Function that, given a variable holding a segment of text from pdf, uses regex to find and strip the section labeled 'What Happened' and returns
# *** I need to add error handling that returns void if its even 1% unsure about the data it found / didnt find
def find_what_happened_section(pdffile):
    start_pattern = r'What Happened'
    end_pattern = r'What Information Was Involved'
    start_match = re.search(start_pattern, pdffile)
    end_match = re.search(end_pattern, pdffile)
    if start_match and end_match:
        start_index = start_match.start()
        end_index = end_match.start()
        what_happened_section = pdffile[start_index:end_index].strip()
        what_happened_section = re.sub(r'\n', ' ', what_happened_section).lower()
        what_happened_section = re.sub(r'  ', ' ', what_happened_section)
        return what_happened_section
    else:
        print("What Happened Section Not Found in Document")

# Function that, given a variable holding a segment of text from pdf, uses regex to find and strip the section labeled 'What Happened' and returns
# *** I need to add error handling that returns void if its even 1% unsure about the data it found / didnt find
def find_info_section(pdffile):
    start_pattern = r'What Information Was Involved'
    end_pattern = r'What We Are Doing'
    start_match = re.search(start_pattern, pdffile)
    end_match = re.search(end_pattern, pdffile)
    if start_match and end_match:
        start_index = start_match.start()
        end_index = end_match.start()
        info_section = pdffile[start_index:end_index].strip()
        info_section = re.sub(r'\n', ' ', info_section).lower()
        info_section = re.sub(r'  ', ' ', info_section)
        return info_section
    else:
        print("What Info Was Involved Section not found in File")


# Example Usages
my_pdf_text1 = get_text(pdf_path1)
my_pdf_text2 = get_text(pdf_path2)
my_pdf_text3 = get_text(pdf_path3)
what_happened_section1 = find_what_happened_section(my_pdf_text1)
info_section1 = find_info_section(my_pdf_text1)
what_happened_section2 = find_what_happened_section(my_pdf_text2)
info_section2 = find_info_section(my_pdf_text2)
what_happened_section3 = find_what_happened_section(my_pdf_text3)
info_section3 = find_info_section(my_pdf_text3)

print("Info Section:\n")
print(info_section1)
print("\nWhat Happened Section:\n")
print(what_happened_section1)
print("\nInfo Section:\n")
print(info_section2)
print("\nWhat Happened Section:\n")
print(what_happened_section2)
print("nInfo Section:\n")
print(info_section3)
print("\nWhat Happened Section:\n")
print(what_happened_section3)

