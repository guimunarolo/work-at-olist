# API Documentation

Here you can understand how this API works.


## URL

- [https://thawing-meadow-82188.herokuapp.com/v1](https://thawing-meadow-82188.herokuapp.com/v1/)


## Accepted

- `json`


## Call Events Record

| Endpoint                | Method | Response     |
| ----------------------- |:------:| :-----------:|
| /telephony/call-events/ | `POST` | `201`, `400` |

### Fields

| Field               | Type    | Description                                          | Required              | Default           |
| ------------------- |:-------:| ---------------------------------------------------- |:---------------------:| ----------------- |
| type                | string  | Indicate if it's a call "start" or "end" record      | No                    | "start"           |
| timestamp           | int     | Valid timestamp that event happens                   | No                    | Current timestamp |
| call_id             | int     | Call identification                                  | Only for "end" type   | Identification    |
| source              | string  | The subscriber phone number that originated the call | Only for "start" type |                   |
| destination         | string  | The phone number receiving the call                  | Only for "start" type |                   |

**Note:** The phone number format is AAXXXXXXXXX, where AA is the area code and XXXXXXXXX is the phone number.
The phone number is composed of 8 or 9 digits.

### Examples

- Start call event:

```
{
  "type":  "start", // or null to get start as default
  "timestamp":  1527001196, // or null to get current timestamp
  "call_id":  123, // or null to application generates
  "source":  "11991232344",
  "destination":  "11994345337"
}
```

- End call event:

```
{
 "type":  "end",
 "timestamp":  1527001199, // or null to get current timestamp
 "call_id":  123,
}
```

### Responses

- `201` - `Created` - Return the created object;
- `400` - `Bad Request` - Return the validation error.


## Bill Report

| Endpoint                            | Method | Response |
| ----------------------------------- |:------:|:--------:|
| /telephony/bill-report/AAXXXXXXXXX/ | `GET`  | `200`    |

**Note:** The phone number format is AAXXXXXXXXX, where AA is the area code and XXXXXXXXX is the phone number.
The phone number is composed of 8 or 9 digits.

### Filters

| Field | Type | Description                 | Required | Default        |
| ----- |:----:| --------------------------- |:--------:| -------------- |
| month | int  | Month that you wanna filter | No       | Previous month |
| year  | int  | Year that you wanna filter  | No       | Previous year  |

**Note:** It's only possible to get a telephone bill after the reference period has ended.

### Examples

- [https://thawing-meadow-82188.herokuapp.com/v1/telephony/bill-report/99988526423/?month=12&year=2017](https://thawing-meadow-82188.herokuapp.com/v1/telephony/bill-report/99988526423/?month=12&year=2017):

```
{
  "count": 6,
  "filters": {
    "month": 12,
    "year": 2017
  },
  "objects": [
    {
      "destination": "9993468278",
      "start_date": "2017-12-12",
      "start_time": "15:07:13",
      "duration": "0h7m43s",
      "price": "R$ 0,99"
    },
    {
      "destination": "9993468278",
      "start_date": "2017-12-12",
      "start_time": "22:47:56",
      "duration": "0h3m0s",
      "price": "R$ 0,36"
    },
    {
      "destination": "9993468278",
      "start_date": "2017-12-12",
      "start_time": "21:57:13",
      "duration": "0h13m43s",
      "price": "R$ 0,54"
    },
    {
      "destination": "9993468278",
      "start_date": "2017-12-12",
      "start_time": "04:57:13",
      "duration": "1h13m43s",
      "price": "R$ 1,26"
    },
    {
      "destination": "9993468278",
      "start_date": "2017-12-12",
      "start_time": "21:57:13",
      "duration": "24h13m43s",
      "price": "R$ 86,94"
    },
    {
      "destination": "9993468278",
      "start_date": "2017-12-12",
      "start_time": "15:07:58",
      "duration": "0h4m58s",
      "price": "R$ 0,72"
    }
  ]
}
```

### Responses

- `200` - `Ok` - Return the report bill;
