from stonks.test_files import paper_test_1, bonnie_test
from stonks.test_files.test_Emulator import test_emu
import warnings
warnings.filterwarnings('ignore')

# Файлик для тестов

#  paper_test_1(time=300.)
#  test_emu()
bonnie_test(time=3600.)
