def englishLearn(word, showList, filename='C:\\Users\\ivan1rufus\\Desktop\\wordsList.txt'):
    with open(filename, 'a+') as f:
        foundFlag = False
        #重定位
        f.seek(0)
        for eachline in f.readlines():
            if eachline.find(word) != '-1':
                #eachline.replace(eachline[eachline.index(':')+1], )
                foundFlag = True
                break
        if showList[1] == '无':
            foundFlag = True
        if foundFlag == False:
            newLine = '<' + word + '>' + 'count:0' + '\n'
            f.write(newLine)
            for eachShow in showList:
                f.write(eachShow + '\n')