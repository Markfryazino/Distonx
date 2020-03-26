from ..paper_testing.Emulator_v2 import EmulatorV2
from ..paper_testing import Agent, Environment
import logging
from .write_all_logger import WriteAllLogger


# ничего особенного, просто функция для тестирования эмулятора.
def test_emu():
    orderbook1 = {'btcusdt': {'bids': [[8535.56, 0.150682], [8535.53, 0.467708], [8535.08, 0.371598], [8535.02, 2.0], [8534.24, 0.5], [8534.23, 0.376502], [8534.21, 0.068841], [8534.19, 2.1], [8534.08, 0.031398], [8533.31, 0.070903], [8533.26, 0.035], [8533.04, 0.4], [8533.0, 0.204743], [8532.5, 0.245307], [8532.1, 0.184662], [8532.02, 0.138341], [8532.0, 0.006], [8531.88, 0.002], [8531.42, 0.6], [8531.4, 0.045]], 'asks': [[8535.69, 0.014694], [8535.71, 0.3], [8535.73, 0.002126], [8537.48, 0.516773], [8537.49, 0.182249], [8538.19, 0.074083], [8538.2, 0.2], [8538.22, 0.0013], [8538.33, 0.3], [8538.34, 0.175755], [8538.35, 0.936439], [8538.36, 0.2929], [8538.37, 2.1], [8538.51, 1.25], [8539.14, 0.234345], [8539.15, 0.2], [8539.16, 0.2], [8539.2, 0.013167], [8539.22, 2.82], [8539.71, 0.026548]]}, 'ethusdt': {'bids': [[218.22, 0.80332], [218.17, 11.45509], [218.16, 5.43254], [218.15, 13.75201], [218.14, 53.22405], [218.13, 16.4117], [218.12, 18.71205], [218.11, 9.18082], [218.1, 20.12999], [218.08, 9.26469], [218.07, 9.22062], [218.06, 15.79929], [218.05, 103.09222], [218.03, 21.26755], [218.02, 5.80019], [218.01, 15.82164], [218.0, 184.52262], [217.99, 60.20371], [217.98, 109.57283], [217.97, 0.88193]], 'asks': [[218.24, 1.82461], [218.25, 12.95251], [218.26, 1.82465], [218.27, 1.82465], [218.28, 32.24958], [218.29, 1.82465], [218.3, 30.42495], [218.31, 3.57252], [218.32, 17.73303], [218.33, 8.28408], [218.34, 35.20135], [218.35, 5.71588], [218.36, 31.47691], [218.37, 13.3779], [218.38, 44.33223], [218.39, 92.2], [218.4, 9.16359], [218.41, 93.0], [218.42, 27.34186], [218.43, 7.21]]}, 'bchusdt': {'bids': [[312.5, 4.09123], [312.49, 1.81581], [312.48, 1.33764], [312.47, 2.44721], [312.46, 0.53821], [312.45, 1.80702], [312.44, 4.18761], [312.43, 0.88955], [312.41, 7.78139], [312.39, 5.46074], [312.37, 6.99533], [312.36, 6.39894], [312.31, 20.0], [312.3, 5.06285], [312.29, 4.55213], [312.28, 0.96068], [312.27, 24.80061], [312.26, 6.47499], [312.25, 0.88955], [312.22, 9.64385]], 'asks': [[312.62, 2.53479], [312.63, 2.3], [312.65, 8.04789], [312.66, 5.0], [312.72, 12.25822], [312.74, 3.82], [312.75, 21.81088], [312.77, 8.60653], [312.78, 6.56805], [312.82, 2.5], [312.83, 0.042], [312.85, 2.22882], [312.86, 34.98], [312.87, 2.73052], [312.88, 0.6], [312.89, 4.30247], [312.93, 4.79355], [312.94, 2.73047], [312.95, 15.9934], [312.96, 8.24386]]}, 'bnbusdt': {'bids': [[18.8525, 44.83], [18.8524, 14.98], [18.8523, 7.88], [18.8507, 1.1], [18.85, 116.38], [18.8498, 1.77], [18.8481, 1.0], [18.8477, 0.58], [18.845, 1.0], [18.8443, 3.67], [18.8438, 4.0], [18.8437, 55.11], [18.8421, 1.47], [18.8409, 1.16], [18.8407, 7.7], [18.8401, 9.14], [18.84, 7.06], [18.8377, 0.58], [18.836, 22.78], [18.8359, 0.65]], 'asks': [[18.8698, 32.84], [18.87, 80.25], [18.8701, 2.04], [18.8704, 128.4], [18.8716, 203.38], [18.8724, 151.09], [18.8755, 82.24], [18.878, 12.0], [18.8781, 4.32], [18.8782, 159.08], [18.8783, 54.83], [18.8802, 721.0], [18.8852, 100.0], [18.8853, 53.46], [18.886, 1.01], [18.889, 974.0], [18.8895, 54.66], [18.8935, 158.78], [18.898, 100.0], [18.901, 65.0]]}, 'ltcusdt': {'bids': [[57.75, 64.66918], [57.74, 67.45216], [57.73, 143.27206], [57.72, 270.70438], [57.71, 117.99853], [57.7, 190.35927], [57.69, 212.81572], [57.68, 331.36615], [57.67, 57.98435], [57.66, 25.98752], [57.65, 443.69632], [57.64, 76.41166], [57.63, 38.01726], [57.62, 37.08115], [57.61, 50.4194], [57.6, 36.44416], [57.59, 207.69525], [57.58, 411.34745], [57.57, 45.10149], [57.56, 54.28961]], 'asks': [[57.78, 34.24], [57.79, 83.45751], [57.8, 99.57701], [57.81, 30.48237], [57.82, 78.48326], [57.83, 329.94962], [57.84, 192.20099], [57.85, 114.90306], [57.86, 642.71505], [57.87, 37.90103], [57.88, 199.89374], [57.89, 267.0], [57.91, 143.80925], [57.92, 47.85972], [57.93, 420.33896], [57.95, 41.9624], [57.96, 187.34353], [57.97, 7.88896], [57.98, 53.5702], [57.99, 8.75162]]}, 'ethbtc': {'bids': [[0.025565, 1.427], [0.025563, 0.56], [0.025562, 2.214], [0.025561, 39.0], [0.025559, 23.189], [0.025558, 6.939], [0.025557, 0.268], [0.025556, 7.234], [0.025555, 7.944], [0.025554, 9.303], [0.025553, 17.806], [0.025552, 4.367], [0.025551, 0.119], [0.02555, 8.071], [0.025549, 0.1], [0.025548, 0.191], [0.025547, 0.2], [0.025546, 1.847], [0.025545, 5.96], [0.025544, 5.072]], 'asks': [[0.025572, 8.0], [0.025575, 0.12], [0.025576, 14.785], [0.025577, 5.956], [0.025579, 13.656], [0.025581, 12.684], [0.025582, 7.821], [0.025583, 11.734], [0.025584, 7.822], [0.025585, 3.958], [0.025586, 4.082], [0.025587, 23.464], [0.025588, 167.1], [0.025591, 12.051], [0.025592, 15.059], [0.025598, 4.892], [0.025599, 83.7], [0.0256, 10.292], [0.025602, 9.159], [0.025604, 4.002]]}, 'bchbtc': {'bids': [[0.03663, 0.027], [0.036628, 3.17], [0.036609, 1.254], [0.036607, 0.025], [0.036606, 0.082], [0.036599, 0.369], [0.036598, 2.731], [0.036597, 10.42], [0.036595, 0.038], [0.036594, 6.399], [0.036593, 0.552], [0.03659, 0.778], [0.036589, 0.012], [0.036586, 0.08], [0.036584, 2.73], [0.036583, 0.552], [0.036582, 2.492], [0.036581, 0.126], [0.036576, 3.17], [0.036575, 7.198]], 'asks': [[0.036648, 9.737], [0.036649, 5.461], [0.03665, 5.454], [0.036651, 4.0], [0.036652, 5.46], [0.036653, 0.476], [0.036656, 2.768], [0.036658, 2.73], [0.03666, 9.344], [0.036661, 0.715], [0.036664, 4.0], [0.036665, 2.482], [0.036669, 29.5], [0.036674, 2.411], [0.036675, 2.606], [0.036677, 4.795], [0.03668, 1.047], [0.036683, 2.507], [0.036685, 6.232], [0.036686, 27.09]]}, 'bnbbtc': {'bids': [[0.0022096, 2.5], [0.0022095, 0.38], [0.0022093, 0.06], [0.0022092, 2.87], [0.0022091, 0.06], [0.002209, 0.41], [0.0022089, 0.5], [0.0022088, 1.87], [0.0022087, 2.04], [0.0022086, 2.64], [0.0022085, 45.5], [0.0022083, 2.16], [0.0022082, 0.62], [0.0022081, 0.3], [0.002208, 3.22], [0.0022079, 774.05], [0.0022078, 0.41], [0.0022076, 42.58], [0.0022075, 3.65], [0.0022074, 0.68]], 'asks': [[0.0022107, 16.0], [0.002211, 82.9], [0.0022112, 48.62], [0.0022118, 159.1], [0.0022122, 0.09], [0.0022123, 37.84], [0.0022124, 198.94], [0.0022125, 792.0], [0.0022131, 37.84], [0.0022133, 42.01], [0.0022134, 659.0], [0.0022137, 57.5], [0.0022138, 43.58], [0.0022142, 549.87], [0.0022143, 721.32], [0.0022148, 23.24], [0.002215, 26.75], [0.002216, 147.85], [0.0022165, 80.0], [0.0022166, 97.5]]}, 'ltcbtc': {'bids': [[0.006766, 30.0], [0.006765, 29.54], [0.006764, 59.78], [0.006763, 4.27], [0.006762, 3.0], [0.006761, 276.26], [0.00676, 45.4], [0.006759, 282.42], [0.006758, 26.54], [0.006757, 37.55], [0.006756, 33.41], [0.006755, 36.38], [0.006754, 378.65], [0.006753, 125.31], [0.006752, 50.53], [0.006751, 17.29], [0.00675, 61.13], [0.006749, 6.83], [0.006748, 0.02], [0.006747, 91.66]], 'asks': [[0.006769, 29.83], [0.006771, 32.46], [0.006773, 13.43], [0.006774, 55.51], [0.006775, 31.78], [0.006776, 219.64], [0.006777, 204.84], [0.006778, 29.54], [0.006779, 165.3], [0.00678, 171.04], [0.006781, 29.55], [0.006782, 167.34], [0.006784, 367.14], [0.006785, 37.15], [0.006786, 28.49], [0.006787, 27.21], [0.006788, 0.02], [0.006789, 3.81], [0.00679, 62.2], [0.006791, 78.16]]}, 'bchbnb': {'bids': [[16.532, 3.893], [16.531, 0.888], [16.508, 1.103], [16.504, 0.551], [16.496, 0.03], [16.481, 0.079], [16.476, 0.458], [16.474, 0.03], [16.472, 0.063], [16.467, 0.045], [16.461, 0.183], [16.46, 0.008], [16.446, 0.061], [16.428, 0.007], [16.42, 0.458], [16.409, 0.019], [16.407, 0.079], [16.401, 0.011], [16.39, 0.07], [16.372, 0.68]], 'asks': [[16.585, 0.321], [16.586, 0.12], [16.589, 0.488], [16.594, 0.552], [16.604, 0.035], [16.616, 20.0], [16.617, 0.03], [16.626, 0.12], [16.629, 0.079], [16.646, 0.458], [16.658, 0.12], [16.664, 0.12], [16.666, 0.19], [16.673, 0.12], [16.679, 0.06], [16.686, 0.023], [16.693, 0.31], [16.698, 0.122], [16.701, 0.853], [16.702, 0.458]]}, 'ltcbnb': {'bids': [[3.057, 14.771], [3.056, 14.051], [3.055, 61.932], [3.054, 8.0], [3.051, 5.8], [3.05, 5.977], [3.049, 2.983], [3.048, 7.091], [3.047, 0.32], [3.046, 0.168], [3.045, 0.162], [3.044, 0.247], [3.042, 13.267], [3.041, 0.039], [3.04, 0.291], [3.039, 0.065], [3.038, 16.209], [3.037, 2.0], [3.036, 23.107], [3.035, 52.055]], 'asks': [[3.064, 11.436], [3.065, 0.898], [3.066, 7.512], [3.067, 0.036], [3.068, 21.2], [3.069, 18.188], [3.07, 2.056], [3.071, 0.107], [3.072, 50.078], [3.073, 1.783], [3.074, 0.308], [3.075, 1.991], [3.076, 0.155], [3.077, 12.444], [3.078, 9.934], [3.079, 0.181], [3.08, 13.977], [3.081, 0.035], [3.082, 5.201], [3.083, 0.348]]}}
    orderbook2 = {'btcusdt': {'bids': [[8535.56, 0.150682], [8535.53, 0.467708], [8535.08, 0.371598], [8535.02, 2.0], [8534.24, 0.5], [8534.23, 0.376502], [8534.21, 0.068841], [8534.19, 2.1], [8534.08, 0.031398], [8533.31, 0.070903], [8533.26, 0.035], [8533.04, 0.4], [8533.0, 0.204743], [8532.5, 0.245307], [8532.1, 0.184662], [8532.02, 0.138341], [8532.0, 0.006], [8531.88, 0.002], [8531.42, 0.6], [8531.4, 0.045]], 'asks': [[8535.69, 0.014694], [8535.71, 0.3], [8535.73, 0.002126], [8537.48, 0.516773], [8537.49, 0.182249], [8538.19, 0.074083], [8538.2, 0.2], [8538.22, 0.0013], [8538.33, 0.3], [8538.34, 0.175755], [8538.35, 0.936439], [8538.36, 0.2929], [8538.37, 2.1], [8538.51, 1.25], [8539.14, 0.234345], [8539.15, 0.2], [8539.16, 0.2], [8539.2, 0.013167], [8539.22, 2.82], [8539.71, 0.026548]]}, 'ethusdt': {'bids': [[218.22, 0.80332], [218.17, 11.45509], [218.16, 5.43254], [218.15, 13.75201], [218.14, 53.22405], [218.13, 16.4117], [218.12, 18.71205], [218.11, 9.18082], [218.1, 20.12999], [218.08, 9.26469], [218.07, 9.22062], [218.06, 15.79929], [218.05, 103.09222], [218.03, 21.26755], [218.02, 5.80019], [218.01, 15.82164], [218.0, 184.52262], [217.99, 60.20371], [217.98, 109.57283], [217.97, 0.88193]], 'asks': [[218.24, 1.82461], [218.25, 12.95251], [218.26, 1.82465], [218.27, 1.82465], [218.28, 32.24958], [218.29, 1.82465], [218.3, 30.42495], [218.31, 3.57252], [218.32, 17.73303], [218.33, 8.28408], [218.34, 35.20135], [218.35, 5.71588], [218.36, 31.47691], [218.37, 13.3779], [218.38, 44.33223], [218.39, 92.2], [218.4, 9.16359], [218.41, 93.0], [218.42, 27.34186], [218.43, 7.21]]}, 'bchusdt': {'bids': [[312.5, 4.09123], [312.49, 1.81581], [312.48, 1.33764], [312.47, 2.44721], [312.46, 0.53821], [312.45, 1.80702], [312.44, 4.18761], [312.43, 0.88955], [312.41, 7.78139], [312.39, 5.46074], [312.37, 6.99533], [312.36, 6.39894], [312.31, 20.0], [312.3, 5.06285], [312.29, 4.55213], [312.28, 0.96068], [312.27, 24.80061], [312.26, 6.47499], [312.25, 0.88955], [312.22, 9.64385]], 'asks': [[312.62, 2.53479], [312.63, 2.3], [312.65, 8.04789], [312.66, 5.0], [312.72, 12.25822], [312.74, 3.82], [312.75, 21.81088], [312.77, 8.60653], [312.78, 6.56805], [312.82, 2.5], [312.83, 0.042], [312.85, 2.22882], [312.86, 34.98], [312.87, 2.73052], [312.88, 0.6], [312.89, 4.30247], [312.93, 4.79355], [312.94, 2.73047], [312.95, 15.9934], [312.96, 8.24386]]}, 'bnbusdt': {'bids': [[18.8525, 44.83], [18.8524, 14.98], [18.8523, 7.88], [18.8507, 1.1], [18.85, 116.38], [18.8498, 1.77], [18.8481, 1.0], [18.8477, 0.58], [18.845, 1.0], [18.8443, 3.67], [18.8438, 4.0], [18.8437, 55.11], [18.8421, 1.47], [18.8409, 1.16], [18.8407, 7.7], [18.8401, 9.14], [18.84, 7.06], [18.8377, 0.58], [18.836, 22.78], [18.8359, 0.65]], 'asks': [[18.8698, 32.84], [18.87, 80.25], [18.8701, 2.04], [18.8704, 128.4], [18.8716, 203.38], [18.8724, 151.09], [18.8755, 82.24], [18.878, 12.0], [18.8781, 4.32], [18.8782, 159.08], [18.8783, 54.83], [18.8802, 721.0], [18.8852, 100.0], [18.8853, 53.46], [18.886, 1.01], [18.889, 974.0], [18.8895, 54.66], [18.8935, 158.78], [18.898, 100.0], [18.901, 65.0]]}, 'ltcusdt': {'bids': [[57.75, 64.66918], [57.74, 67.45216], [57.73, 143.27206], [57.72, 270.70438], [57.71, 117.99853], [57.7, 190.35927], [57.69, 212.81572], [57.68, 331.36615], [57.67, 57.98435], [57.66, 25.98752], [57.65, 443.69632], [57.64, 76.41166], [57.63, 38.01726], [57.62, 37.08115], [57.61, 50.4194], [57.6, 36.44416], [57.59, 207.69525], [57.58, 411.34745], [57.57, 45.10149], [57.56, 54.28961]], 'asks': [[57.78, 34.24], [57.79, 83.45751], [57.8, 99.57701], [57.81, 30.48237], [57.82, 78.48326], [57.83, 329.94962], [57.84, 192.20099], [57.85, 114.90306], [57.86, 642.71505], [57.87, 37.90103], [57.88, 199.89374], [57.89, 267.0], [57.91, 143.80925], [57.92, 47.85972], [57.93, 420.33896], [57.95, 41.9624], [57.96, 187.34353], [57.97, 7.88896], [57.98, 53.5702], [57.99, 8.75162]]}, 'ethbtc': {'bids': [[0.025565, 1.427], [0.025563, 0.56], [0.025562, 2.214], [0.025561, 39.0], [0.025559, 23.189], [0.025558, 6.939], [0.025557, 0.268], [0.025556, 7.234], [0.025555, 7.944], [0.025554, 9.303], [0.025553, 17.806], [0.025552, 4.367], [0.025551, 0.119], [0.02555, 8.071], [0.025549, 0.1], [0.025548, 0.191], [0.025547, 0.2], [0.025546, 1.847], [0.025545, 5.96], [0.025544, 5.072]], 'asks': [[0.025572, 8.0], [0.025575, 0.12], [0.025576, 14.785], [0.025577, 5.956], [0.025579, 13.656], [0.025581, 12.684], [0.025582, 7.821], [0.025583, 11.734], [0.025584, 7.822], [0.025585, 3.958], [0.025586, 4.082], [0.025587, 23.464], [0.025588, 167.1], [0.025591, 12.051], [0.025592, 15.059], [0.025598, 4.892], [0.025599, 83.7], [0.0256, 10.292], [0.025602, 9.159], [0.025604, 4.002]]}, 'bchbtc': {'bids': [[0.03663, 0.027], [0.036628, 3.17], [0.036609, 1.254], [0.036607, 0.025], [0.036606, 0.082], [0.036599, 0.369], [0.036598, 2.731], [0.036597, 10.42], [0.036595, 0.038], [0.036594, 6.399], [0.036593, 0.552], [0.03659, 0.778], [0.036589, 0.012], [0.036586, 0.08], [0.036584, 2.73], [0.036583, 0.552], [0.036582, 2.492], [0.036581, 0.126], [0.036576, 3.17], [0.036575, 7.198]], 'asks': [[0.036648, 9.737], [0.036649, 5.461], [0.03665, 5.454], [0.036651, 4.0], [0.036652, 5.46], [0.036653, 0.476], [0.036656, 2.768], [0.036658, 2.73], [0.03666, 9.344], [0.036661, 0.715], [0.036664, 4.0], [0.036665, 2.482], [0.036669, 29.5], [0.036674, 2.411], [0.036675, 2.606], [0.036677, 4.795], [0.03668, 1.047], [0.036683, 2.507], [0.036685, 6.232], [0.036686, 27.09]]}, 'bnbbtc': {'bids': [[0.0022096, 2.5], [0.0022095, 0.38], [0.0022093, 0.06], [0.0022092, 2.87], [0.0022091, 0.06], [0.002209, 0.41], [0.0022089, 0.5], [0.0022088, 1.87], [0.0022087, 2.04], [0.0022086, 2.64], [0.0022085, 45.5], [0.0022083, 2.16], [0.0022082, 0.62], [0.0022081, 0.3], [0.002208, 3.22], [0.0022079, 774.05], [0.0022078, 0.41], [0.0022076, 42.58], [0.0022075, 3.65], [0.0022074, 0.68]], 'asks': [[0.0022107, 16.0], [0.002211, 82.9], [0.0022112, 48.62], [0.0022118, 159.1], [0.0022122, 0.09], [0.0022123, 37.84], [0.0022124, 198.94], [0.0022125, 792.0], [0.0022131, 37.84], [0.0022133, 42.01], [0.0022134, 659.0], [0.0022137, 57.5], [0.0022138, 43.58], [0.0022142, 549.87], [0.0022143, 721.32], [0.0022148, 23.24], [0.002215, 26.75], [0.002216, 147.85], [0.0022165, 80.0], [0.0022166, 97.5]]}, 'ltcbtc': {'bids': [[0.006766, 30.0], [0.006765, 29.54], [0.006764, 59.78], [0.006763, 4.27], [0.006762, 3.0], [0.006761, 276.26], [0.00676, 45.4], [0.006759, 282.42], [0.006758, 26.54], [0.006757, 37.55], [0.006756, 33.41], [0.006755, 36.38], [0.006754, 378.65], [0.006753, 125.31], [0.006752, 50.53], [0.006751, 17.29], [0.00675, 61.13], [0.006749, 6.83], [0.006748, 0.02], [0.006747, 91.66]], 'asks': [[0.006769, 29.83], [0.006771, 32.46], [0.006773, 13.43], [0.006774, 55.51], [0.006775, 31.78], [0.006776, 219.64], [0.006777, 204.84], [0.006778, 29.54], [0.006779, 165.3], [0.00678, 171.04], [0.006781, 29.55], [0.006782, 167.34], [0.006784, 367.14], [0.006785, 37.15], [0.006786, 28.49], [0.006787, 27.21], [0.006788, 0.02], [0.006789, 3.81], [0.00679, 62.2], [0.006791, 78.16]]}, 'bchbnb': {'bids': [[16.532, 3.893], [16.531, 0.888], [16.508, 1.103], [16.504, 0.551], [16.496, 0.03], [16.481, 0.079], [16.476, 0.458], [16.474, 0.03], [16.472, 0.063], [16.467, 0.045], [16.461, 0.183], [16.46, 0.008], [16.446, 0.061], [16.428, 0.007], [16.42, 0.458], [16.409, 0.019], [16.407, 0.079], [16.401, 0.011], [16.39, 0.07], [16.372, 0.68]], 'asks': [[16.585, 0.321], [16.586, 0.12], [16.589, 0.488], [16.594, 0.552], [16.604, 0.035], [16.616, 20.0], [16.617, 0.03], [16.626, 0.12], [16.629, 0.079], [16.646, 0.458], [16.658, 0.12], [16.664, 0.12], [16.666, 0.19], [16.673, 0.12], [16.679, 0.06], [16.686, 0.023], [16.693, 0.31], [16.698, 0.122], [16.701, 0.853], [16.702, 0.458]]}, 'ltcbnb': {'bids': [[3.057, 14.771], [3.056, 14.051], [3.055, 61.932], [3.054, 8.0], [3.051, 5.8], [3.05, 5.977], [3.049, 2.983], [3.048, 7.091], [3.047, 0.32], [3.046, 0.168], [3.045, 0.162], [3.044, 0.247], [3.042, 13.267], [3.041, 0.039], [3.04, 0.291], [3.039, 0.065], [3.038, 16.209], [3.037, 2.0], [3.036, 23.107], [3.035, 52.055]], 'asks': [[3.064, 11.436], [3.065, 0.898], [3.066, 7.512], [3.067, 0.036], [3.068, 21.2], [3.069, 18.188], [3.07, 2.056], [3.071, 0.107], [3.072, 50.078], [3.073, 1.783], [3.074, 0.308], [3.075, 1.991], [3.076, 0.155], [3.077, 12.444], [3.078, 9.934], [3.079, 0.181], [3.08, 13.977], [3.081, 0.035], [3.082, 5.201], [3.083, 0.348]]}}
    orderbook3 = {'btcusdt': {'bids': [[8535.56, 0.150682], [8535.53, 0.467708], [8535.08, 0.371598], [8535.02, 2.0], [8534.24, 0.5], [8534.23, 0.376502], [8534.21, 0.068841], [8534.19, 2.1], [8534.08, 0.031398], [8533.31, 0.070903], [8533.26, 0.035], [8533.04, 0.4], [8533.0, 0.204743], [8532.5, 0.245307], [8532.1, 0.184662], [8532.02, 0.138341], [8532.0, 0.006], [8531.88, 0.002], [8531.42, 0.6], [8531.4, 0.045]], 'asks': [[8535.69, 0.014694], [8535.71, 0.3], [8535.73, 0.002126], [8537.48, 0.516773], [8537.49, 0.182249], [8538.19, 0.074083], [8538.2, 0.2], [8538.22, 0.0013], [8538.33, 0.3], [8538.34, 0.175755], [8538.35, 0.936439], [8538.36, 0.2929], [8538.37, 2.1], [8538.51, 1.25], [8539.14, 0.234345], [8539.15, 0.2], [8539.16, 0.2], [8539.2, 0.013167], [8539.22, 2.82], [8539.71, 0.026548]]}, 'ethusdt': {'bids': [[218.22, 0.80332], [218.17, 11.45509], [218.16, 5.43254], [218.15, 13.75201], [218.14, 53.22405], [218.13, 16.4117], [218.12, 18.71205], [218.11, 9.18082], [218.1, 20.12999], [218.08, 9.26469], [218.07, 9.22062], [218.06, 15.79929], [218.05, 103.09222], [218.03, 21.26755], [218.02, 5.80019], [218.01, 15.82164], [218.0, 184.52262], [217.99, 60.20371], [217.98, 109.57283], [217.97, 0.88193]], 'asks': [[218.24, 1.82461], [218.25, 12.95251], [218.26, 1.82465], [218.27, 1.82465], [218.28, 32.24958], [218.29, 1.82465], [218.3, 30.42495], [218.31, 3.57252], [218.32, 17.73303], [218.33, 8.28408], [218.34, 35.20135], [218.35, 5.71588], [218.36, 31.47691], [218.37, 13.3779], [218.38, 44.33223], [218.39, 92.2], [218.4, 9.16359], [218.41, 93.0], [218.42, 27.34186], [218.43, 7.21]]}, 'bchusdt': {'bids': [[312.5, 4.09123], [312.49, 1.81581], [312.48, 1.33764], [312.47, 2.44721], [312.46, 0.53821], [312.45, 1.80702], [312.44, 4.18761], [312.43, 0.88955], [312.41, 7.78139], [312.39, 5.46074], [312.37, 6.99533], [312.36, 6.39894], [312.31, 20.0], [312.3, 5.06285], [312.29, 4.55213], [312.28, 0.96068], [312.27, 24.80061], [312.26, 6.47499], [312.25, 0.88955], [312.22, 9.64385]], 'asks': [[312.62, 2.53479], [312.63, 2.3], [312.65, 8.04789], [312.66, 5.0], [312.72, 12.25822], [312.74, 3.82], [312.75, 21.81088], [312.77, 8.60653], [312.78, 6.56805], [312.82, 2.5], [312.83, 0.042], [312.85, 2.22882], [312.86, 34.98], [312.87, 2.73052], [312.88, 0.6], [312.89, 4.30247], [312.93, 4.79355], [312.94, 2.73047], [312.95, 15.9934], [312.96, 8.24386]]}, 'bnbusdt': {'bids': [[18.8525, 44.83], [18.8524, 14.98], [18.8523, 7.88], [18.8507, 1.1], [18.85, 116.38], [18.8498, 1.77], [18.8481, 1.0], [18.8477, 0.58], [18.845, 1.0], [18.8443, 3.67], [18.8438, 4.0], [18.8437, 55.11], [18.8421, 1.47], [18.8409, 1.16], [18.8407, 7.7], [18.8401, 9.14], [18.84, 7.06], [18.8377, 0.58], [18.836, 22.78], [18.8359, 0.65]], 'asks': [[18.8698, 32.84], [18.87, 80.25], [18.8701, 2.04], [18.8704, 128.4], [18.8716, 203.38], [18.8724, 151.09], [18.8755, 82.24], [18.878, 12.0], [18.8781, 4.32], [18.8782, 159.08], [18.8783, 54.83], [18.8802, 721.0], [18.8852, 100.0], [18.8853, 53.46], [18.886, 1.01], [18.889, 974.0], [18.8895, 54.66], [18.8935, 158.78], [18.898, 100.0], [18.901, 65.0]]}, 'ltcusdt': {'bids': [[57.75, 64.66918], [57.74, 67.45216], [57.73, 143.27206], [57.72, 270.70438], [57.71, 117.99853], [57.7, 190.35927], [57.69, 212.81572], [57.68, 331.36615], [57.67, 57.98435], [57.66, 25.98752], [57.65, 443.69632], [57.64, 76.41166], [57.63, 38.01726], [57.62, 37.08115], [57.61, 50.4194], [57.6, 36.44416], [57.59, 207.69525], [57.58, 411.34745], [57.57, 45.10149], [57.56, 54.28961]], 'asks': [[57.78, 34.24], [57.79, 83.45751], [57.8, 99.57701], [57.81, 30.48237], [57.82, 78.48326], [57.83, 329.94962], [57.84, 192.20099], [57.85, 114.90306], [57.86, 642.71505], [57.87, 37.90103], [57.88, 199.89374], [57.89, 267.0], [57.91, 143.80925], [57.92, 47.85972], [57.93, 420.33896], [57.95, 41.9624], [57.96, 187.34353], [57.97, 7.88896], [57.98, 53.5702], [57.99, 8.75162]]}, 'ethbtc': {'bids': [[0.025565, 1.427], [0.025563, 0.56], [0.025562, 2.214], [0.025561, 39.0], [0.025559, 23.189], [0.025558, 6.939], [0.025557, 0.268], [0.025556, 7.234], [0.025555, 7.944], [0.025554, 9.303], [0.025553, 17.806], [0.025552, 4.367], [0.025551, 0.119], [0.02555, 8.071], [0.025549, 0.1], [0.025548, 0.191], [0.025547, 0.2], [0.025546, 1.847], [0.025545, 5.96], [0.025544, 5.072]], 'asks': [[0.025572, 8.0], [0.025575, 0.12], [0.025576, 14.785], [0.025577, 5.956], [0.025579, 13.656], [0.025581, 12.684], [0.025582, 7.821], [0.025583, 11.734], [0.025584, 7.822], [0.025585, 3.958], [0.025586, 4.082], [0.025587, 23.464], [0.025588, 167.1], [0.025591, 12.051], [0.025592, 15.059], [0.025598, 4.892], [0.025599, 83.7], [0.0256, 10.292], [0.025602, 9.159], [0.025604, 4.002]]}, 'bchbtc': {'bids': [[0.03663, 0.027], [0.036628, 3.17], [0.036609, 1.254], [0.036607, 0.025], [0.036606, 0.082], [0.036599, 0.369], [0.036598, 2.731], [0.036597, 10.42], [0.036595, 0.038], [0.036594, 6.399], [0.036593, 0.552], [0.03659, 0.778], [0.036589, 0.012], [0.036586, 0.08], [0.036584, 2.73], [0.036583, 0.552], [0.036582, 2.492], [0.036581, 0.126], [0.036576, 3.17], [0.036575, 7.198]], 'asks': [[0.036648, 9.737], [0.036649, 5.461], [0.03665, 5.454], [0.036651, 4.0], [0.036652, 5.46], [0.036653, 0.476], [0.036656, 2.768], [0.036658, 2.73], [0.03666, 9.344], [0.036661, 0.715], [0.036664, 4.0], [0.036665, 2.482], [0.036669, 29.5], [0.036674, 2.411], [0.036675, 2.606], [0.036677, 4.795], [0.03668, 1.047], [0.036683, 2.507], [0.036685, 6.232], [0.036686, 27.09]]}, 'bnbbtc': {'bids': [[0.0022096, 2.5], [0.0022095, 0.38], [0.0022093, 0.06], [0.0022092, 2.87], [0.0022091, 0.06], [0.002209, 0.41], [0.0022089, 0.5], [0.0022088, 1.87], [0.0022087, 2.04], [0.0022086, 2.64], [0.0022085, 45.5], [0.0022083, 2.16], [0.0022082, 0.62], [0.0022081, 0.3], [0.002208, 3.22], [0.0022079, 774.05], [0.0022078, 0.41], [0.0022076, 42.58], [0.0022075, 3.65], [0.0022074, 0.68]], 'asks': [[0.0022107, 16.0], [0.002211, 82.9], [0.0022112, 48.62], [0.0022118, 159.1], [0.0022122, 0.09], [0.0022123, 37.84], [0.0022124, 198.94], [0.0022125, 792.0], [0.0022131, 37.84], [0.0022133, 42.01], [0.0022134, 659.0], [0.0022137, 57.5], [0.0022138, 43.58], [0.0022142, 549.87], [0.0022143, 721.32], [0.0022148, 23.24], [0.002215, 26.75], [0.002216, 147.85], [0.0022165, 80.0], [0.0022166, 97.5]]}, 'ltcbtc': {'bids': [[0.006766, 30.0], [0.006765, 29.54], [0.006764, 59.78], [0.006763, 4.27], [0.006762, 3.0], [0.006761, 276.26], [0.00676, 45.4], [0.006759, 282.42], [0.006758, 26.54], [0.006757, 37.55], [0.006756, 33.41], [0.006755, 36.38], [0.006754, 378.65], [0.006753, 125.31], [0.006752, 50.53], [0.006751, 17.29], [0.00675, 61.13], [0.006749, 6.83], [0.006748, 0.02], [0.006747, 91.66]], 'asks': [[0.006769, 29.83], [0.006771, 32.46], [0.006773, 13.43], [0.006774, 55.51], [0.006775, 31.78], [0.006776, 219.64], [0.006777, 204.84], [0.006778, 29.54], [0.006779, 165.3], [0.00678, 171.04], [0.006781, 29.55], [0.006782, 167.34], [0.006784, 367.14], [0.006785, 37.15], [0.006786, 28.49], [0.006787, 27.21], [0.006788, 0.02], [0.006789, 3.81], [0.00679, 62.2], [0.006791, 78.16]]}, 'bchbnb': {'bids': [[16.532, 3.893], [16.531, 0.888], [16.508, 1.103], [16.504, 0.551], [16.496, 0.03], [16.481, 0.079], [16.476, 0.458], [16.474, 0.03], [16.472, 0.063], [16.467, 0.045], [16.461, 0.183], [16.46, 0.008], [16.446, 0.061], [16.428, 0.007], [16.42, 0.458], [16.409, 0.019], [16.407, 0.079], [16.401, 0.011], [16.39, 0.07], [16.372, 0.68]], 'asks': [[16.585, 0.321], [16.586, 0.12], [16.589, 0.488], [16.594, 0.552], [16.604, 0.035], [16.616, 20.0], [16.617, 0.03], [16.626, 0.12], [16.629, 0.079], [16.646, 0.458], [16.658, 0.12], [16.664, 0.12], [16.666, 0.19], [16.673, 0.12], [16.679, 0.06], [16.686, 0.023], [16.693, 0.31], [16.698, 0.122], [16.701, 0.853], [16.702, 0.458]]}, 'ltcbnb': {'bids': [[3.057, 14.771], [3.056, 14.051], [3.055, 61.932], [3.054, 8.0], [3.051, 5.8], [3.05, 5.977], [3.049, 2.983], [3.048, 7.091], [3.047, 0.32], [3.046, 0.168], [3.045, 0.162], [3.044, 0.247], [3.042, 13.267], [3.041, 0.039], [3.04, 0.291], [3.039, 0.065], [3.038, 16.209], [3.037, 2.0], [3.036, 23.107], [3.035, 52.055]], 'asks': [[3.064, 11.436], [3.065, 0.898], [3.066, 7.512], [3.067, 0.036], [3.068, 21.2], [3.069, 18.188], [3.07, 2.056], [3.071, 0.107], [3.072, 50.078], [3.073, 1.783], [3.074, 0.308], [3.075, 1.991], [3.076, 0.155], [3.077, 12.444], [3.078, 9.934], [3.079, 0.181], [3.08, 13.977], [3.081, 0.035], [3.082, 5.201], [3.083, 0.348]]}}
    test_orderbook = {'btcusdt': {'bids': [[10000., 10]], 'asks': [[10000., 10]]}}

    open("trash/Ariana_output.txt", "w").close()
    with open('settings/cryptos.txt') as file:
        cryptos = [a[:-1] for a in file.readlines()]

    balance = {asset: 0. for asset in cryptos}
    balance['usdt'] = 0.
    balance['btc'] = 3.
    balance['ltc'] = 0
    query = {'btcusdt': ('sell base', 0.5)}
    emulator = EmulatorV2()
    # emulator.fee = 0.
    response = emulator.handle(query, balance, orderbook1)
    print(response)
