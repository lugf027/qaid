import re, sys, getopt, time


def kill_tags(html_name, output_name):
    f_html = open(html_name, mode='r', encoding='utf-8')
    html = f_html.read()

    reg1 = r'(。\s*<.+?>)'
    tag_re1 = re.compile(reg1)
    tag_list1 = re.findall(tag_re1, html)

    for tag1 in tag_list1:
        html = html.replace(tag1, '$')

    reg1 = r'("\s*<.+?>)'
    tag_re1 = re.compile(reg1)
    tag_list1 = re.findall(tag_re1, html)

    for tag1 in tag_list1:
        html = html.replace(tag1, '$')

    reg1 = r'(”\s*<.+?>)'
    tag_re1 = re.compile(reg1)
    tag_list1 = re.findall(tag_re1, html)

    for tag1 in tag_list1:
        html = html.replace(tag1, '$')

    reg1 = r'([\u4e00-\u9fa5]+|\$)'
    tag_re1 = re.compile(reg1)
    tag_list1 = re.findall(tag_re1, html)

    result = ''
    for tag1 in tag_list1:
        result += tag1

    num = result.count('$')
    print(num)

    f_killed = open(output_name, mode='w', encoding='utf-8')
    f_killed.write(result)
    f_killed.close()

'''
def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print("translating: " + inputfile + " to " + outputfile + " now~")
    t1 = time.time()
    kill_tags(inputfile, outputfile)
    t2 = time.time()
    print("Total:" + str(1000 * (t2 - t1)) + "ms")


if __name__ == "__main__":
   main(sys.argv[1:])
'''


