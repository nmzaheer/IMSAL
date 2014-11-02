from bs4 import BeautifulSoup
import requests

base_url = 'https://www.one.com/admin/'
login_url = base_url + 'login.do'
logout_url = base_url + 'logout.do'
mailalias_url = base_url + 'edit-alias.do'

#TODO : Modularize the code

def main():
    '''
    Algorithm
    ---------
    - Start a HTTP Session
    - Initialize parameters for logging in to www.one.com
    - Send a POST request with the params (This will log you into www.one.com)
    - Send a GET request to get details of recipients of the mailing list
    - Find the token value required for changing the mailing list members
    - Find all recipients and add/remove recipients as needed
    - Initialize the params and send a POST request to save the new list
    - Logout from the session
    '''
    s = requests.Session()
    payload = {'loginDomain':'true', 'targetDomain':'', 'loginTarget':''}
    payload['displayUsername'] = 'imsal.leuven@gmail.com'
    payload['username'] = 'imsal.leuven@gmail.com'
    payload['password1'] = 'imsalftp1'
    r = s.post(login_url, data=payload)
    r = s.get(mailalias_url + '?name=general_members_2014')
    soup = BeautifulSoup(r.content)
    token = soup.find(id='mailAliasForm').find('input')['value']
    recipients = [x['value'] for x in soup.find(id='mailAliasForm').find_all('input') if x['name'] == 'recipients']
    params = {
        'org.apache.struts.taglib.html.TOKEN' : token,
        'name' : 'general_members_2014',
        'enabled' : 'true',
        'removeRecipient' : '',
        'addRecipient' : '',
        'recipients' : recipients,
        'Save' : 'Save'
        }
    r = s.post(mailalias_url, data=params)
    r = s.get(logout_url)


if __name__ == '__main__':
    main()
