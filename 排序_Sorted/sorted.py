def get_score_str():
    import requests, re
    url = 'https://github.com/wfhsiao/python_learning/raw/master/data/scores.txt'
    r=requests.get(url, stream=True)
    result=[]
    for line in r.iter_lines():
        line = line.decode('utf-8-sig')
        result.append(line)

    student = [line.split('\t') for line in result[1:]]

    sorted_student = sorted(student , key = lambda x: int(x[1]) , reverse = True)

    return sorted_student

print(get_score_str())