

'''
	{ verify, approve, validate, certify, vouch }
'''

'''
	import story_1.modules.EEC_448_2.verify as verify
	verified = verify.start (
		public_key_string,
		
		signed_bytes = signed_bytes,
		unsigned_bytes = unsigned_bytes
	)
'''

from Crypto.Signature import eddsa
from Crypto.PublicKey import ECC

def start (
	public_key_instance = None,
	
	unsigned_bytes = None,
	signed_bytes = None
):
	verifier = eddsa.new (public_key_instance, 'rfc8032')
	
	try:
		verifier.verify (unsigned_bytes, signed_bytes)		
		return "yes";
		
	except Exception as E:
		print ("exception:", E)
		
		#
		#	for example, "The signature is not authentic"
		#
	
		pass;
				
	return "no";