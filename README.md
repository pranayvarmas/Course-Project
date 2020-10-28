Welcome to our project:-

We have implemented a user interface where the client can login with their credentials. If they are new to this application, they can create an account. The client can also change their password at will. After that, the client has to give the application a passcode which is exclusive to their university. For now, it is 123456 and it is subject to change and improvements. After this, the client would get directed to a page where he can upload files of any type. Also, there is button named "Your files" which will give access to the download links of all your uploaded files. Also, there will be button for "home" in this page which will take the client to the upload/welcome page. The client can log himself out after. 

All this has been done using django for both frontend and the backend which is a python web framework.

What to expect in the future:-

Right now, there is only one passcode for everyone, we will extend it to a bunch of unversities, for this, we will add one more feature which asks the client his university while he is registering himself. Also, we will implement the "forgot password" feature, where a randomly generated OTP will be asked and then the client has to type that and if it is the right one, the webpage will be redirected to the "change password" page where he can change his password. For this, the client has to give his email while registering himself. Also, we need to improve the routing for the page which asks the organization passcode. Also, finally a "Result" button will be added, which lets you download the output file which is a "csv" file or "plot" image (subject to change) which is the result of the this copy checker. The upload of a "zip" file is encouraged. Also, for now we added a basic styles for the website and it is subject to improvement.

We are yet to implement a python script which compares multiple files and produces an output csv file or a plot image (which can be changed in the future) which will be integrated into the django framework in the future. We are planning

