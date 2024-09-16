import json

json_list = ['phishing.json', 'scambait.json', 'scams_data.json']

def load_data(i):
    with open(i, 'r') as f:
        data = json.load(f)
        return data
    
def count_posts():
    '''
    posts in phishing.json: 998
    posts in scambait.json: 964
    posts in scams_data.json: 994
    '''
    for i in json_list:
        data = load_data(i)
        print(f'posts in {i}:',len(data))

def count_image_posts():
    '''
        number of image posts: 358 which is 35.87% of phishing.json
        number of image posts: 558 which is 57.88% of scambait.json
        number of image posts: 575 which is 57.85% of scams_data.json
    '''
    for i in json_list:
        count=0
        count1=0
        data = load_data(i)
        for j in data:
            if j['selftext'] == "":
                count+=1
            count1+=1
        print(f'number of image posts: {count} which is {round((count/count1)*100,2)}% of {i}')

count_image_posts()


    
