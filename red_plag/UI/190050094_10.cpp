#include <bits/stdc++.h>
using namespace std;

int binaryToDecimal (int *a, int &n) {
    int lamb = 0;
    for (int i = 0; i < sizeof(a); i++) {
        if (a[i] == 1) {
            lamb += pow(2, (n - i - 1));
        }
    }
    return lamb;
}

int num_ones(string &s) {
    int count = 0;
    for (int i = 0; i < s.length(); ++i)
    {
        if (s[i] == '1') {
            count++;
        }
    }
    return count;
}

int printKthBit (int &n, int &k) {
    return((n & (1 << (k))) >> (k));
}

bool is_equi (string &s1, string &s2, int &n) {
    if (s1 == s2) return true;
    int permu[n], compa[n];
    string ran = s1;
    for (int i = 0; i < n; i++) {
        permu[i] = i;
        compa[i] = i;
    }
    next_permutation(permu, permu + n);
    do {
        for (int i = 0; i < pow(2, n); i++) {
            for (int j = 0; j < n; j++) {
                compa[n - 1 - permu[j]] = printKthBit(i, j);
            }
            ran[binaryToDecimal(compa, n)] = s1[i];
        }
        if (ran == s2) return true;
    } while (next_permutation(permu, permu + n));
    return false;
}


int main(){
    int n, m;
    cin >> n >> m;
    string vals[m];
    for (int i = 0; i < m; i++) {
        cin >> vals[i];
    }
    map<int, vector<string>> groups;
    for(int i = 0; i < m; i++){
        int count = num_ones(vals[i]);
        groups[count].push_back(vals[i]);
    }
    int result = 0;
    for (auto i = groups.begin(); i != groups.end(); i++) {
        vector<string> here = i->second;
        if (here.size() == 1) {
            result++;
            continue;
        }
        if (here.size() > 1) {
            int count = 1;
            for (int m = 0; m < here.size(); m++) {
                for (int j = m - 1; j >= 0; j--) {
                    if (is_equi(here[m], here[j], n)) {
                        break;
                    }
                    if (j == 0) {
                        count++;
                    }
                }
            }
            result += count;
        }
    }
    cout << result << endl;
}
