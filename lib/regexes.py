import re

regexes = {
    'email': re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}', re.I),
    #'mail-pass' : re.compile('^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\s*?[:|\||/]\s*?\w[4-50]\n'),
    #'userpass' : re.compile('^\w{4-50}\s*?[;|:|\||/|\t]+?\s*?\w{4-50}[:|\||/\n|\s]?'), try with a new one
    #'userpass' : re.compile('\w*?\s*?[;|:|\||/|\s]*?\s*?\w*?@\w*?[:|\||/|\s]?'),
    'userpass' : re.compile('[A-Z0-9._%+-]+@[A-Z0-9.-]*?\.?[A-Z]{2,4}\s*?[;|:|\||\s]+?\s*?\w{5,}', re.I),
    #'ssn' : re.compile(r'\d{3}-?\d{2}-?\d{4}'),
    'hash32': re.compile('([A-F\d]{32})', re.I),
    'sha1' : re.compile('[0-9a-fA-F]{40}'),
    'md5_wp' : re.compile('\$.\$.{31}'),
    'imei' : re.compile('[0-9]{2}-[0-9]{6}-[0-9]{6}-([0-9]?|[0-9]{2})'),  #AAAAAA-BB-CCCCCC-D
    'shadow' : re.compile('.*?(:(.)*?){8}'),
    'ip' : re.compile('[0-2]?[0-9]?[0-9]+?(\.[0-2]?[0-9]?[0-9]+?){3}'),
    'FFF': re.compile(r'FBI\s*Friday', re.I),  # will need to work on this to not match CSS
    'lulz': re.compile(r'(lulzsec|antisec)', re.I),
    'cisco_hash': re.compile(r'enable\s+secret', re.I),
    'cisco_pass': re.compile(r'enable\s+password', re.I),
    'google_api': re.compile(r'\W(AIza.{35})'),
    'honeypot': re.compile(r'<dionaea\.capture>', re.I),
    #'twitter' : re.compile('(@[^\.]+)|(twitter.com/\w+)'),
    'twitter' : re.compile('(^@([A-Za-z0-9_]+))|(twitter.com/\w+)'),
    'phonenum' : re.compile('(\d{1,4}[\s|-|/]?\d{1,4})+?'), #first stub
    'credit_card': re.compile('[\||:|;|\s]+?(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})[\s|\||:|;]+?'),
    'ssn' : re.compile('[([a-zA-Z]{6}[0-9]{2}[a-zA-Z][0-9]{2}[a-zA-Z][0-9]{3}[a-zA-Z])|(\d{3}-\d{2}-\d{4})]')
    'db_keywords': [
    re.compile(
    r'((customers?|email|users?|members?|acc(?:oun)?ts?)([-_|/\s]?(address|name|id[^")a-zA-Z0-9_]|[-_:|/\\])))', re.I),
        re.compile(
            r'((\W?pass(w)??(or)??(d??)|hash)[\s|:])', re.I),
        re.compile(
            r'((\btarget|\bsite)\s*?:?\s*?(([a-z][\w-]+:/{1,3})?([-\w\s_/]+\.)*[\w=/?%]+))', re.I),  # very basic URL check - may be improved later
        re.compile(
            r'(my\s?sql[^i_\.]|sql\s*server)', re.I),
        re.compile(
            r'((host|target)[-_\s]+ip:)', re.I),
        re.compile(
            r'(data[-_\s]*base|\Wdb)', re.I),  # added the non-word char before db.. we'll see if that helps
        re.compile(r'(table\s*?:)', re.I),
        re.compile(
            r'((available|current)\s*(databases?|dbs?)\W)', re.I),
        re.compile(r'(hacked\s*by)', re.I)
    ],
    'blacklist': [  # I was hoping to not have to make a blacklist, but it looks like I don't really have a choice
    re.compile(
    r'(select\s+.*?from|join|declare\s+.*?\s+as\s+|update.*?set|insert.*?into)', re.I),  # SQL
        re.compile(
            r'(define\(.*?\)|require_once\(.*?\))', re.I),  # PHP
        re.compile(
            r'(function.*?\(.*?\))', re.I),
        re.compile(
            r'(Configuration(\.Factory|\s*file))', re.I),
        re.compile(
            r'((border|background)-color)', re.I),  # Basic CSS (Will need to be improved)
        re.compile(
            r'(Traceback \(most recent call last\))', re.I),
        re.compile(
            r'(java\.(util|lang|io))', re.I),
        re.compile(r'(sqlserver\.jdbc)', re.I)
    ],
    # The banlist is the list of regexes that are found in crash reports
    'banlist': [
        re.compile(r'faf\.fa\.proxies', re.I),
        re.compile(r'Technic Launcher is starting', re.I),
        re.compile(r'TDSS rootkit removing tool', re.I),
        re.compile(r'INFO: Processing cookbook_file', re.I),
        re.compile(r'loading\.target\.rdio', re.I),
        re.compile(r'<key>SysInfoCrashReporterKey</key>', re.I)
    ]
}
