# K-Time-Kit ⏱️

This project is a Python implementation of the Duration class, which represents a duration of time in years, days, hours, minutes, and seconds. It allows you to easily manipulate durations of time with arithmetic operations, conversions, and comparisons.

## Features 💡

* The Duration class can accept floating-point values for its parameters, and convert them to a standard time format.
* The Duration class can be added, subtracted, and compared to other durations with the operators `+`, `-`, `==`, `<=`, and `<`.
* The Duration class can be converted to seconds, minutes, hours, days, or years with the methods `to_sec`, `to_min`, `to_hour`, `to_day`, and `to_year`.
* The DurationInt class is an integer version of the Duration class, which allows you to manipulate large integers more efficiently.

## Examples of use 📝

```python
# Create a duration of 3 years, 2 days, 4 hours, 30 minutes, and 15 seconds
d1 = Duration(15, 30, 4, 2, 3)
print(d1) # prints "3.0y 2.0d 4.0h 30.0m 15.0s"

# Create a duration of 0.5 year, 0.25 day, 0.125 hour, 0.0625 minute, and 0.03125 second
d2 = Duration(0.03125, 0.0625, 0.125, 0.25, 0.5)
print(d2) # prints "0.0y 182.0d 18.0h 7.0m 33.78125s"

# Add two durations
d3 = d1 + d2
print(d3) # prints "3.0y 184.0d 22.0h 37.0m 48.78125s"

# Subtract two durations
d4 = d3 - d1
print(d4) # prints "0.0y 182.0d 18.0h 7.0m 33.78125s"

# Compare two durations
print(d1 == d2) # prints "False"
print(d1 <= d2) # prints "False"
print(d1 < d2) # prints "False"

# Convert a duration to seconds
print(d1.to_sec()) # prints "94770115.0"

# Convert a duration to minutes
print(d1.to_min()) # prints "1579950.25"

# Convert a duration to hours
print(d1.to_hour()) # prints "26332.504166666666"

# Convert a duration to days
print(d1.to_day()) # prints "1097.1876736111112"

# Convert a duration to years
print(d1.to_year()) # prints "3.0059936263318114"

# Create an integer duration of 1000000000 seconds
d5 = DurationInt(1000000000)
print(d5) # prints "31y 259d 1h 46m 40s"
```

## Author ✍️

This project was created by KpihX. You can contact me at kapoivha@gmail.com for any questions or suggestions.

## License 📄

This project is licensed under the MIT license - see the LICENSE file for more details.

: https://github.com/KpihX
