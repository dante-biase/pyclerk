import sys
import unittest
from typing import Any, Callable, Tuple, Type, Union

sys.path.append('..')

from pyclerk import path


class PathTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		pass

	@classmethod
	def tearDownClass(self):
		pass

	def assertEqual(self, first: Any, second: Any, msg: Any = ...) -> None:
		try:
			super(PathTest, self).assertEqual(first, second, msg)
		except self.failureException:
			self.fail(
					'\n\tinput:           ' + f'{msg}' +
					'\n\texpected output: ' + f'{first}' +
					'\n\treal output:     ' + f'{second}'
			)

	def assertRaises(self,  # type: ignore
	                 expected_exception: Union[Type[BaseException], Tuple[Type[BaseException], ...]],
	                 callable: Callable[..., Any],
	                 *args: Any, **kwargs: Any) -> None:

		input_s = kwargs['input_s']
		try:
			with super(PathTest, self).assertRaises(expected_exception):
				callable(*input_s)

		except self.failureException:
			self.fail(
					f'path.{callable.__name__}{input_s} did not throw {expected_exception.__name__}'
			)

	def test_cleanup(self):
		test_data = {
				''                  : '',
				'//'                : '/',
				'///A//B/C'         : '/A/B/C',
				'///A//B/C//'       : '/A/B/C',
				'///A//B/C//F.EXT'  : '/A/B/C/F.EXT',
				'///A//B/C//F.EXT//': '/A/B/C/F.EXT',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.cleanup(input_), input_)

		input_ = ['', '//', '///A//B/C', '///A//B/C//', '///A//B/C//F.EXT', '///A//B/C//F.EXT//']
		expected_output = ['', '/', '/A/B/C', '/A/B/C', '/A/B/C/F.EXT', '/A/B/C/F.EXT']
		self.assertEqual(expected_output, path.cleanup(input_), input_)

	def test_reorient(self):
		test_data = {
				'\A\B\C'      : '/A/B/C',
				'\A\B\C\F.EXT': '/A/B/C/F.EXT',
				'/A/B/C'      : '/A/B/C',
				'/A/B/C/F.EXT': '/A/B/C/F.EXT',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.reorient(input_), input_)

	def test_cat(self):
		test_data = {
				('', '')     : '',
				('', '/')    : '/',
				('/', '')    : '/',
				('/', '/')   : '/',
				('/A', 'B')  : '/A/B',
				('/A', '/B/'): '/A/B',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.cat(*inputs), inputs)

	def test_join(self):
		test_data = {
				()            : '',
				('', 'A/B')   : 'A/B',
				('/', 'A/B')  : '/A/B',
				('/', '/A/B/'): '/A/B',
				('A/B')       : 'A/B',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.join([*inputs]), [*inputs])

	def test_split(self):
		test_data = {
				('/')         : ['/'],
				('/A/B/F.EXT'): ['/', 'A', 'B', 'F.EXT'],
				('A/B/F.EXT') : ['A', 'B', 'F.EXT'],
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.split(input_), input_)

	def test_bisect(self):
		test_data = {
				('/A/B/F.EXT', 0) : ('/', 'A/B/F.EXT'),
				('/A/B/F.EXT', 1) : ('/A', 'B/F.EXT'),
				('/A/B/F.EXT', -3): ('/A', 'B/F.EXT'),
				('/A/B/F.EXT', -1): ('/A/B', 'F.EXT'),
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.bisect(*inputs), inputs)

	def test_strip_root(self):
		test_data = {
				'/'  : '',
				'/A' : 'A',
				'A/B': 'B',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.strip_root(input_), input_)

	def test_strip_tail(self):
		test_data = {
				'/'    : '',
				'/A'   : 'A',
				'A/B'  : 'B',
				'/A/B' : 'B',
				'/A/B/': 'B',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.strip_trail(input_), input_)

	def test_strip_base(self):
		test_data = {
				'/'    : '',
				'/A'   : '/',
				'A/B'  : 'A',
				'/A/B' : '/A',
				'/A/B/': '/A',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.strip_base(input_), input_)

	def test_strip_ext(self):
		test_data = {
				'/'       : '/',
				'/A'      : '/A',
				'/A/'     : '/A',
				'F.EXT'   : 'F',
				'F.EXT/'  : 'F',
				'/F.EXT/' : '/F',
				'A/F.EXT/': 'A/F',
				'/A/F.EXT': '/A/F',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.strip_ext(input_), input_)

	def test_replace(self):
		test_data = {
				('/A/B/', '', '/A/B/C')  : 'C',
				('A/B/', '', 'A/B/C')    : 'C',
				('/', '/A', '/B/C/')     : '/A/B/C',
				('/', '/A/', '/B/C/')    : '/A/B/C',
				('/', '/A/', '/B/C/')    : '/A/B/C',
				('/', '/A', '/B/C/')     : '/A/B/C',
				('/', 'A/', '/B/C/')     : 'A/B/C',
				('/B', '/D', '/B/C/')    : '/D/C',
				('/B/', '/D', '/B/C/')   : '/D/C',
				('/B/', '/D/', '/B/C/')  : '/D/C',
				('/B', 'D', '/B/C/')     : 'D/C',
				('/B/', 'D', '/B/C/')    : 'D/C',
				('/B/', 'D/', '/B/C/')   : 'D/C',
				('/B', '/A/A', '/B/C/')  : '/A/A/C',
				('/B/', '/A/A', '/B/C/') : '/A/A/C',
				('/B', 'A/A', '/B/C/')   : 'A/A/C',
				('/B/', 'A/A/', '/B/C/') : 'A/A/C',
				('C', '/A/A/', 'B/C/D')  : 'B/A/A/D',
				('C', '/A/A', 'B/C/D')   : 'B/A/A/D',
				('D', '/A/A/', 'B/C/D')  : 'B/C/A/A',
				('D', '/A/A', 'B/C/D')   : 'B/C/A/A',
				('B/C', 'A', 'B/C/D')    : 'A/D',
				('B/C/', 'A', 'B/C/D')   : 'A/D',
				('B/C', 'A/', 'B/C/D')   : 'A/D',
				('B/C/', 'A/', 'B/C/D')  : 'A/D',
				('B/C/D', 'E', 'B/C/D')  : 'E',
				('B/C/D', 'E/', 'B/C/D') : 'E',
				('B/C/D', 'E/', 'B/C/D/'): 'E',
				('A', 'B', 'A/A/A')      : 'B/A/A',
				('A', 'B', 'B/A/A')      : 'B/B/A',

		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.replace(*inputs), inputs)

		test_inputs = [
				('/A', 'B', 'A'),
				('/A', 'B', 'A/A'),
		]

		for inputs in test_inputs:
			self.assertRaises(Exception, path.replace, input_s=inputs)

	def test_insert(self):
		test_data = {
				('A', 0, 'B/C')     : 'A/B/C',
				('B', 1, 'A/C')     : 'A/B/C',
				('C', 2, 'A/B')     : 'A/B/C',
				('A/', 0, '/B/C/')  : 'A/B/C',
				('B/', 1, 'A/C/')   : 'A/B/C',
				('C/', 2, 'A/B/')   : 'A/B/C',
				('/A/', 0, '/B/C/') : '/A/B/C',
				('/B/', 1, 'A/C/')  : 'A/B/C',
				('/C/', 2, 'A/B/')  : 'A/B/C',
				('A', -3, 'B/C')    : 'A/B/C',
				('A', -2, 'B/C')    : 'A/B/C',
				('B', -1, 'A/C')    : 'A/B/C',
				('A/', -3, '/B/C/') : 'A/B/C',
				('A/', -2, '/B/C/') : '/A/B/C',
				('B/', -1, 'A/C/')  : 'A/B/C',
				('/A/', -3, '/B/C/'): '/A/B/C',
				('/A/', -2, '/B/C/'): '/A/B/C',
				('/B/', -1, 'A/C/') : 'A/B/C',
				('A', 'B', 'B/C')   : 'A/B/C',
				('B', 'C', 'A/C')   : 'A/B/C',
				('B/C', 'D', 'A/D') : 'A/B/C/D',
				('A/B/C/', 'D', 'D'): 'A/B/C/D',
				('A', '/', '/B/C')  : 'A/B/C',
				('/A', '/', '/B/C') : '/A/B/C',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.insert(*inputs), inputs)

		test_inputs = [
				('A', '/B', 'B/C/')
		]

		for inputs in test_inputs:
			self.assertRaises(Exception, path.insert, input_s=inputs)

	def test_append(self):
		test_data = {
				('/B', 'A')  : 'A/B',
				('B', 'A')   : 'A/B',
				('B/', 'A')  : 'A/B',
				('B/', '/A') : '/A/B',
				('B/', '/A/'): '/A/B',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.append(*inputs), inputs)

	def test_remove(self):
		test_data = {
				('B', 'A/B')  : 'A',
				('B', 'A/B/') : 'A',
				('B/', 'A/B') : 'A',
				('B/', 'A/B/'): 'A',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.remove(*inputs), inputs)

	def test_pop(self):
		test_data = {
				('/A/B', 0) : '/',
				('/A/B', 1) : 'A',
				('/A/B', 2) : 'B',
				('/A/B/', 2): 'B',
				('A/B', 0)  : 'A',
				('A/B', 1)  : 'B',
				('A/B', 1)  : 'B',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.pop(*inputs), inputs)

	def test_ltrim(self):
		test_data = {
				('/A/B', 0) : '/A/B',
				('/A/B', 1) : 'A/B',
				('/A/B/', 1): 'A/B',
				('/A/B', 2) : 'B',
				('/A/B', 3) : '',
				('/A/B', 10): '',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.ltrim(*inputs), inputs)

		test_inputs = [
				('/A/B', -1)
		]

		for inputs in test_inputs:
			self.assertRaises(Exception, path.ltrim, input_s=inputs)

	def test_rtrim(self):
		test_data = {
				('/A/B', 0) : '/A/B',
				('/A/B', 1) : '/A',
				('/A/B/', 1): '/A',
				('/A/B', 2) : '/',
				('/A/B', 3) : '',
				('/A/B', 10): '',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.rtrim(*inputs), inputs)

		test_inputs = [
				('/A/B', -1)
		]

		for inputs in test_inputs:
			self.assertRaises(Exception, path.rtrim, input_s=inputs)

	def test_root(self):
		test_data = {
				''     : None,
				'/'    : '/',
				'/A'   : '/',
				'A/B'  : 'A',
				'/A/B' : '/',
				'/A/B/': '/',
				'A/B/' : 'A',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.root(input_), input_)

	def test_trail(self):
		test_data = {
				''       : None,
				'/'      : '/',
				'/A'     : '/',
				'A/B'    : 'A',
				'/A/B'   : '/A',
				'/A/B/'  : '/A',
				'A/B/'   : 'A',
				'/A/B/C' : '/A/B',
				'/A/B/C/': '/A/B',
				'A/B/C'  : 'A/B',
				'A/B/C/' : 'A/B',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.trail(input_), input_)

	def test_shared_trail(self):
		pass

	def test_base(self):
		test_data = {
				''          : None,
				'/'         : '/',
				'/A'        : 'A',
				'A/B'       : 'B',
				'/A/B'      : 'B',
				'/A/B/'     : 'B',
				'A/B/'      : 'B',
				'A/B/F.EXT/': 'F.EXT',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.base(input_), input_)

	def test_basename(self):
		test_data = {
				''        : None,
				'/'       : '/',
				'/A'      : 'A',
				'A/B'     : 'B',
				'/A/B'    : 'B',
				'/A/B/'   : 'B',
				'A/B/'    : 'B',
				'/F.EXT'  : 'F',
				'/F.EXT/' : 'F',
				'F.EXT/'  : 'F',
				'/A/F.EXT': 'F',
				'A/F.EXT' : 'F',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.basename(input_), input_)

	def test_ext(self):
		test_data = {
				''        : None,
				'/'       : None,
				'/A'      : None,
				'/A/'     : None,
				'A/'      : None,
				'/F.EXT'  : '.EXT',
				'/F.EXT/' : '.EXT',
				'F.EXT/'  : '.EXT',
				'/A/F.EXT': '.EXT',
				'A/F.EXT' : '.EXT',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.ext(input_), input_)

	def test_subpath(self):
		test_data = {
				('/A/B/C/', None, None): '/A/B/C',
				('/A/B/C/', 0, 0)      : '',
				('/A/B/C/', 0, None)   : '/A/B/C',
				('/A/B/C/', None, -1)  : '/A/B',
				('/A/B/C/', 0, 1)      : '/',
				('/A/B/C/', 0, 2)      : '/A',
				('/A/B/C/', 0, 3)      : '/A/B',
				('/A/B/C/', 0, 4)      : '/A/B/C',

				('A/B/C/', 0, None)    : 'A/B/C',
				('A/B/C/', None, -1)   : 'A/B',
				('A/B/C/', 0, 1)       : 'A',
				('A/B/C/', 0, 2)       : 'A/B',
				('A/B/C/', 0, 3)       : 'A/B/C',

				('/A/B/C/', '/', 'A')  : '/',
				('/A/B/C/', '/', 'B')  : '/A',
				('/A/B/C/', '/', 'C')  : '/A/B',
				('/A/B/C/', '/', None) : '/A/B/C',
				('/A/B/C/', None, '/') : '',
				('/A/B/C/', None, 'A') : '/',
				('/A/B/C/', None, 'B') : '/A',
				('/A/B/C/', None, 'C') : '/A/B',

				('A/B/C/', 'A', 'A')   : '',
				('A/B/C/', 'A', 'B')   : 'A',
				('A/B/C/', 'A', 'C')   : 'A/B',
				('A/B/C/', 'A', None)  : 'A/B/C',
				('A/B/C/', None, 'A')  : '',
				('A/B/C/', None, 'B')  : 'A',
				('A/B/C/', None, 'C')  : 'A/B',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.subpath(*inputs), inputs)

		# TODO: assert error messages
		test_inputs = [
				('/A/B/C/', 'A/B', None),
				('/A/B/C/', 'D', None)
		]

		for inputs in test_inputs:
			self.assertRaises(Exception, path.subpath, input_s=inputs)

	def test_shared_subpath(self):
		pass

	def test_depth(self):
		test_data = {
				''      : 0,
				'/'     : 1,
				'/A'    : 2,
				'/A/B'  : 3,
				'/A/B/C': 4,
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.depth(input_), input_)

	def test_index(self):
		test_data = {
				('/', '/A/B/C'): 0,
				('A', '/A/B/C'): 1,
				('B', '/A/B/C'): 2,
				('C', '/A/B/C'): 3,
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.index(*inputs), inputs)

		# TODO: assert error messages
		test_inputs = [
				('A/B', '/A/B/C'),
				('D', '/A/B/C/')
		]

		for inputs in test_inputs:
			self.assertRaises(Exception, path.index, input_s=inputs)

	def test_hide(self):
		test_data = {
				'/A/.F': '/A/.F',
				'F'    : '.F',
				'/A/F' : '/A/.F',
				'/A/F/': '/A/.F',
				'A/F/' : 'A/.F',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.hide(input_), input_)

		test_inputs = [
				('/'),
		]

		for inputs in test_inputs:
			self.assertRaises(Exception, path.hide, input_s=inputs)

	def test_reveal(self):
		test_data = {
				'.F'    : 'F',
				'/A/.F' : '/A/F',
				'/A/.F/': '/A/F',
				'A/.F/' : 'A/F',
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.reveal(input_), input_)

	def test_rename(self):
		test_data = {
				('A', 'B')        : 'B',
				('/A', 'B')       : '/B',
				('/A/', 'B')      : '/B',
				('A', 'A/B')      : 'B',
				('/A', '/A/B')    : '/B',
				('/A/', '/A/B/')  : '/B',
				('/A/', '/A/B')   : '/B',
				('A/C', 'B')      : 'A/B',
				('/A/C', 'B')     : '/A/B',
				('/A/C/', 'B')    : '/A/B',
				('A/C', 'A/B')    : 'A/B',
				('/A/C', '/A/B')  : '/A/B',
				('/A/C/', '/A/B/'): '/A/B',
				('/A/C/', 'A/B/') : '/A/B',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.rename(*inputs), inputs)

	def test_change_base(self):
		test_data = {
				('A', 'B')      : 'B',
				('/A', 'B')     : '/B',
				('/A', 'B/C')   : '/B/C',
				('/A', '/B/C')  : '/B/C',
				('/A', 'B/C/')  : '/B/C',
				('/A', '/B/C/') : '/B/C',
				('A/', 'B')     : 'B',
				('/A/', 'B')    : '/B',
				('/A/', 'B/C')  : '/B/C',
				('/A/', '/B/C') : '/B/C',
				('/A/', 'B/C/') : '/B/C',
				('/A/', '/B/C/'): '/B/C',

				('/A/B/D', 'C') : '/A/B/C',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.change_base(*inputs), inputs)

	def test_change_basename(self):
		test_data = {
				('A', 'B')              : 'B',
				('/A', 'B')             : '/B',
				('/A', 'B/C')           : '/B/C',
				('/A', '/B/C')          : '/B/C',
				('/A', 'B/C/')          : '/B/C',
				('/A', '/B/C/')         : '/B/C',
				('A/', 'B')             : 'B',
				('/A/', 'B')            : '/B',
				('/A/', 'B/C')          : '/B/C',
				('/A/', '/B/C')         : '/B/C',
				('/A/', 'B/C/')         : '/B/C',
				('/A/', '/B/C/')        : '/B/C',
				('/A/B/D', 'C')         : '/A/B/C',

				('C.EXT', 'C.EXT1')     : 'C.EXT1.EXT',
				('/A/B/C.EXT', 'C.EXT1'): '/A/B/C.EXT1.EXT',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.change_basename(*inputs), inputs)

	def test_change_ext(self):
		test_data = {
				('C.EXT', 'NEW_EXT')      : 'C.NEW_EXT',
				('/A/B/C.EXT', 'NEW_EXT') : '/A/B/C.NEW_EXT',

				('C.EXT', '.NEW_EXT')     : 'C.NEW_EXT',
				('/A/B/C.EXT', '.NEW_EXT'): '/A/B/C.NEW_EXT',

				('C', 'NEW_EXT')          : 'C.NEW_EXT',
				('/A/B/C', 'NEW_EXT')     : '/A/B/C.NEW_EXT',
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.change_ext(*inputs), inputs)

	def test_increment_base(self):
		test_data = {
				'/A'      : '/A 1',
				'/A 1'    : '/A 2',
				'A'       : 'A 1',
				'A 1'     : 'A 2',
				'A/B/C/'  : 'A/B/C 1',
				'A/B/C 1/': 'A/B/C 2'
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.increment_base(input_), input_)

	def test_deconstruct(self):
		test_data = {
				''        : (None, None, None),
				'/'       : ('/', '/', None),
				'/A'      : ('/', 'A', None),
				'/A/B'    : ('/A', 'B', None),
				'/A/B.EXT': ('/A', 'B', '.EXT'),
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.deconstruct(input_), input_)

	def test_is_legal(self):
		test_data = {
				'/A/B.ext'    : True,
				'/A.ext/B.ext': False,
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.is_legal(input_), input_)

	# TODO: add false assertion when is_legal() is fixed

	def test_is_absolute(self):
		test_data = {
				'/A': True,
				'A' : False,
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.is_absolute(input_), input_)

	def test_is_relative(self):
		test_data = {
				'/A': False,
				'A' : True,
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.is_relative(input_), input_)

	def test_is_in_path(self):
		test_data = {
				('/', '/B/C')    : True,
				('/', 'B/C/')    : False,
				('/', 'B/C')     : False,
				('/B', '/B/C')   : True,
				('/B', 'B/C')    : False,
				('B', '/B/C')    : True,
				('B', 'B/C')     : True,
				('B', 'BA/C')    : False,
				('/C', 'B/C')    : False,
				('C', 'B/C')     : True,
				('C/D', 'B/C/D') : True,
				('C/D', 'B/C/D/'): True,
				('B/D', 'B/C/D/'): False,
		}

		for inputs, expected_output in test_data.items():
			self.assertEqual(expected_output, path.is_in_path(*inputs), inputs)

	def test_is_subpath(self):
		test_data = {
				'/'      : True,
				'/A'     : True,
				'/A/B'   : True,
				'/A/B/C' : True,
				'/A/'    : True,
				'/A/B/'  : True,
				'/A/B/C/': True,
				''       : False,
				'A'      : False,
				'A/B'    : False,
				'A/B/C'  : False,
				'/A/C'   : False,
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.is_subpath(input_, '/A/B/C'), input_)

	def test_has_ext(self):
		test_data = {
				'A.EXT': True,
				'A'    : False,
		}

		for input_, expected_output in test_data.items():
			self.assertEqual(expected_output, path.has_ext(input_), input_)


if __name__ == '__main__':
	unittest.main()
