def filter_func(emails):
    res = []
    for email in emails:
        mail = email.partition('@')
        flag = True
        for i in mail[0]:
            if not(i.isalnum() or '_' in i):
                flag = False
        if flag == False:
            continue

        flag = True
        for i in mail[2]:
             if not (i.isalnum() or '.' in i):
                flag = False

        if flag == False:
            continue
        else:
            dom = mail[2].split('.')
            print(dom)
            print(len(dom))
            length=0
            for each in dom:
                length+= len(each)
        if length>2 and (not '' in dom):
            res.append(email)
    return res

emails = ['abs@co.com','ab/c@gmail.com.ua', '*@ank.com', '_ny@us.gov.us', 'z@b.k']

print(filter_func(emails))