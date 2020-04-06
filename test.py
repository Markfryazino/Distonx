<<<<<<< HEAD
from stonks.test_files import paper_test_1, bonnie_test
from stonks.test_files.testing_paper import another_bonnie_test
from stonks.test_files.test_Emulator import test_emu
=======
# from stonks.test_files import paper_test_1, bonnie_test
# from stonks.test_files.test_Emulator import test_emu
>>>>>>> master
import warnings
from absl import logging
from stonks.web.server import StartServer

logging._warn_preinit_stderr = 0
logging.set_verbosity(logging.DEBUG)
warnings.filterwarnings('ignore')

# Файлик для тестов

#  paper_test_1(time=300.)
#  test_emu()
<<<<<<< HEAD
# bonnie_test(time=3600.)
another_bonnie_test()
# bonnie_test()
=======
#  bonnie_test(time=3600.)
StartServer()
>>>>>>> master
