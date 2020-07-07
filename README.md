# coxusage-docker


Python web scraper designed to return Cox Communications internet usage data

## Usage

You can run the tool from the container using [prebuilt Docker image](https://hub.docker.com/r/ntalekt/coxusage). The container has 1 mount point:
-  ``/data`` this is where the output will be stored.

You also need to create an enviroment file (e.g. secret/cox.env) with the following contents

```
COX_USER=username
COX_PASSWORD=password
JSON_LOCATION=/data/coxusage.json
```

To run ::

    docker run \
       -ti \
       --name coxusage \
	   --env-file /YOUR_LOCAL/PATH/TO_ENV/cox.env \
       -v /YOUR_LOCAL/PATH/TO_OUTPUT:/data \
       ntalekt/coxusage
	   
Personally I like to run it via cron (my personal example) ::
```
0 0 * * * /usr/bin/docker run --rm --name coxusage --env-file /mnt/nas2/coxusage-docker/config/cox.env -v /mnt/nas2/coxusage-docker/output:/data ntalekt/coxusage > /dev/null 2>&1
```

## Home Assistant Card Example
![Alt text](/img/HA_Example.JPG?raw=true)
```
title: Cox Internet Usage
type: entities
entities:
  - entity: sensor.cox_utilization
    icon: mdi:percent
  - entity: sensor.cox_time_left
    icon: mdi:calendar-clock
  - entity: sensor.cox_avg_gb_current
    icon: mdi:chart-line
  - entity: sensor.cox_avg_gb_remaining
    icon: mdi:chart-line-stacked
show_header_toggle: false
```

### Sensor Component
-----
```
sensor:
  - platform: command_line
    command: cal $(date +"%m %Y") | awk 'NF {DAYS = $NF}; END {print DAYS}'
    name: Days In Current Month
    scan_interval: 3600

  - platform: file
    name: Cox Utilization
    file_path: /YOUR_LOCAL/PATH/TO_OUTPUT/coxusage.json
    value_template: >
      {% if value_json is defined %}
        {% if value_json.dumUsage | int == 0 and value_json.dumLimit | int == 0 and value_json.dumUtilization | int == 0 %}
          stats unavailable
        {% else %}
          {{ value_json.dumUsage | int }} / {{ value_json.dumLimit | int }} GB ({{ value_json.dumUtilization | int }} %)
        {% endif %}
      {% else %}
        undefined
      {% endif %}

  - platform: file
    name: Cox Time Left
    file_path: /YOUR_LOCAL/PATH/TO_OUTPUT/coxusage.json
    value_template: >
      {% if value_json is defined %}
        {% if value_json.dumDaysLeft is defined %}
          {{ value_json.dumDaysLeft | int }} Days
        {% else %}
          unknown
        {% endif %}
      {% else %}
        undefined
      {% endif %}

  - platform: file
    name: Cox Avg GB Current
    file_path: /YOUR_LOCAL/PATH/TO_OUTPUT/coxusage.json
    value_template: >
      {% if value_json is defined %}
        {% if value_json.dumUsage | int == 0 and value_json.dumDaysLeft | int == 0 %}
          stats unavailable
        {% elif states.sensor.days_in_current_month.state is defined %}
          {{ (float(value_json.dumUsage) / (float(states.sensor.days_in_current_month.state) - float(value_json.dumDaysLeft))) | round(1) }} GB per day
        {% else %}
          month_undefined
        {% endif %}
      {% else %}
        undefined
      {% endif %}

  - platform: file
    name: Cox Avg GB Remaining
    file_path: /YOUR_LOCAL/PATH/TO_OUTPUT/coxusage.json
    value_template: >
      {% if value_json is defined %}
        {% if value_json.dumLimit | int == 0 and value_json.dumUsage | int == 0 and value_json.dumDaysLeft | int == 0 %}
          stats unavailable
        {% else %}
          {{ ((float(value_json.dumLimit) - float(value_json.dumUsage)) / float(value_json.dumDaysLeft)) | round(1) }} GB per day
        {% endif %}
      {% else %}
        undefined
      {% endif %}
```


