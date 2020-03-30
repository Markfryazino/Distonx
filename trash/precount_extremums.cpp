#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

template<typename T>
bool cmp(bool is_max, T a, T b) {
    if (is_max) {
        return a > b;
    }
    return b > a;
}

void makeSparse(
        std::vector<double>& prices,
        std::vector<std::vector<double>>& ST_min,
        std::vector<std::vector<double>>& ST_max,
        int n, int log_len) {
    for (unsigned j = 0; j <= log_len; ++j) {
        for (int i = 0; i + (1u << j) <= n; ++i) {
            ST_max[i][j] =
                    (j == 0 ? prices[i] : std::max(ST_max[i][j - 1],
                                                   ST_max[i + (1u << (j - 1))][j - 1]));
            ST_min[i][j] =
                    (j == 0 ? prices[i] : std::min(ST_min[i][j - 1],
                                                   ST_min[i + (1u << (j - 1))][j - 1]));
        }
    }

}

void countLog(std::vector<int>& log, int n) {
    log[1] = 0;
    for (int i = 2; i <= n; ++i) {
        log[i] = log[i / 2] + 1;
    }
}


double query(
        std::vector<std::vector<double>>& ST,
        std::vector<int>& log,
        int l, int r,
        bool is_max) {
    unsigned j = log[r - l + 1];
    if (is_max) {
        return std::max(ST[l][j], ST[r - (1u << j) + 1][j]);
    }
    return std::min(ST[l][j], ST[r - (1u << j) + 1][j]);
}


int search(
        std::vector<std::vector<double>>& ST,
        std::vector<int>& log,
        int pos, int n, double border,
        bool is_max) {
    int left = pos, right = n;
    while (right - left > 1) {
        int mid = (left + right) / 2;
        double cur_query = query(ST, log, pos, mid, is_max);
        if (cmp(is_max, cur_query, border)) {
            right = mid;
        } else {
            left = mid;
        }
    }
    left = std::max(left - 1, pos);
    while (left < n &&
    !cmp(is_max, query(ST, log, pos, left, is_max), border)) {
        ++left;
    }
    return left;
}


void make_res(
        std::vector<std::vector<double>>& ST_min,
        std::vector<std::vector<double>>& ST_max,
        std::vector<double>& prices,
        std::vector<int>& log,
        std::vector<int>& result,
        int n, double mod) {
    for (int i = 0; i < n; ++i) {
        int pos_of_min = search(ST_min, log, i, n,
                prices[i] * (1 - mod), false),
                pos_of_max = search(ST_max, log, i, n,
                        prices[i] * (1 + mod), true);
        if (pos_of_min < pos_of_max) {
            result[i] = 0;
        } else if (pos_of_min > pos_of_max) {
            result[i] = 1;
        } else {
            result[i] = -1;
        }
    }
}

void make_slow_res(
        std::vector<double>& prices,
        std::vector<int>& result,
        int n, double mod
        ) {
    for (int i = 0; i < n; ++i) {
        bool could_find = false;
        for (int j = i + 1; j < n; ++j) {
            if (prices[j] <= prices[i] * (1 - mod)) {
                could_find = true;
                result[i] = 0;
                break;
            } else if (prices[j] >= prices[i] * (1 + mod)) {
                could_find = true;
                result[i] = 1;
                break;
            }
        }
        if (!could_find) {
            result[i] = -1;
        }
    }
}


int main() {
    std::ifstream in;
    in.open("input.txt");
    std::vector<double> prices;
    int n;
    double mod;
    in >> n >> mod;
    prices.resize(n);
    for (int i = 0; i < n; ++i) {
        in >> prices[i];
    }
    in.close();

    int log_len = ceil(log2(n) + 1.0);
    std::vector<std::vector<double>>
            ST_min(n, std::vector<double> (log_len)),
            ST_max(n, std::vector<double> (log_len));
    std::vector<int> log(n + 1);
    makeSparse(prices, ST_min, ST_max, n, log_len);
    countLog(log, n);

    std::vector<int> result(n), slow(n);
    make_res(ST_min, ST_max, prices, log, result, n, mod);

    std::ofstream out;
    out.open("output.txt");
    out << "[";
    int cnt = 0;
    for (auto el : result) {
        ++cnt;
        out << el << (cnt == n ? "]" : ", ");
    }
    out.close();

    return 0;
}