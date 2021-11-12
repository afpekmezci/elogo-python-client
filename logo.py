from zeep import Client
from utils.CustomTypes import get_array_of_string_type
from utils.TimeUtil import TimeConvert
from utils.DocumentTypes import DocumentTypes
import logging.config
import getpass
logger = logging.getLogger(__name__)
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

class LogoClient:
	
	logo_url = 'https://pb-demo.elogo.com.tr/postboxservice.svc?singlewsdl'
	session_id = None
	date_frmt = '%Y-%m-%d'
	client_id = None
	password = None
	def __init__(self, client_id, client_password):
		self.client_id = client_id
		self.password = client_password
		self.login()


	def client(self):
		client = Client(self.logo_url)
		client.set_ns_prefix('tem', "http://tempuri.org/")
		client.set_ns_prefix('arr', "http://schemas.microsoft.com/2003/10/Serialization/Arrays")
		return client


	def login(self):
		request_data = {
			'userName' : self.client_id,
			'passWord': self.password,
		}
		req = self.client().service.Login(request_data)
		if req.LoginResult:
			self.session_id = req.sessionID
		else:
			raise ValueError('cannot login to system')


	def logout(self):
		self.client().service.Logout(**self.get_session())


	def get_session(self):
		return {'sessionID': self.session_id}


	def send_document(self):
		paramsList = {'paramList':[]} 
		request_data = {**self.get_session(), **paramsList}
		request = self.client().service.SendDocument(request_data)
		self.logout()
		return request


	def get_document(self):
		paramsList = {'paramList':[DocumentTypes().get_param_string(DocumentTypes.efatura)]} 
		request_data = {**self.get_session(), **paramsList}
		request = self.client().service.SendDocument(request_data)
		self.logout()
		return request


	def get_document_done(self, document_id):
		document = {'uuid': document_id}
		paramsList = {'paramList':[DocumentTypes().get_param_string(DocumentTypes.efatura)]}
		request_data = {**self.get_session(), **document, **paramsList}
		request = self.client().service.GetDocumentDone(request_data)
		self.logout()
		return request
	

	def get_document_list(self, begin_date=None, end_date=None):
		begin_date = begin_date if begin_date is not None else TimeConvert().start_or_end_wtih_tz(TimeConvert().get_current_time(), 'end')
		end_date = end_date if end_date is not None else TimeConvert().start_or_end_wtih_tz(TimeConvert().get_current_time(), 'end')
		begin_date = TimeConvert().convert_to_human_readeble(begin_date.timestamp(), self.date_frmt)
		end_date = TimeConvert().convert_to_human_readeble(end_date.timestamp(), self.date_frmt)
		paramlist = get_array_of_string_type(self.client(), [f"DOCUMENTTYPE={DocumentTypes.efatura}", f"BEGINDATE={begin_date}", f"ENDDATE={end_date}", "OPTYPE=2", "DATEBY=0"])
		return self.client().service.GetDocumentList(**self.get_session(), paramList=paramlist )
if __name__ == "__main__":
	client_id = input('Vergi Numarası : ')
	client_password = getpass.getpass('Password:')
	documents = LogoClient(client_id=client_id, client_password=client_password).get_document_list()
	print(documents)

