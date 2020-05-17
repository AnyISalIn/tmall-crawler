USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

}

FOOTER_ID = 'footer'
HEADER_ID = 'header'

DELETE_ELEMENT = [
    ('div', {'id': 'site-nav'}),
    ('div', {'id': FOOTER_ID}),
    ('div', {'id': HEADER_ID}),
    ('script', {'async': ""}),
    ('div', {'class': 'mui-mbar'}),
    ('div', {'class': 'WW'})
]

REDIS_URL = 'redis://localhost:6379/0'

ANALYSIS_CODE = '''
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?f4c47456b515ed7bc521baa8678c6362";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
'''

TASK_LIST = 'http://localhost:5000/task/list'
