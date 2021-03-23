class ValidationError(Exception):
	def __init__(self, path, *args, **kwargs):
		super(ValidationError, self).__init__(*args)
		self.path = path
		self.inner = kwargs.get('inner', [])
