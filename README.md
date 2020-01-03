This project(residing in https:/github/rbjork/MarsWeatherProbe) contains the code for building a AWS cloud based IoT application.  As with most IoT application, it contains code to support device(s) calls to the cloud,  code to run on the cloud, and code that runs on a monitoring/control applications for humans to interact with.  

This project was started with the intention to meet several requirements as stated in the following:  Assume a data source containing weather data is being generated on a daily basis from the planet Mars.  Come up with a solution to receive, record and measure the average temperature.  Also, trigger some kind event when the temperature drops below some specified value.

The following assumptions were made after the above specification was provided.  First that Amazon Web Services (AWS) would be used and those services would accumulate a log of temperature readings along with meta information.

Final design:

Two fictitious remote sensors:
Temperature sensor: measures temperature(implemented in MarsProbeTempeture)
Windsensor: measures wind direction (implemented in MarsProbeWindSensor)

One device that collects sensor data:
This may be either and local(on Mars) network hub with networked connected sensors or a unit that contains sensor data via tcp/ip socket connections. This unit is also communicates with the cloud through the AWS API Gateway.  This was implemented in the module/file MarsProbeRadioTransceiver.

The cloud contains 5 components:
An API Gateway 'MarsWeather' with url "https://vlqojfxgzl.execute-api.us-west-1.amazonaws.com/marsweather1"


A Lambda function, 'weatherlogging', to receive and process the above API call. This code resides in 'lambdas/api2s3.py” file.

An S3 bucket 's3-to-es-bucket'

A Lambda function, 's3-log-indexing', thats triggered by 'put' events to the above s3 bucket. This code resides in 'lambdas/S3toES.py'. This code extracts 'meta' data of the log in s3 and pushes it the ElasticSearch.

A EC2 based Web application to retrieve and display log data.  This was deployed with EC2. This code resides in 'app.py' and 'EarthCommandConsole.py'. URL: http://ec2-54-193-55-167.us-west-1.compute.amazonaws.com/


Two additional utility classes reside in the repo: ConfigParser and WeatherDataParser.py.
This ConfigParser assists the other modules to extract their needed parameter values from sysconfig.json

Unit Tests:
There are two unit tests(along with testrunner suite) that this project contains. They reside in 'test folder.
