#include<bits/stdc++.h>
using namespace std;

vector<int*>permutation_vector;
int n,m;

void hulk(int *nlen, int* arr, int n){
	if (n<0)return;
	int sz = 1<<n;
        int t=1<<nlen[n];
	for (int i=2*sz-1; i>=sz;  i--){
            arr[i]-=sz-t;
        }
	hulk(nlen, arr, n-1);
        hulk(nlen, arr+sz, n-1);
}

bool equivalent(string s1, string s2){
        int sz=1<<n;
        int identity=0;

	while(identity<permutation_vector.size()) {
           bool flag=1;
           for (int i=0; i<sz; i++){
		if(s1[i]!=s2[permutation_vector[identity][i]]){flag=0; break;}
           }
           if(flag)return true;
	   identity++;
  	}
        return false;

}
string generat(string &k,vector<int> &p)
{
	string l="";
	l.resize(1<<n);
	//cout << k << endl;
	for(int i=0;i<(1<<n);i++)
	{
		int index=0;
		for(int j=0;j<n;j++)
		{
			index=index+(bool)(i&(1<<j))*(1<<p[j]);
		}
		l[index]=k[i];
	}
	return l;
}

int main(){
	string s;
	cin >> n;
	cin >> m;
	int size = 1<<n;
	int* nlen = new int[n];
	for(int i=0; i<n; i++)nlen[i]=i;
	do {
    	   int* arr = new int[size];
	   for(int i=0; i<size; i++)arr[i]=i;
           hulk(nlen, arr, n-1);
	   permutation_vector.push_back(arr);

  	} while(next_permutation(nlen,nlen+n));
	map<pair<int,int>,vector<string>> hashmap;
	map<pair<int,int>,vector<string>>:: iterator itr;
	for(int i=0; i<m; i++)
	{
		cin >> s;
		int b=0;
		for (int j=0; j<n; j++) b += (int)s[1<<j];
		pair<int,int> l = make_pair(count(s.begin(),s.end(),'1'),b);
		hashmap[l].push_back(s);
	}
    int j=0; /*adjnfdsj asdjgn*/
	/*vector<vector<int>> per;
	vector<int> arr;
	for(int i=0;i<n;i++)
		arr.push_back(i);
	do{
		per.push_back(arr);
	}while(next_permutation(arr.begin(),arr.end()));*/
        int ctr=0;
        for (itr=hashmap.begin(); itr!=hashmap.end();++itr){
                vector<string> remember;
		//cout << itr->first <<'\t';
		//vector<string> (itr->second) = itr->second;
 		for (int i=0; i<itr->second.size(); i++){
                    bool flag=1;
                    for (int j=0; j<remember.size(); j++){
			if (equivalent(itr->second[i],remember[j])){flag=0;break;}
                    }
                    if(flag)remember.push_back(itr->second[i]);
                }
		ctr = ctr + remember.size();
        }
        cout << ctr << "\n";

}
