# Crontab Expression: https://crontab.guru/.

vifcroexp library will allow you to check if the crontab parameters are correct.
you need to follow the order of the schedule expression like in the web site: (minute, hour, day_month, month, day_week)

  - minute: allowed values 0-59.

  - hour: allowed values 0-23.

  - day_month: allowed values 1-31.

  - month: allowed values 1-12.

  - day_week: allowed values 1-7.
  
  - '*' any value.

Parameter:

  - crontab_parameter => need to be a string.

Return:

  - If the parameters are valid, otherwise it will raise an error: 'Parameters are not correct'.


```console
>>> from croexp import vifcroexp
>>> vifcroexp("*,0,1,4,4")
```